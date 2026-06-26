#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const envPath = path.join(__dirname, "..", "assets", "config-template.env");

function loadEnvFile(filePath) {
  if (!fs.existsSync(filePath)) {
    return;
  }
  const content = fs.readFileSync(filePath, "utf8");
  for (const line of content.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) {
      continue;
    }
    const idx = trimmed.indexOf("=");
    if (idx === -1) {
      continue;
    }
    const key = trimmed.slice(0, idx);
    const value = trimmed.slice(idx + 1);
    if (!(key in process.env)) {
      process.env[key] = value;
    }
  }
}

async function toBlobFromInput(input) {
  if (/^https?:\/\//i.test(input)) {
    const res = await fetch(input);
    if (!res.ok) {
      throw new Error(`audio_download_failed:${res.status}`);
    }
    const arrayBuffer = await res.arrayBuffer();
    const contentType = res.headers.get("content-type") || "audio/mpeg";
    return new Blob([Buffer.from(arrayBuffer)], { type: contentType });
  }

  const filePath = path.resolve(input);
  if (!fs.existsSync(filePath)) {
    throw new Error(`audio_file_not_found:${filePath}`);
  }
  const buffer = fs.readFileSync(filePath);
  const ext = path.extname(filePath).toLowerCase();
  const mimeByExt = {
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/mp4",
    ".aac": "audio/aac",
    ".ogg": "audio/ogg",
    ".opus": "audio/ogg",
    ".flac": "audio/flac"
  };
  return new Blob([buffer], { type: mimeByExt[ext] || "application/octet-stream" });
}

async function main() {
  loadEnvFile(envPath);

  const audioInput = process.argv[2];
  const languageHint = process.argv[3] || "auto";
  const promptHint = process.argv[4] || "";

  if (!audioInput) {
    console.error(
      "Usage: node skills/claw-go/scripts/transcribe_audio.js <audioPathOrUrl> [languageHint] [promptHint]"
    );
    process.exit(1);
  }

  const apiBase = process.env.CLAWGO_STT_API_BASE || "https://api.siliconflow.cn/v1/audio/transcriptions";
  const apiKey = process.env.CLAWGO_STT_API_KEY || process.env.CLAWGO_TTS_API_KEY;
  const model = process.env.CLAWGO_STT_MODEL || "FunAudioLLM/SenseVoiceSmall";

  if (!apiKey || apiKey.startsWith("replace-with-")) {
    throw new Error("missing_stt_api_key");
  }

  const form = new FormData();
  const blob = await toBlobFromInput(audioInput);
  const filename = /^https?:\/\//i.test(audioInput) ? "voice-message.mp3" : path.basename(audioInput);
  form.set("file", blob, filename);
  form.set("model", model);
  if (languageHint && languageHint !== "auto") {
    form.set("language", languageHint);
  }
  if (promptHint) {
    form.set("prompt", promptHint);
  }

  const res = await fetch(apiBase, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`
    },
    body: form
  });

  const text = await res.text();
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${text}`);
  }

  const data = JSON.parse(text);
  const transcript = String(data.text || "").trim();
  process.stdout.write(
    JSON.stringify(
      {
        transcript,
        language_hint: languageHint,
        model,
        source: audioInput
      },
      null,
      2
    ) + "\n"
  );
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
