"use strict";

const fs = require("fs");
const { spawn, spawnSync } = require("child_process");
const paths = require("./paths");
const { ensureDir } = require("./fsutil");

function findPlayer() {
  for (const player of [
    ["afplay", []],
    ["paplay", []],
    ["aplay", ["-q"]],
    ["ffplay", ["-nodisp", "-autoexit", "-loglevel", "quiet"]],
  ]) {
    const probe = spawnSync("which", [player[0]], { stdio: "ignore" });
    if (probe.status === 0) return player;
  }
  return null;
}

function readState() {
  try {
    return JSON.parse(fs.readFileSync(paths.PLAYBACK_STATE_PATH, "utf8"));
  } catch (_) {
    return null;
  }
}

function writeState(state) {
  ensureDir(paths.APP_DIR);
  fs.writeFileSync(paths.PLAYBACK_STATE_PATH, JSON.stringify(state, null, 2), { mode: 0o600 });
}

function clearState() {
  try {
    fs.unlinkSync(paths.PLAYBACK_STATE_PATH);
  } catch (_) {}
}

function pidAlive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch (_) {
    return false;
  }
}

function stopPlayback({ quiet } = {}) {
  const state = readState();
  if (!state || !pidAlive(state.pid)) {
    clearState();
    if (!quiet) console.log("No ClawVoice playback is running.");
    return false;
  }

  try {
    process.kill(state.pid, "SIGTERM");
  } catch (_) {
    clearState();
    if (!quiet) console.log("No ClawVoice playback is running.");
    return false;
  }

  clearState();
  if (!quiet) console.log(`Stopped ClawVoice playback (${state.bin}, pid ${state.pid}).`);
  return true;
}

function playFile(file) {
  const player = findPlayer();
  if (!player) return false;
  stopPlayback({ quiet: true });

  const [bin, args] = player;
  const child = spawn(bin, [...args, file], {
    detached: true,
    stdio: "ignore",
  });
  child.unref();
  writeState({ pid: child.pid, bin, file, startedAt: new Date().toISOString() });
  return true;
}

module.exports = { findPlayer, playFile, stopPlayback };
