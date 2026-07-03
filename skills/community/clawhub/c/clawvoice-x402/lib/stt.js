"use strict";

const fs = require("fs");
const path = require("path");
const readline = require("readline");
const { spawn, spawnSync } = require("child_process");
const paths = require("./paths");
const { ensureDir } = require("./fsutil");
const { commandExists } = require("./mic");

const TRANSCRIBE_SCRIPT = path.join(__dirname, "..", "scripts", "transcribe.py");

function venvPython() {
  return path.join(paths.VOICE_DIR, ".venv", "bin", "python");
}

function requireSttDeps() {
  if (!commandExists("ffmpeg")) {
    console.error("FFmpeg not found — needed to record from the microphone.");
    console.error(process.platform === "darwin" ? "Install: brew install ffmpeg" : "Install: sudo apt-get install ffmpeg");
    process.exit(1);
  }
  if (!fs.existsSync(venvPython())) {
    console.error("Speech-to-text not installed. Run: x402-agent-voice install-mic");
    process.exit(1);
  }
}

function micInputArgs() {
  if (process.platform === "darwin") return ["-f", "avfoundation", "-i", ":0"];
  if (process.platform === "linux") {
    if (spawnSync("which", ["pactl"], { stdio: "ignore" }).status === 0) return ["-f", "pulse", "-i", "default"];
    return ["-f", "alsa", "-i", "default"];
  }
  console.error("Microphone recording is not supported on this platform yet. Use: listen --file <audio.wav>");
  process.exit(1);
}

// 16kHz mono PCM — what whisper expects.
const WAV_ARGS = ["-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", "-y"];

function recordSeconds(outPath, seconds) {
  const args = ["-hide_banner", "-loglevel", "error", ...micInputArgs(), "-t", String(seconds), ...WAV_ARGS, outPath];
  const result = spawnSync("ffmpeg", args, { stdio: ["ignore", "ignore", "pipe"] });
  if (result.status !== 0) {
    throw new Error(`recording failed: ${(result.stderr || "").toString().trim().slice(0, 200)}`);
  }
}

// Push-to-talk: records until the user presses Enter.
function recordPushToTalk(outPath) {
  return new Promise((resolve, reject) => {
    const args = ["-hide_banner", "-loglevel", "error", ...micInputArgs(), ...WAV_ARGS, outPath];
    const child = spawn("ffmpeg", args, { stdio: ["pipe", "ignore", "pipe"] });
    let stderr = "";
    child.stderr.on("data", (d) => (stderr += d));

    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    console.log("● Recording — press Enter when you're done talking.");
    rl.once("line", () => {
      rl.close();
      child.stdin.write("q"); // ffmpeg finalizes the file cleanly on "q"
    });

    child.on("close", (code) => {
      if (fs.existsSync(outPath) && fs.statSync(outPath).size > 44) resolve();
      else reject(new Error(`recording failed (exit ${code}): ${stderr.trim().slice(0, 200)}`));
    });
    child.on("error", reject);
  });
}

function transcribe(wavPath, model) {
  const result = spawnSync(venvPython(), [TRANSCRIBE_SCRIPT, wavPath, model || "base"], {
    stdio: ["ignore", "pipe", "inherit"], // stderr shows first-run model download progress
    timeout: 300000,
  });
  if (result.status !== 0 && !result.stdout) {
    throw new Error("transcription failed (see output above)");
  }
  const parsed = JSON.parse(result.stdout.toString().trim().split("\n").pop());
  if (parsed.error) throw new Error(parsed.error);
  return parsed;
}

// Returns { text, language, durationS, audioPath }. Options: file, seconds, model, keep.
async function listen({ file, seconds, model, keep } = {}) {
  const cfgModel = model || "base";
  let wavPath = file;
  let temporary = false;

  if (!wavPath) {
    requireSttDeps();
    ensureDir(paths.AUDIO_DIR);
    wavPath = path.join(paths.AUDIO_DIR, `mic-${Date.now()}.wav`);
    temporary = !keep;
    if (seconds) recordSeconds(wavPath, seconds);
    else await recordPushToTalk(wavPath);
  } else if (!fs.existsSync(wavPath)) {
    throw new Error(`audio file not found: ${wavPath}`);
  }

  try {
    const result = transcribe(wavPath, cfgModel);
    return { ...result, audioPath: temporary ? null : wavPath };
  } finally {
    if (temporary) {
      try {
        fs.unlinkSync(wavPath);
      } catch (_) {}
    }
  }
}

module.exports = { listen, transcribe, requireSttDeps };
