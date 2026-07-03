#!/usr/bin/env node
"use strict";

const fs = require("fs");
const paths = require("../lib/paths");
const { loadConfig, requireConfig } = require("../lib/config");
const { loadWallet } = require("../lib/wallet");
const { spentTodayUsd } = require("../lib/spend");
const { commandExists } = require("../lib/mic");

function usage() {
  console.log(`ClawVoice by ForgeMesh Labs — Voice and TTS controls for OpenClaw agents

Usage:
  clawvoice init [--mode local|hosted|hybrid] [--mic] [--yes] [--voice M1] [--lang en] [--tier base] [--preset id] [--mix id] [--expression id] [--level 0.7] [--control name=value]
  clawvoice speak "text to say" [--out file.wav] [--approve] [--no-play]
  clawvoice stop
  clawvoice listen [--seconds N] [--file audio.wav] [--model base] [--keep]
  clawvoice talk [--agent "claude -p"] [--approve] [--model base]
  clawvoice wallet
  clawvoice balance
  clawvoice withdraw --to 0xYourWallet --amount all|N [--yes]
  clawvoice products
  clawvoice voice [voice-id] [--lang code] [--tier tier] [--preset id] [--mix id] [--expression id] [--level 0.7] [--control name=value] [--clear-controls]
  clawvoice config
  clawvoice voice-check
  clawvoice voice-serve | voice-stop
  clawvoice install-voice [--dry-run]
  clawvoice install-mic [--dry-run] [--yes]

init runs an interactive setup: pick a voice mode, get a wallet address to fund,
and your agent starts talking. Private keys stay local and are never printed.

listen is push-to-talk: recording starts immediately and stops when you press Enter.
talk is a full conversation loop: talk -> agent replies out loud, until you say exit.
Wake word and always-on listening: coming soon.

Aliases: clawvoice, agentvoice, x402-agent-voice`);
}

function walletCmd() {
  const walletData = loadWallet();
  const config = loadConfig();
  console.log(
    JSON.stringify(
      {
        address: walletData.address,
        chain: walletData.chain || "base",
        network: walletData.network || "base-mainnet",
        token: "USDC",
        fundingNote: "Send only a small working balance to this hot wallet.",
        policy: config?.x402Policy || null,
      },
      null,
      2,
    ),
  );
}

function configCmd() {
  console.log(JSON.stringify(requireConfig(), null, 2));
}

function productsCmd() {
  const config = requireConfig();
  console.log(JSON.stringify({
    discoveryOrder: config.products?.discoveryOrder || ["preloaded", "agentcash"],
    products: config.products?.preloaded || [],
    note: config.products?.note || null,
  }, null, 2));
}

async function voiceCheckCmd() {
  const { cliInstalled, serverHealthy } = require("../lib/tts-local");
  const { micStatus } = require("../lib/mic");
  const { formatVersion, probePython } = require("../lib/python");
  const config = loadConfig();
  const serverUrl = config?.localVoice?.serverUrl || paths.DEFAULT_LOCAL_SERVER_URL;
  const mic = micStatus();
  const python = probePython();

  console.log(
    JSON.stringify(
      {
        node: process.version,
        python3: commandExists("python3"),
        localVoicePython: python.selected
          ? {
              bin: python.selected,
              version: formatVersion(
                (python.override || python.candidates.find((candidate) => candidate.bin === python.selected))?.version,
              ),
            }
          : null,
        pythonProbe: python.override
          ? [{ bin: python.override.bin, version: formatVersion(python.override.version), compatible: python.override.compatible }]
          : python.candidates.map((candidate) => ({
              bin: candidate.bin,
              version: formatVersion(candidate.version),
              compatible: candidate.compatible,
            })),
        mode: config?.mode || null,
        configExists: fs.existsSync(paths.CONFIG_PATH),
        walletExists: fs.existsSync(paths.WALLET_PATH),
        localVoiceInstalled: cliInstalled(),
        localServerHealthy: await serverHealthy(serverUrl),
        localServerUrl: serverUrl,
        micEnabled: config?.mic?.enabled ?? false,
        ffmpeg: mic.ffmpeg,
        whisper: mic.whisper,
        spentTodayUsd: Number(spentTodayUsd().toFixed(6)),
        dailyCapUsd: config?.x402Policy?.dailyCapUsd || null,
        conversation: config?.conversation || null,
      },
      null,
      2,
    ),
  );
}

function parseSpeakArgs(args) {
  const opts = { out: null, approve: false, play: true };
  const words = [];
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === "--out") opts.out = args[++i];
    else if (a === "--approve") opts.approve = true;
    else if (a === "--no-play") opts.play = false;
    else words.push(a);
  }
  return { text: words.join(" "), opts };
}

async function main() {
  const [, , command, ...args] = process.argv;
  if (!command || command === "--help" || command === "-h") return usage();

  switch (command) {
    case "init":
      return require("../lib/init").init(args);
    case "speak": {
      const { text, opts } = parseSpeakArgs(args);
      return require("../lib/speak").speak(text, opts);
    }
    case "stop":
    case "silence":
      return require("../lib/playback").stopPlayback();
    case "wallet":
      return walletCmd();
    case "balance":
      return require("../lib/balance").balance();
    case "withdraw":
      return require("../lib/withdraw").withdraw(args);
    case "products":
      return productsCmd();
    case "voice":
      return require("../lib/voice").voice(args);
    case "config":
      return configCmd();
    case "voice-check":
      return voiceCheckCmd();
    case "voice-serve":
      return require("../lib/local-runtime").serveStart(requireConfig());
    case "voice-stop":
      return require("../lib/local-runtime").serveStop();
    case "install-voice": {
      const ok = require("../lib/local-runtime").installVoice({ dryRun: args.includes("--dry-run") });
      if (!ok) process.exit(1);
      return;
    }
    case "install-mic":
      return require("../lib/mic").installMic(requireConfig(), {
        dryRun: args.includes("--dry-run"),
        yes: args.includes("--yes") || args.includes("-y"),
      });
    case "listen": {
      const opts = { seconds: null, file: null, model: null, keep: false };
      for (let i = 0; i < args.length; i++) {
        if (args[i] === "--seconds") opts.seconds = parseFloat(args[++i]);
        else if (args[i] === "--file") opts.file = args[++i];
        else if (args[i] === "--model") opts.model = args[++i];
        else if (args[i] === "--keep") opts.keep = true;
      }
      const cfgModel = requireConfig().conversation?.whisperModel;
      const result = await require("../lib/stt").listen({ ...opts, model: opts.model || cfgModel });
      console.log(JSON.stringify(result, null, 2));
      return;
    }
    case "talk": {
      const opts = { agent: null, approve: false, model: null };
      for (let i = 0; i < args.length; i++) {
        if (args[i] === "--agent") opts.agent = args[++i];
        else if (args[i] === "--approve") opts.approve = true;
        else if (args[i] === "--model") opts.model = args[++i];
      }
      return require("../lib/talk").talk(opts);
    }
    default:
      console.error(`Unknown command: ${command}`);
      usage();
      process.exit(1);
  }
}

main().catch((err) => {
  console.error(err?.message || err);
  process.exit(1);
});
