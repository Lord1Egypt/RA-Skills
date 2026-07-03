"use strict";

const paths = require("./paths");
const { ensureDir } = require("./fsutil");
const { MODES, defaultConfig, loadConfig, saveConfig } = require("./config");
const { ensureWallet } = require("./wallet");
const { isInteractive, ask, askYesNo, askChoice } = require("./prompt");
const { installVoice } = require("./local-runtime");
const { speak } = require("./speak");

const MODE_CHOICES = [
  "Free local voice   — runs on your machine, free after setup",
  "Hosted voice       — no install, pays per call from your agent wallet",
  "Hybrid             — local first, hosted fallback (recommended)",
];

function parseFlags(args) {
  const flags = { mode: null, mic: null, yes: false, install: null, voice: null, lang: null, tier: null, preset: null, mix: null, expression: null, level: null, expressionControls: {} };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === "--mode") flags.mode = args[++i];
    else if (a === "--mic") flags.mic = true;
    else if (a === "--no-mic") flags.mic = false;
    else if (a === "--yes" || a === "-y") flags.yes = true;
    else if (a === "--install") flags.install = true;
    else if (a === "--no-install") flags.install = false;
    else if (a === "--voice") flags.voice = args[++i];
    else if (a === "--lang" || a === "--language") flags.lang = args[++i];
    else if (a === "--tier" || a === "--endpoint") flags.tier = args[++i];
    else if (a === "--preset") flags.preset = args[++i];
    else if (a === "--mix") flags.mix = args[++i];
    else if (a === "--expression") flags.expression = args[++i];
    else if (a === "--level" || a === "--expression-level") flags.level = args[++i];
    else if (a === "--control" || a === "--expression-control" || a === "--knob") {
      const raw = args[++i] || "";
      const idx = raw.indexOf("=");
      if (idx > 0) {
        const value = raw.slice(idx + 1);
        const numeric = Number(value);
        flags.expressionControls[raw.slice(0, idx)] = Number.isFinite(numeric) && value.trim() !== "" ? numeric : value;
      }
    }
  }
  if (flags.mode && !MODES.includes(flags.mode)) {
    console.error(`Invalid --mode "${flags.mode}". Use: ${MODES.join(" | ")}`);
    process.exit(1);
  }
  return flags;
}

async function askWithDefault(question, current) {
  const answer = await ask(`${question} [${current || "none"}]: `);
  if (!answer) return current || null;
  return answer === "none" ? null : answer;
}

async function resolveVoiceOptions({ flags, existing, interactive }) {
  const current = {
    voice: flags.voice || existing.hostedVoice?.voice || "M1",
    lang: flags.lang || existing.hostedVoice?.language || existing.hostedVoice?.lang || "en",
    tier: flags.tier || existing.hostedVoice?.tier || "base",
    preset: flags.preset ?? existing.hostedVoice?.preset ?? null,
    mix: flags.mix ?? existing.hostedVoice?.mix ?? null,
    expression: flags.expression ?? existing.hostedVoice?.expression ?? null,
    level: flags.level ?? existing.hostedVoice?.expressionLevel ?? null,
    expressionControls: Object.keys(flags.expressionControls).length ? flags.expressionControls : existing.hostedVoice?.expressionControls || existing.hostedVoice?.knobs || {},
  };

  if (interactive && !flags.voice && !flags.lang && !flags.tier && flags.preset === null && flags.mix === null && flags.expression === null && flags.level === null && !Object.keys(flags.expressionControls).length) {
    const customize = await askYesNo("\nCustomize your agent's voice now?", false);
    if (!customize) return current;
    console.log("Options: voice ID, language, endpoint tier, preset, mix, expression, expression level, and expression controls.");
    console.log('Press Enter to keep the current value. Type "none" to clear preset or mix.');
    current.voice = await askWithDefault("Voice ID", current.voice);
    current.lang = await askWithDefault("Language code", current.lang);
    current.tier = await askWithDefault("Hosted endpoint tier", current.tier);
    current.preset = await askWithDefault("Preset", current.preset);
    current.mix = await askWithDefault("Mix", current.mix);
    current.expression = await askWithDefault("Expression", current.expression);
    current.level = await askWithDefault("Expression level", current.level);
    const controlLine = await ask("Expression controls as name=value pairs, comma-separated [none]: ");
    if (controlLine && controlLine !== "none") {
      current.expressionControls = {};
      for (const part of controlLine.split(",")) {
        const idx = part.indexOf("=");
        if (idx <= 0) continue;
        const key = part.slice(0, idx).trim();
        const value = part.slice(idx + 1).trim();
        const numeric = Number(value);
        current.expressionControls[key] = Number.isFinite(numeric) && value !== "" ? numeric : value;
      }
    }
  }

  return current;
}

