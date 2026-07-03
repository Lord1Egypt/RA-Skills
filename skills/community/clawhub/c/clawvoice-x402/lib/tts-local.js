"use strict";

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
const paths = require("./paths");

function supertonicBin() {
  return path.join(paths.VENV_BIN, "supertonic");
}

function cliInstalled() {
  return fs.existsSync(supertonicBin());
}

async function serverHealthy(serverUrl) {
  try {
    const res = await fetch(serverUrl + "/v1/tts", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ text: "ping", lang: "en", voice: "M1" }),
      signal: AbortSignal.timeout(10000),
    });
    return res.ok;
  } catch (_) {
    return false;
  }
}

async function synthViaServer(serverUrl, text, outPath, { voice, language, preset, mix, expression, expressionLevel, expressionControls } = {}) {
  const body = { text, lang: language || "en", voice: voice || "M1", response_format: "wav" };
  if (preset) body.preset = preset;
  if (mix) body.mix = mix;
  if (expression) body.expression = expression;
  if (expressionLevel != null) body.expressionLevel = expressionLevel;
  if (expressionControls && Object.keys(expressionControls).length) body.knobs = expressionControls;
  const res = await fetch(serverUrl + "/v1/tts", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(60000),
  });
  if (!res.ok) throw new Error(`local voice server returned ${res.status}`);
  fs.writeFileSync(outPath, Buffer.from(await res.arrayBuffer()));
}

function synthViaCli(text, outPath) {
  const result = spawnSync(supertonicBin(), ["synth", "--text", text, "--out", outPath], {
    stdio: ["ignore", "ignore", "pipe"],
  });
  if (result.status !== 0) {
    const stderr = result.stderr ? result.stderr.toString().trim().slice(0, 300) : "";
    throw new Error(`supertonic CLI failed${stderr ? `: ${stderr}` : ""}`);
  }
  if (!fs.existsSync(outPath)) throw new Error("supertonic CLI produced no output file");
}

// Returns { ok, engine: "local", error? }. Never throws.
async function localSpeak(config, text, outPath) {
  const serverUrl = config.localVoice?.serverUrl || paths.DEFAULT_LOCAL_SERVER_URL;
  try {
    if (await serverHealthy(serverUrl)) {
      await synthViaServer(serverUrl, text, outPath, {
        voice: config.localVoice?.voice || config.hostedVoice?.voice,
        language: config.localVoice?.language || config.hostedVoice?.language,
        preset: config.localVoice?.preset || config.hostedVoice?.preset,
        mix: config.localVoice?.mix || config.hostedVoice?.mix,
        expression: config.localVoice?.expression || config.hostedVoice?.expression,
        expressionLevel: config.localVoice?.expressionLevel ?? config.hostedVoice?.expressionLevel,
        expressionControls: config.localVoice?.expressionControls || config.hostedVoice?.expressionControls,
      });
      return { ok: true, engine: "local-server" };
    }
    if (cliInstalled()) {
      synthViaCli(text, outPath);
      return { ok: true, engine: "local-cli" };
    }
    return { ok: false, engine: "local", error: "local voice not installed (run: x402-agent-voice install-voice)" };
  } catch (err) {
    return { ok: false, engine: "local", error: err.message };
  }
}

module.exports = { localSpeak, serverHealthy, cliInstalled, supertonicBin };
