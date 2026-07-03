"use strict";

const fs = require("fs");
const paths = require("./paths");
const { readJson, writePrivateJson } = require("./fsutil");

const CONFIG_VERSION = 6;
const MODES = ["local", "hosted", "hybrid"];

const PRELOADED_FORGEMESH_PRODUCTS = [
  {
    id: "voice",
    name: "ForgeMesh Voice",
    baseUrl: "https://voice.forgemesh.io",
    bestFor: "Agent speech / TTS",
    exampleEndpoint: "/v1/tts/base",
    startingPriceUsd: "0.001",
    protocol: "x402",
    affiliate: { pyrimidEligible: false },
    source: "preloaded",
  },
  {
    id: "coinopai",
    name: "CoinOpAI Market Intelligence",
    baseUrl: "https://x402.coinopai.com",
    bestFor: "Kronos signals, market intelligence, calibration, anomaly checks",
    exampleEndpoint: "/api/categories",
    startingPriceUsd: "0.005",
    protocol: "x402",
    affiliate: { pyrimidEligible: true, note: "Some CoinOpAI/Kronos routes are Pyrimid affiliate eligible." },
    source: "preloaded",
  },
  {
    id: "imagegen",
    name: "ForgeMesh ImageGen",
    baseUrl: "https://imagegen.coinopai.com",
    bestFor: "Paid image generation",
    exampleEndpoint: "/generate",
    startingPriceUsd: "0.25",
    protocol: "x402",
    affiliate: { pyrimidEligible: true, note: "ImageGen has existing Pyrimid affiliate routing in the ForgeMesh stack." },
    source: "preloaded",
  },
  {
    id: "anomaly",
    name: "ForgeMesh Anomaly",
    baseUrl: "https://anomaly.forgemesh.io",
    bestFor: "Sequence and mempool anomaly checks",
    exampleEndpoint: "/api/sequence-anomaly/status",
    startingPriceUsd: "0.01",
    protocol: "x402",
    affiliate: { pyrimidEligible: false },
    source: "preloaded",
  },
  {
    id: "disruption",
    name: "Disruption Intelligence",
    baseUrl: "https://disruption.forgemesh.io",
    bestFor: "WARN, disruption, source-health, and company event intelligence",
    exampleEndpoint: "/events/:id/severity",
    startingPriceUsd: "0.01",
    protocol: "x402",
    affiliate: { pyrimidEligible: false },
    source: "preloaded",
  },
  {
    id: "travel-agent",
    name: "ForgeMesh Travel Agent",
    baseUrl: "https://travel-agent.forgemesh.io",
    bestFor: "Travel pulse, transit providers, and agentic travel planning",
    exampleEndpoint: "/api/transit-providers",
    startingPriceUsd: "0.01",
    protocol: "x402",
    affiliate: { pyrimidEligible: false },
    source: "preloaded",
  },
  {
    id: "fare-intelligence",
    name: "Fare Intelligence",
    baseUrl: "https://travel.forgemesh.io",
    bestFor: "Fare intelligence and travel price context",
    exampleEndpoint: "/api/fare-intelligence",
    startingPriceUsd: "0.10",
    protocol: "x402",
    affiliate: { pyrimidEligible: false },
    source: "preloaded",
  },
];

