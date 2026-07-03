"use strict";

const os = require("os");
const path = require("path");

const APP_DIR = path.join(os.homedir(), ".x402-agent-voice");
const VOICE_DIR = path.join(APP_DIR, "voice");

module.exports = {
  APP_DIR,
  VOICE_DIR,
  CONFIG_PATH: path.join(APP_DIR, "config.json"),
  WALLET_PATH: path.join(APP_DIR, "wallet.json"),
  SPEND_LOG_PATH: path.join(APP_DIR, "spend.jsonl"),
  PLAYBACK_STATE_PATH: path.join(APP_DIR, "playback.json"),
  AUDIO_DIR: path.join(APP_DIR, "audio"),
  SERVER_PID_PATH: path.join(VOICE_DIR, "server.pid"),
  VENV_BIN: path.join(VOICE_DIR, ".venv", "bin"),
  DEFAULT_BASE_URL: "https://voice.forgemesh.io",
  DEFAULT_LOCAL_SERVER_URL: "http://127.0.0.1:7788",
};
