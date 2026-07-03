"use strict";

const fs = require("fs");
const path = require("path");
const paths = require("./paths");
const { ensureDir } = require("./fsutil");
const { requireConfig } = require("./config");
const { localSpeak } = require("./tts-local");
const { hostedSpeak } = require("./tts-hosted");
const { isInteractive, askYesNo } = require("./prompt");
const { playFile } = require("./playback");

// Options: out, play, approve, soft (return null instead of exiting on failure),
// noHosted (skip the paid hosted fallback, e.g. when a session spend cap is hit).
async function speak(text, { out, play, approve, soft, noHosted } = {}) {
  const config = requireConfig();
  if (!text || !text.trim()) {
    console.error('Nothing to say. Usage: x402-agent-voice speak "hello world"');
    if (soft) return null;
    process.exit(1);
  }

  ensureDir(paths.AUDIO_DIR);
  const outPath = out || path.join(paths.AUDIO_DIR, `say-${Date.now()}.wav`);

  const confirm = approve
    ? async () => true
    : isInteractive()
      ? (amountUsd, url) => askYesNo(`Pay $${amountUsd} USDC for hosted voice (${url})?`, false)
      : null;

  const attempts = [];
  let result = null;

  if (config.mode === "local" || config.mode === "hybrid") {
    result = await localSpeak(config, text, outPath);
    if (!result.ok) attempts.push(`local: ${result.error}`);
  }
  if ((!result || !result.ok) && !noHosted && (config.mode === "hosted" || config.mode === "hybrid")) {
    result = await hostedSpeak(config, text, outPath, { confirm });
    if (!result.ok) attempts.push(`hosted: ${result.error}`);
  }

  if (!result || !result.ok) {
    console.error("Could not speak:");
    for (const a of attempts) console.error(`  - ${a}`);
    if (soft) return null;
    process.exit(1);
  }

  const paid = result.amountUsd ? ` (paid $${result.amountUsd} USDC)` : "";
  console.log(`Spoke via ${result.engine}${paid}: ${outPath}`);

  if (play !== false && !out) {
    if (!playFile(outPath)) {
      console.log("No audio player found on this machine; audio saved to the path above.");
    }
  }
  return outPath;
}

module.exports = { speak, playFile };
