"use strict";

const { spawnSync } = require("child_process");

// onnxruntime (Supertonic) and faster-whisper only ship wheels for CPython 3.9-3.12.
const MIN_MINOR = 9;
const MAX_MINOR = 12;
const CANDIDATE_BINS = ["python3.12", "python3.11", "python3.10", "python3.9", "python3"];

function formatRange() {
  return `Python 3.${MIN_MINOR}-3.${MAX_MINOR}`;
}

function formatVersion(v) {
  return v ? `Python ${v.major}.${v.minor}` : "not runnable";
}

function versionOf(bin, env = process.env) {
  const result = spawnSync(bin, ["-c", "import sys; print('%d.%d' % sys.version_info[:2])"], {
    encoding: "utf8",
    env,
  });
  if (result.status !== 0 || !result.stdout) return null;
  const [major, minor] = result.stdout.trim().split(".").map(Number);
  if (!Number.isInteger(major) || !Number.isInteger(minor)) return null;
  return { major, minor };
}

function compatible(v) {
  return v !== null && v.major === 3 && v.minor >= MIN_MINOR && v.minor <= MAX_MINOR;
}

function probePython({ env = process.env, candidates = CANDIDATE_BINS } = {}) {
  const override = env.X402_VOICE_PYTHON;
  if (override) {
    const version = versionOf(override, env);
    return {
      selected: compatible(version) ? override : null,
      override: { bin: override, version, compatible: compatible(version) },
      candidates: [],
    };
  }

  const checked = [];
  for (const bin of candidates) {
    const version = versionOf(bin, env);
    const ok = compatible(version);
    checked.push({ bin, version, compatible: ok });
    if (ok) return { selected: bin, override: null, candidates: checked };
  }
  return { selected: null, override: null, candidates: checked };
}

// Returns the first Python binary usable for the voice venv, or null (after
// printing guidance). X402_VOICE_PYTHON overrides probing.
function findPython(options = {}) {
  const log = options.log || console.error;
  const probe = probePython(options);
  if (probe.selected) return probe.selected;

  if (probe.override) {
    log(
      `X402_VOICE_PYTHON=${probe.override.bin} is ${formatVersion(probe.override.version)}; ` +
        `need ${formatRange()}.`,
    );
    return null;
  }

  const runnable = probe.candidates.filter((candidate) => candidate.version);
  if (runnable.length) {
    const seen = runnable.map((candidate) => `${candidate.bin}=${formatVersion(candidate.version)}`).join(", ");
    log(
      `No compatible Python found (${seen}). The local voice runtime needs ` +
        `${formatRange()} (onnxruntime has no wheels for newer versions).`,
    );
  } else {
    log("No compatible Python executable found.");
  }
  log("Install Python 3.12 (brew install python@3.12, pyenv install 3.12, or the python.org installer),");
  log("or set X402_VOICE_PYTHON to a compatible interpreter, then rerun this command.");
  return null;
}

module.exports = { CANDIDATE_BINS, compatible, findPython, formatVersion, probePython, versionOf };