function applyVoiceOptions(config, options) {
  const levelNumber = Number(options.level);
  const expressionLevel = options.level === "none" || options.level == null
    ? null
    : Number.isFinite(levelNumber)
      ? levelNumber
      : options.level;
  config.hostedVoice = { ...(config.hostedVoice || {}) };
  config.localVoice = { ...(config.localVoice || {}) };
  config.hostedVoice.voice = options.voice || "M1";
  config.localVoice.voice = options.voice || "M1";
  config.hostedVoice.language = options.lang || "en";
  config.localVoice.language = options.lang || "en";
  config.hostedVoice.tier = options.tier || "base";
  config.hostedVoice.preset = options.preset || null;
  config.localVoice.preset = options.preset || null;
  config.hostedVoice.mix = options.mix || null;
  config.localVoice.mix = options.mix || null;
  config.hostedVoice.expression = options.expression || null;
  config.localVoice.expression = options.expression || null;
  config.hostedVoice.expressionLevel = expressionLevel;
  config.localVoice.expressionLevel = expressionLevel;
  config.hostedVoice.expressionControls = options.expressionControls || {};
  config.localVoice.expressionControls = options.expressionControls || {};
}

async function init(args) {
  const flags = parseFlags(args);
  const interactive = isInteractive() && !flags.yes;
  const existing = loadConfig() || {};

  console.log("Hello world! Thanks for using ClawVoice by ForgeMesh Labs.");
  console.log("Feedback and bugs: clawdbotworker@gmail.com\n");
  console.log("ClawVoice setup\n");

  let mode = flags.mode;
  if (!mode) {
    if (interactive) {
      const idx = await askChoice("How should your agent speak?", MODE_CHOICES, 2);
      mode = MODES[idx];
    } else {
      mode = existing.mode || "hybrid";
    }
  }

  let micEnabled = flags.mic;
  if (micEnabled === null) {
    if (interactive) {
      micEnabled = await askYesNo(
        "\nEnable mic support later (FFmpeg + Whisper, so you can talk to your agent)?",
        false,
      );
    } else {
      micEnabled = existing.mic?.enabled ?? false;
    }
  }

  const voiceOptions = await resolveVoiceOptions({ flags, existing, interactive });

  ensureDir(paths.APP_DIR);
  ensureDir(paths.VOICE_DIR);

  // Wallet is always created, in every mode — it powers hosted voice and future paid agent tools.
  const { wallet, created } = await ensureWallet();
  const config = defaultConfig({ walletAddress: wallet.address, mode, micEnabled, existing });
  applyVoiceOptions(config, voiceOptions);
  saveConfig(config);

  console.log(`\n✔ Setup saved (mode: ${mode}${micEnabled ? ", mic: enabled" : ""})`);
  console.log(
    `✔ Voice options: voice=${config.hostedVoice.voice}, lang=${config.hostedVoice.language}, tier=${config.hostedVoice.tier}, preset=${config.hostedVoice.preset || "none"}, mix=${config.hostedVoice.mix || "none"}, expression=${config.hostedVoice.expression || "none"}, level=${config.hostedVoice.expressionLevel ?? "none"}`,
  );
  console.log(`✔ Wallet ${created ? "created" : "found"} — your agent's payment address:\n`);
  console.log(`    ${wallet.address}\n`);
  console.log("  Copy this address and send it a small USDC balance on Base network.");
  console.log("  This wallet pays for hosted voice and other paid agent tools.");
  console.log("  The private key stays on this machine and is never shown or sent anywhere.\n");

  let localInstalled = false;
  if (mode !== "hosted") {
    let doInstall = flags.install;
    if (doInstall === null) {
      doInstall = interactive
        ? await askYesNo("Install the local voice engine now (downloads Python packages)?", true)
        : false;
    }
    if (doInstall) localInstalled = installVoice({ dryRun: false });
    else console.log("Skipping local voice install. Run later: clawvoice install-voice");
  }

  if (micEnabled) {
    console.log("\nMic support flagged on. When you're ready: clawvoice install-mic");
  }

  if (localInstalled) {
    console.log("\nTesting your agent's voice...");
    try {
      await speak("Hello world. ClawVoice is ready.", { approve: false });
    } catch (_) {
      console.log('Test skipped — try it yourself: clawvoice speak "hello"');
    }
  } else {
    console.log("\nNext steps:");
    if (mode !== "hosted") console.log("  1. clawvoice install-voice   (free local speech)");
    if (mode !== "local") console.log(`  ${mode !== "hosted" ? "2" : "1"}. Fund the wallet address above with USDC on Base`);
    console.log(`  Then: clawvoice speak "hello world"`);
  }
}

module.exports = { init };
