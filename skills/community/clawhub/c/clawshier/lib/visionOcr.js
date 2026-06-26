const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync, spawnSync } = require("child_process");
const OpenAI = require("openai");

const OCR_PROMPT = "Extract ALL visible text from this receipt or invoice image. Reproduce the text exactly as it appears, preserving line breaks. If this is not a receipt or invoice, respond with exactly: NOT_A_RECEIPT";
const VALID_PROVIDERS = new Set(["auto", "openai", "ollama"]);

function parsePositiveInt(value, fallback) {
  const parsed = parseInt(value, 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function getVisionConfig(env = process.env) {
  const provider = String(env.CLAWSHIER_VISION_PROVIDER || "openai").trim().toLowerCase();
  if (!VALID_PROVIDERS.has(provider)) {
    throw new Error(
      `Invalid CLAWSHIER_VISION_PROVIDER: "${provider}". Expected one of: auto, openai, ollama.`
    );
  }

  return {
    provider,
    openaiModel: String(env.OPENAI_MODEL || "gpt-4o").trim(),
    ollamaModel: String(env.CLAWSHIER_OLLAMA_MODEL || "llama3.2-vision:latest").trim(),
    ollamaHost: String(env.CLAWSHIER_OLLAMA_HOST || "http://127.0.0.1:11434").trim().replace(/\/$/, ""),
    ollamaMaxDimension: parsePositiveInt(env.CLAWSHIER_OLLAMA_MAX_DIMENSION, 1024),
  };
}

function getMimeType(imagePath) {
  const ext = String(imagePath).split(".").pop().toLowerCase();
  const mimeTypes = {
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    png: "image/png",
    webp: "image/webp",
    gif: "image/gif",
  };
  return mimeTypes[ext] || "image/jpeg";
}

function getImageBase64(imagePath) {
  return fs.readFileSync(imagePath).toString("base64");
}

function assertValidOcrText(ocrText) {
  const text = String(ocrText || "").trim();
  const lowered = text.toLowerCase();

  if (!text) {
    throw new Error("OCR did not return any text");
  }

  if (text === "NOT_A_RECEIPT") {
    throw new Error("Image does not appear to be a receipt or invoice");
  }

  const refusalPatterns = [
    "i'm sorry",
    "i cannot assist",
    "i can't assist",
    "i'm unable to",
    "unable to transcribe",
    "cannot transcribe",
    "can't transcribe",
    "cannot help with that",
    "can't help with that",
  ];

  if (refusalPatterns.some((pattern) => lowered.includes(pattern))) {
    throw new Error("OCR returned a refusal instead of receipt text");
  }

  return text;
}

function canUseSips() {
  if (process.platform !== "darwin") return false;
  const result = spawnSync("which", ["sips"], { stdio: "ignore" });
  return result.status === 0;
}

function prepareOllamaImage(imagePath, { maxDimension = 1024 } = {}) {
  if (!maxDimension || !canUseSips()) {
    return { imagePath, cleanup: () => {} };
  }

  const tempPath = path.join(os.tmpdir(), `clawshier-ollama-${process.pid}-${Date.now()}.jpg`);

  try {
    execFileSync("sips", ["-Z", String(maxDimension), imagePath, "--out", tempPath], { stdio: "ignore" });
    return {
      imagePath: tempPath,
      cleanup: () => {
        try {
          fs.unlinkSync(tempPath);
        } catch (_) {}
      },
    };
  } catch (_) {
    return { imagePath, cleanup: () => {} };
  }
}

async function ocrWithOpenAI({ imagePath, apiKey, model }) {
  if (!apiKey) {
    throw new Error("OPENAI_API_KEY is required for OpenAI OCR");
  }

  const base64 = getImageBase64(imagePath);
  const mime = getMimeType(imagePath);
  const openai = new OpenAI({ apiKey });

  const response = await openai.chat.completions.create({
    model,
    messages: [
      {
        role: "user",
        content: [
          { type: "text", text: OCR_PROMPT },
          {
            type: "image_url",
            image_url: { url: `data:${mime};base64,${base64}` },
          },
        ],
      },
    ],
    max_tokens: 2048,
  });

  return assertValidOcrText(response.choices?.[0]?.message?.content);
}

async function ocrWithOllama({ imagePath, host, model, fetchImpl = global.fetch, maxDimension = 1024 }) {
  if (typeof fetchImpl !== "function") {
    throw new Error("fetch is required for Ollama OCR");
  }

  const prepared = prepareOllamaImage(imagePath, { maxDimension });

  try {
    const base64 = getImageBase64(prepared.imagePath);
    const response = await fetchImpl(`${host}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model,
        messages: [
          {
            role: "user",
            content: OCR_PROMPT,
            images: [base64],
          },
        ],
        stream: false,
      }),
    });

    if (!response.ok) {
      throw new Error(`Ollama OCR request failed: ${response.status} ${response.statusText} ${await response.text()}`.trim());
    }

    const data = await response.json();
    return assertValidOcrText(data?.message?.content || data?.response);
  } finally {
    prepared.cleanup();
  }
}

async function runOcrWithProvider({
  imagePath,
  env = process.env,
  openaiOcr = ocrWithOpenAI,
  ollamaOcr = ocrWithOllama,
  fetchImpl = global.fetch,
}) {
  const config = getVisionConfig(env);
  const openaiArgs = {
    imagePath,
    apiKey: env.OPENAI_API_KEY,
    model: config.openaiModel,
  };
  const ollamaArgs = {
    imagePath,
    host: config.ollamaHost,
    model: config.ollamaModel,
    maxDimension: config.ollamaMaxDimension,
    fetchImpl,
  };

  if (config.provider === "openai") {
    return openaiOcr(openaiArgs);
  }

  if (config.provider === "ollama") {
    return ollamaOcr(ollamaArgs);
  }

  try {
    return await ollamaOcr(ollamaArgs);
  } catch (ollamaError) {
    try {
      return await openaiOcr(openaiArgs);
    } catch (openaiError) {
      throw new Error(
        `Auto OCR fallback failed. Ollama error: ${ollamaError.message}. OpenAI error: ${openaiError.message}`
      );
    }
  }
}

module.exports = {
  OCR_PROMPT,
  parsePositiveInt,
  getVisionConfig,
  getMimeType,
  getImageBase64,
  assertValidOcrText,
  canUseSips,
  prepareOllamaImage,
  ocrWithOpenAI,
  ocrWithOllama,
  runOcrWithProvider,
};
