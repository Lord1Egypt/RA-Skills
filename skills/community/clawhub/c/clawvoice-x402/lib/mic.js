"use strict";

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
const paths = require("./paths");
const { ensureDir } = require("./fsutil");
const { askYesNo, isInteractive } = require("./prompt");
const { findPython } = require("./python");

function commandExists(bin) {
  return spawnSync("which", [bin], { stdio: "ignore" }).status === 0;
}

function whisperInstalled() {
  const python = path.join(paths.VOICE_DIR, ".venv", "bin", "python");
  if (!fs.existsSync(python)) return false;
  return spawnSync(python, ["-c", "import faster_whisper"], { stdio: "ignore" }).status === 0;
}

function micStatus() {
  return { ffmpeg: commandExists("ffmpeg"), whisper: whisperInstalled() };
}

function ffmpegInstallHint() {
  if (process.platform === "darwin") return "brew install ffmpeg";
  return "sudo apt-get install ffmpeg   (or your distro's package manager)";
}

function venvPython() {
  return path.join(paths.VOICE_DIR, ".venv", "bin", "python");
}

function runStep(cmd, args) {
  console.log(`Running: ${[cmd, ...args].join(" ")}`);
  const result = spawnSync(cmd, args, { stdio: "inherit" });
  if (result.status !== 0) {
    console.error(`Command failed: ${cmd}`);
    process.exit(result.status || 1);
  }
}

async function ensureMicVenv({ dryRun, yes }) {
  const python = venvPython();
  if (fs.existsSync(python)) return python;

  if (dryRun) {
    console.log("Would create the local speech-to-text Python runtime:");
    console.log(`Would run: python3.12/python3.11/python3.10/python3.9 (or X402_VOICE_PYTHON) -m venv ${path.join(paths.VOICE_DIR, ".venv")}`);
    console.log(`Would run: ${python} -m pip install --upgrade pip`);
    return python;
  }

  const basePython = findPython();
  if (!basePython) process.exit(1);

  const steps = [
    [basePython, ["-m", "venv", path.join(paths.VOICE_DIR, ".venv")]],
    [python, ["-m", "pip", "install", "--upgrade", "pip"]],
  ];

  let approved = yes;
  if (!approved && isInteractive()) {
    approved = await askYesNo(
      "Create a local Python venv and download faster-whisper for private speech-to-text?",
      false,
    );
  }
  if (!approved) {
    console.log("Mic install needs permission to create a local venv and download Python packages.");
    console.log("Run again with: x402-agent-voice install-mic --yes");
    process.exit(1);
  }

  ensureDir(paths.VOICE_DIR);
  for (const [cmd, args] of steps) runStep(cmd, args);
  return python;
}

// Installs the optional speech-to-text stack for future "talk to your agent" support.
// Detects FFmpeg and prints an install instruction rather than running a system package manager.
async function installMic(config, { dryRun, yes }) {
  if (!config.mic?.enabled) {
    console.log('Mic support is disabled. Enable it by setting "mic.enabled": true in ~/.x402-agent-voice/config.json');
    console.log("or rerun: x402-agent-voice init");
    return;
  }

  const status = micStatus();
  if (!status.ffmpeg) {
    console.log(`FFmpeg not found. Install it with: ${ffmpegInstallHint()}`);
  }

  if (status.whisper) {
    console.log("Local Whisper (faster-whisper) already installed.");
    return;
  }

  const python = await ensureMicVenv({ dryRun, yes });
  const model = config.conversation?.whisperModel || "base";
  const args = ["-m", "pip", "install", "faster-whisper"];
  const preloadSnippet = `from faster_whisper import WhisperModel; WhisperModel("${model}", device="cpu", compute_type="int8")`;
  if (dryRun) {
    console.log(`Would run: ${[python, ...args].join(" ")}`);
    console.log(`Would predownload whisper model "${model}"`);
    return;
  }
  console.log(`Running: ${[python, ...args].join(" ")}`);
  const result = spawnSync(python, args, { stdio: "inherit" });
  if (result.status !== 0) {
    console.error("faster-whisper install failed.");
    process.exit(result.status || 1);
  }

  console.log(`Downloading whisper model "${model}" (one-time)...`);
  const preload = spawnSync(python, ["-c", preloadSnippet], { stdio: "inherit", timeout: 600000 });
  if (preload.status !== 0) {
    console.log("Model predownload failed — it will download automatically on first listen.");
  }
  console.log("Mic ready. Try: x402-agent-voice listen   or   x402-agent-voice talk");
}

module.exports = { micStatus, installMic, commandExists };
