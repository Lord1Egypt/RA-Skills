const test = require("node:test");
const assert = require("node:assert/strict");

const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

const {
  getVisionConfig,
  assertValidOcrText,
  ocrWithOllama,
  runOcrWithProvider,
} = require("../lib/visionOcr");

test("getVisionConfig defaults to openai with ollama defaults", () => {
  const config = getVisionConfig({ OPENAI_MODEL: "gpt-4o-mini" });

  assert.equal(config.provider, "openai");
  assert.equal(config.openaiModel, "gpt-4o-mini");
  assert.equal(config.ollamaModel, "llama3.2-vision:latest");
  assert.equal(config.ollamaHost, "http://127.0.0.1:11434");
  assert.equal(config.ollamaMaxDimension, 1024);
});

test("getVisionConfig rejects unknown providers", () => {
  assert.throws(
    () => getVisionConfig({ CLAWSHIER_VISION_PROVIDER: "banana" }),
    /Invalid CLAWSHIER_VISION_PROVIDER/
  );
});

test("assertValidOcrText rejects NOT_A_RECEIPT", () => {
  assert.throws(() => assertValidOcrText("NOT_A_RECEIPT"), /does not appear to be a receipt/);
});

test("runOcrWithProvider uses OpenAI when explicitly selected", async () => {
  const calls = [];
  const result = await runOcrWithProvider({
    imagePath: "/tmp/fake.png",
    env: { CLAWSHIER_VISION_PROVIDER: "openai", OPENAI_API_KEY: "key" },
    openaiOcr: async (args) => {
      calls.push(["openai", args]);
      return "OPENAI OCR";
    },
    ollamaOcr: async () => {
      throw new Error("should not be called");
    },
  });

  assert.equal(result, "OPENAI OCR");
  assert.equal(calls.length, 1);
  assert.equal(calls[0][0], "openai");
});

test("runOcrWithProvider uses Ollama when explicitly selected", async () => {
  const calls = [];
  const result = await runOcrWithProvider({
    imagePath: "/tmp/fake.png",
    env: { CLAWSHIER_VISION_PROVIDER: "ollama" },
    openaiOcr: async () => {
      throw new Error("should not be called");
    },
    ollamaOcr: async (args) => {
      calls.push(["ollama", args]);
      return "OLLAMA OCR";
    },
  });

  assert.equal(result, "OLLAMA OCR");
  assert.equal(calls.length, 1);
  assert.equal(calls[0][0], "ollama");
});

test("runOcrWithProvider auto prefers Ollama", async () => {
  const calls = [];
  const result = await runOcrWithProvider({
    imagePath: "/tmp/fake.png",
    env: { CLAWSHIER_VISION_PROVIDER: "auto", OPENAI_API_KEY: "key" },
    openaiOcr: async () => {
      calls.push("openai");
      return "OPENAI OCR";
    },
    ollamaOcr: async () => {
      calls.push("ollama");
      return "OLLAMA OCR";
    },
  });

  assert.equal(result, "OLLAMA OCR");
  assert.deepEqual(calls, ["ollama"]);
});

test("runOcrWithProvider auto falls back to OpenAI", async () => {
  const calls = [];
  const result = await runOcrWithProvider({
    imagePath: "/tmp/fake.png",
    env: { CLAWSHIER_VISION_PROVIDER: "auto", OPENAI_API_KEY: "key" },
    openaiOcr: async () => {
      calls.push("openai");
      return "OPENAI OCR";
    },
    ollamaOcr: async () => {
      calls.push("ollama");
      throw new Error("ollama unavailable");
    },
  });

  assert.equal(result, "OPENAI OCR");
  assert.deepEqual(calls, ["ollama", "openai"]);
});

test("runOcrWithProvider auto surfaces both errors when all backends fail", async () => {
  await assert.rejects(
    () => runOcrWithProvider({
      imagePath: "/tmp/fake.png",
      env: { CLAWSHIER_VISION_PROVIDER: "auto" },
      openaiOcr: async () => {
        throw new Error("missing OpenAI key");
      },
      ollamaOcr: async () => {
        throw new Error("ollama unavailable");
      },
    }),
    /Auto OCR fallback failed. Ollama error: ollama unavailable. OpenAI error: missing OpenAI key/
  );
});

test("ocrWithOllama sends the image as base64 through fetch", async () => {
  const imagePath = path.join(os.tmpdir(), `clawshier-ollama-${process.pid}.png`);
  fs.writeFileSync(imagePath, Buffer.from("hello-image"));

  const calls = [];
  const text = await ocrWithOllama({
    imagePath,
    host: "http://127.0.0.1:11434",
    model: "llama3.2-vision:latest",
    fetchImpl: async (url, options) => {
      calls.push({ url, options: JSON.parse(options.body) });
      return {
        ok: true,
        json: async () => ({ message: { content: "RECEIPT OCR" } }),
      };
    },
  });

  assert.equal(text, "RECEIPT OCR");
  assert.equal(calls[0].url, "http://127.0.0.1:11434/api/chat");
  assert.equal(calls[0].options.model, "llama3.2-vision:latest");
  assert.equal(calls[0].options.stream, false);
  assert.equal(calls[0].options.messages[0].images[0], Buffer.from("hello-image").toString("base64"));
});

test("ocrWithOllama surfaces HTTP failures", async () => {
  const imagePath = path.join(os.tmpdir(), `clawshier-ollama-error-${process.pid}.png`);
  fs.writeFileSync(imagePath, Buffer.from("hello-image"));

  await assert.rejects(
    () => ocrWithOllama({
      imagePath,
      host: "http://127.0.0.1:11434",
      model: "llama3.2-vision:latest",
      fetchImpl: async () => ({
        ok: false,
        status: 500,
        statusText: "Internal Server Error",
        text: async () => "boom",
      }),
    }),
    /Ollama OCR request failed: 500 Internal Server Error boom/
  );
});