function defaultConfig({ walletAddress, mode = "hybrid", micEnabled = false, existing = {} }) {
  return {
    version: CONFIG_VERSION,
    mode,
    walletAddress,
    chain: "base",
    token: "USDC",
    forgemeshVoiceBaseUrl: existing.forgemeshVoiceBaseUrl || paths.DEFAULT_BASE_URL,
    hostedVoice: {
      tier: existing.hostedVoice?.tier || "base",
      voice: existing.hostedVoice?.voice || "M1",
      language: existing.hostedVoice?.language || existing.hostedVoice?.lang || "en",
      preset: existing.hostedVoice?.preset || null,
      mix: existing.hostedVoice?.mix || null,
      expression: existing.hostedVoice?.expression || null,
      expressionLevel: existing.hostedVoice?.expressionLevel ?? null,
      expressionControls: existing.hostedVoice?.expressionControls || existing.hostedVoice?.knobs || {},
    },
    localVoice: {
      engine: "supertonic",
      version: "1.3.1",
      installDir: paths.VOICE_DIR,
      model: "Supertone/supertonic-3",
      voice: existing.localVoice?.voice || existing.hostedVoice?.voice || "M1",
      language: existing.localVoice?.language || existing.hostedVoice?.language || existing.hostedVoice?.lang || "en",
      preset: existing.localVoice?.preset || existing.hostedVoice?.preset || null,
      mix: existing.localVoice?.mix || existing.hostedVoice?.mix || null,
      expression: existing.localVoice?.expression || existing.hostedVoice?.expression || null,
      expressionLevel: existing.localVoice?.expressionLevel ?? existing.hostedVoice?.expressionLevel ?? null,
      expressionControls: existing.localVoice?.expressionControls || existing.hostedVoice?.expressionControls || existing.localVoice?.knobs || existing.hostedVoice?.knobs || {},
      serverUrl: existing.localVoice?.serverUrl || paths.DEFAULT_LOCAL_SERVER_URL,
    },
    mic: {
      enabled: micEnabled,
      note: "When true, FFmpeg + local Whisper may be installed for future speech-to-text (talk to your agent).",
    },
    conversation: {
      status: "push_to_talk",
      agentCommand: existing.conversation?.agentCommand || null,
      whisperModel: existing.conversation?.whisperModel || "base",
      pushToTalk: true,
      wakeWord: { status: "coming_soon" },
      alwaysOn: { status: "coming_soon" },
      note: "listen records until Enter and transcribes locally; talk loops listen -> agentCommand -> speak with sessionCapUsd enforced.",
    },
    x402Policy: {
      forgemeshFeeUsd: existing.x402Policy?.forgemeshFeeUsd || "0.005",
      perCallCapUsd: existing.x402Policy?.perCallCapUsd || "0.05",
      dailyCapUsd: existing.x402Policy?.dailyCapUsd || "0.25",
      sessionCapUsd: existing.x402Policy?.sessionCapUsd || "0.10",
      requireApproval: existing.x402Policy?.requireApproval ?? true,
    },
    discovery: {
      agentCashCompatible: true,
      ponchoReady: true,
      openApiRequired: true,
      agentCashMode: "external_discovery",
      preloadedForgeMeshProducts: true,
    },
    products: {
      preloaded: existing.products?.preloaded || PRELOADED_FORGEMESH_PRODUCTS,
      discoveryOrder: ["preloaded", "agentcash"],
      note: "Use preloaded ForgeMesh products first; use AgentCash/X402Scan discovery to find or validate broader x402 servers.",
    },
    affiliate: {
      pyrimid: {
        status: "aware_not_default",
        defaultAffiliateId: existing.affiliate?.pyrimid?.defaultAffiliateId || null,
        note: "Pyrimid is for affiliate attribution on supported products. Direct x402 remains the default payment path.",
      },
    },
  };
}

function migrate(cfg) {
  if (cfg.version >= CONFIG_VERSION) return cfg;
  const migrated = defaultConfig({
    walletAddress: cfg.walletAddress,
    mode: cfg.mode || "hybrid",
    micEnabled: cfg.mic?.enabled ?? false,
    existing: cfg,
  });
  writePrivateJson(paths.CONFIG_PATH, migrated);
  return migrated;
}

function loadConfig() {
  if (!fs.existsSync(paths.CONFIG_PATH)) return null;
  return migrate(readJson(paths.CONFIG_PATH));
}

function saveConfig(cfg) {
  writePrivateJson(paths.CONFIG_PATH, cfg);
}

function requireConfig() {
  const cfg = loadConfig();
  if (!cfg) {
    console.error("Not set up yet. Run: x402-agent-voice init");
    process.exit(1);
  }
  return cfg;
}

module.exports = {
  CONFIG_VERSION,
  MODES,
  PRELOADED_FORGEMESH_PRODUCTS,
  defaultConfig,
  loadConfig,
  saveConfig,
  requireConfig,
};
