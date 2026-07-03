"use strict";

const { loadConfig, saveConfig } = require("./config");

const LANGUAGE_CATALOG = [
  ["en", "English", "ClawVoice Agent Voice"],
  ["es", "Español", "ClawVoice Voz de agente"],
  ["fr", "Français", "ClawVoice Voix d'agent"],
  ["de", "Deutsch", "ClawVoice Agentenstimme"],
  ["it", "Italiano", "ClawVoice Voce agente"],
  ["pt", "Português", "ClawVoice Voz de agente"],
  ["nl", "Nederlands", "ClawVoice Agentstem"],
  ["pl", "Polski", "ClawVoice Głos agenta"],
  ["cs", "Čeština", "ClawVoice Hlas agenta"],
  ["hu", "Magyar", "ClawVoice Ügynökhang"],
  ["ro", "Română", "ClawVoice Vocea agentului"],
  ["el", "Ελληνικά", "ClawVoice Φωνή πράκτορα"],
  ["sv", "Svenska", "ClawVoice Agentröst"],
  ["da", "Dansk", "ClawVoice Agentstemme"],
  ["fi", "Suomi", "ClawVoice Agenttiääni"],
  ["no", "Norsk", "ClawVoice Agentstemme"],
  ["ru", "Русский", "ClawVoice Голос агента"],
  ["uk", "Українська", "ClawVoice Голос агента"],
  ["tr", "Türkçe", "ClawVoice Ajan sesi"],
  ["ar", "العربية", "ClawVoice صوت الوكيل"],
  ["he", "עברית", "ClawVoice קול סוכן"],
  ["hi", "हिन्दी", "ClawVoice एजेंट आवाज़"],
  ["bn", "বাংলা", "ClawVoice এজেন্ট ভয়েস"],
  ["id", "Bahasa Indonesia", "ClawVoice Suara agen"],
  ["ms", "Bahasa Melayu", "ClawVoice Suara ejen"],
  ["fil", "Filipino", "ClawVoice Boses ng ahente"],
  ["vi", "Tiếng Việt", "ClawVoice Giọng nói tác nhân"],
  ["th", "ไทย", "ClawVoice เสียงเอเจนต์"],
  ["ja", "日本語", "ClawVoice エージェント音声"],
  ["ko", "한국어", "ClawVoice 에이전트 음성"],
  ["zh", "中文", "ClawVoice 智能代理语音"],
];

const TIER_EXAMPLES = ["base", "pro", "custom", "base-long", "pro-long", "custom-long"];

function usage() {
  console.log(`Usage:
  clawvoice voice
  clawvoice voice <voice-id>
  clawvoice voice --voice <voice-id> --lang <language-code> --tier <endpoint-tier>
  clawvoice voice --preset <preset-id> --mix <mix-id>
  clawvoice voice --expression <expression-id> --level <0-1> --control <name=value>
  clawvoice voice --clear-controls
  clawvoice voice --languages
  clawvoice voice --tiers

Examples:
  clawvoice voice
  clawvoice voice M1
  clawvoice voice --lang es
  clawvoice voice --tier pro
  clawvoice voice --preset calm
  clawvoice voice --mix narrator
  clawvoice voice --expression cheerful --level 0.7
  clawvoice voice --control speed=1.1 --control pitch=0.2
  clawvoice voice --clear-controls
  clawvoice voice --voice F1 --lang fr --tier base --preset calm --mix narrator --expression cheerful

Voice IDs, language codes, tiers, presets, mixes, expressions, and expression controls depend on the active voice engine or hosted voice service.
M1, en, and base are the defaults. Preset, mix, expression, and expression controls are unset by default.`);
}

function valueAfter(args, names) {
  for (let i = 0; i < args.length; i++) {
    if (names.includes(args[i])) return args[i + 1] || null;
  }
  return null;
}

function printLanguages() {
  console.log(JSON.stringify({
    count: LANGUAGE_CATALOG.length,
    default: "en",
    set: "clawvoice voice --lang <code>",
    languages: LANGUAGE_CATALOG.map(([code, name, localizedName]) => ({ code, name, localizedName })),
  }, null, 2));
}

function printTiers() {
  console.log(JSON.stringify({
    default: "base",
    set: "clawvoice voice --tier <tier>",
    examples: TIER_EXAMPLES,
    note: "Endpoint tiers are passed through to /v1/tts/<tier> so new hosted endpoints can be used without a package update.",
  }, null, 2));
}

function parseControls(args) {
  const controls = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] !== "--control" && args[i] !== "--expression-control" && args[i] !== "--knob") continue;
    const raw = args[i + 1] || "";
    const idx = raw.indexOf("=");
    if (idx <= 0) continue;
    const key = raw.slice(0, idx);
    const value = raw.slice(idx + 1);
    const numeric = Number(value);
    controls[key] = Number.isFinite(numeric) && value.trim() !== "" ? numeric : value;
  }
  return controls;
}

