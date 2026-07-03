"use strict";

const fs = require("fs");
const path = require("path");
const { spawn, spawnSync } = require("child_process");
const paths = require("./paths");
const { ensureDir } = require("./fsutil");
const { supertonicBin, serverHealthy } = require("./tts-local");
const { findPython } = require("./python");

function guardPosix() {
  if (process.platform === "win32") {
    console.error("install-voice currently supports macOS and Linux only. Use hosted mode on Windows.");
    process.exit(1);
  }
}

function venvPython() {
  return path.join(paths.VOICE_DIR, ".venv", "bin", "python");
}

function installVoice({ dryRun }) {
  guardPosix();
  ensureDir(paths.VOICE_DIR);
  const basePython = dryRun ? "python3.12/python3.11/python3.10/python3.9 (or X402_VOICE_PYTHON)" : findPython();
  if (!basePython) return false;
  const commands = [
    [basePython, ["-m", "venv", path.join(paths.VOICE_DIR, ".venv")]],
    [venvPython(), ["-m", "pip", "install", "--upgrade", "pip"]],
    [venvPython(), ["-m", "pip", "install", "supertonic==1.3.1"]],
  ];

  if (dryRun) {
    console.log("Would run:");
    for (const [cmd, args] of commands) console.log([cmd, ...args].join(" "));
    console.log("Model files are downloaded by Supertonic on first use.");
    return true;
  }

  for (const [cmd, args] of commands) {
    console.log(`Running: ${[cmd, ...args].join(" ")}`);
    const result = spawnSync(cmd, args, { stdio: "inherit" });
    if (result.status !== 0) {
      console.error(`Command failed: ${cmd}`);
      return false;
    }
  }
  console.log("Local voice runtime installed.");
  return true;
}

function readPid() {
  try {
    const pid = parseInt(fs.readFileSync(paths.SERVER_PID_PATH, "utf8").trim(), 10);
    if (!Number.isInteger(pid)) return null;
    process.kill(pid, 0);
    return pid;
  } catch (_) {
    return null;
  }
}

async function serveStart(config) {
  guardPosix();
  if (!fs.existsSync(supertonicBin())) {
    console.error("Local voice not installed. Run: x402-agent-voice install-voice");
    process.exit(1);
  }
  const serverUrl = config.localVoice?.serverUrl || paths.DEFAULT_LOCAL_SERVER_URL;
  if (await serverHealthy(serverUrl)) {
    console.log(`Local voice server already running at ${serverUrl}`);
    return;
  }
  const { hostname, port } = new URL(serverUrl);
  const child = spawn(supertonicBin(), ["serve", "--host", hostname, "--port", port || "7788"], {
    detached: true,
    stdio: "ignore",
  });
  child.unref();
  ensureDir(paths.VOICE_DIR);
  fs.writeFileSync(paths.SERVER_PID_PATH, String(child.pid) + "\n", { mode: 0o600 });
  console.log(`Local voice server starting at ${serverUrl} (pid ${child.pid})`);
}

function serveStop() {
  const pid = readPid();
  if (!pid) {
    console.log("Local voice server is not running.");
    return;
  }
  process.kill(pid);
  try {
    fs.unlinkSync(paths.SERVER_PID_PATH);
  } catch (_) {}
  console.log(`Stopped local voice server (pid ${pid}).`);
}

module.exports = { installVoice, serveStart, serveStop, readPid };