function voice(args) {
  const config = loadConfig();
  if (!config) {
    console.error("Not set up yet. Run: clawvoice init");
    process.exit(1);
  }

  if (args.includes("--help") || args.includes("-h")) return usage();
  if (args.includes("--languages")) return printLanguages();
  if (args.includes("--tiers") || args.includes("--endpoints")) return printTiers();

  const positionalVoice = args[0] && !args[0].startsWith("-") ? args[0] : null;
  const voiceId = valueAfter(args, ["--voice", "-v"]) || positionalVoice;
  const language = valueAfter(args, ["--lang", "--language", "-l"]);
  const tier = valueAfter(args, ["--tier", "--endpoint", "-t"]);
  const preset = valueAfter(args, ["--preset", "-p"]);
  const mix = valueAfter(args, ["--mix", "-m"]);
  const expression = valueAfter(args, ["--expression", "-e"]);
  const level = valueAfter(args, ["--level", "--expression-level"]);
  const expressionControls = parseControls(args);
  const hasControls = Object.keys(expressionControls).length > 0;
  const clearControls = args.includes("--clear-controls") || args.includes("--clear-expression-controls") || args.includes("--clear-knobs");

  if (!voiceId && !language && !tier && !preset && !mix && !expression && !level && !hasControls && !clearControls) {
    console.log(JSON.stringify({
      current: {
        hosted: config.hostedVoice?.voice || "M1",
        local: config.localVoice?.voice || config.hostedVoice?.voice || "M1",
        language: config.hostedVoice?.language || config.localVoice?.language || "en",
        tier: config.hostedVoice?.tier || "base",
        preset: config.hostedVoice?.preset || config.localVoice?.preset || null,
        mix: config.hostedVoice?.mix || config.localVoice?.mix || null,
        expression: config.hostedVoice?.expression || config.localVoice?.expression || null,
        expressionLevel: config.hostedVoice?.expressionLevel ?? config.localVoice?.expressionLevel ?? null,
        expressionControls: config.hostedVoice?.expressionControls || config.localVoice?.expressionControls || config.hostedVoice?.knobs || config.localVoice?.knobs || {},
      },
      defaults: { voice: "M1", language: "en", tier: "base", preset: null, mix: null, expression: null, expressionLevel: null, expressionControls: {} },
      changeVoice: "clawvoice voice <voice-id>",
      changeLanguage: "clawvoice voice --lang <language-code>",
      changeTier: "clawvoice voice --tier <base|pro|custom|...>",
      changePreset: "clawvoice voice --preset <preset-id>",
      changeMix: "clawvoice voice --mix <mix-id>",
      changeExpression: "clawvoice voice --expression <expression-id> --level <0-1>",
      changeExpressionControls: "clawvoice voice --control <name=value> --control <name=value>",
      clearExpressionControls: "clawvoice voice --clear-controls",
      languages: "clawvoice voice --languages",
      tiers: "clawvoice voice --tiers",
      test: 'clawvoice speak "testing the new voice"',
    }, null, 2));
    return;
  }

  config.hostedVoice = { ...(config.hostedVoice || {}) };
  config.localVoice = { ...(config.localVoice || {}) };
  if (voiceId) {
    config.hostedVoice.voice = voiceId;
    config.localVoice.voice = voiceId;
  }
  if (language) {
    config.hostedVoice.language = language;
    config.localVoice.language = language;
  }
  if (tier) config.hostedVoice.tier = tier;
  if (preset) {
    config.hostedVoice.preset = preset === "none" ? null : preset;
    config.localVoice.preset = preset === "none" ? null : preset;
  }
  if (mix) {
    config.hostedVoice.mix = mix === "none" ? null : mix;
    config.localVoice.mix = mix === "none" ? null : mix;
  }
  if (expression) {
    config.hostedVoice.expression = expression === "none" ? null : expression;
    config.localVoice.expression = expression === "none" ? null : expression;
  }
  if (level) {
    const numeric = Number(level);
    const next = level === "none" ? null : Number.isFinite(numeric) ? numeric : level;
    config.hostedVoice.expressionLevel = next;
    config.localVoice.expressionLevel = next;
  }
  if (hasControls) {
    config.hostedVoice.expressionControls = { ...(config.hostedVoice.expressionControls || config.hostedVoice.knobs || {}), ...expressionControls };
    config.localVoice.expressionControls = { ...(config.localVoice.expressionControls || config.localVoice.knobs || {}), ...expressionControls };
  }
  if (clearControls) {
    config.hostedVoice.expressionControls = {};
    config.localVoice.expressionControls = {};
    delete config.hostedVoice.knobs;
    delete config.localVoice.knobs;
  }
  saveConfig(config);
  console.log(
    `Voice options saved: voice=${config.hostedVoice.voice || "M1"}, lang=${config.hostedVoice.language || "en"}, tier=${config.hostedVoice.tier || "base"}, preset=${config.hostedVoice.preset || "none"}, mix=${config.hostedVoice.mix || "none"}, expression=${config.hostedVoice.expression || "none"}, level=${config.hostedVoice.expressionLevel ?? "none"}`,
  );
  console.log('Test it with: clawvoice speak "testing the new voice"');
}

module.exports = { LANGUAGE_CATALOG, TIER_EXAMPLES, voice };
