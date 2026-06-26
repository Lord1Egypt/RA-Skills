#!/usr/bin/env node
require("dotenv").config({ path: require("path").resolve(__dirname, "../../.env") });

const fs = require("fs");
const path = require("path");
const { runOcrWithProvider } = require("../../lib/visionOcr");
const { isTraceEnabled, readTrace, writeTrace, startTraceStep, finishTraceStep } = require("../../lib/trace");
const { writeJsonOutput } = require("../../lib/io");

const isTestMode = process.env.CLAWSHIER_TEST_MODE === "1";

function getImagePath(argv = process.argv) {
  const imageArg = argv.indexOf("--image");
  if (imageArg === -1 || !argv[imageArg + 1]) {
    throw new Error("Usage: handler.js --image <path>");
  }
  return argv[imageArg + 1];
}

function runMockOcr(imagePath) {
  const fixturePath = process.env.CLAWSHIER_TEST_OCR_FIXTURE || path.resolve(__dirname, "../../test/fixtures/mock-ocr.txt");
  const base = path.basename(imagePath).toLowerCase();

  if (base.includes("not-a-receipt")) {
    throw new Error("Image does not appear to be a receipt or invoice");
  }

  return fs.readFileSync(fixturePath, "utf8").trim();
}

async function processReceiptOcr({ imagePath }) {
  const traceEnabled = isTraceEnabled();
  const trace = traceEnabled ? (readTrace() || { steps: [] }) : null;
  const traceStep = traceEnabled ? startTraceStep("ocr", { kind: "vision", imagePath }) : null;

  if (isTestMode) {
    const output = { ocr_text: runMockOcr(imagePath) };
    if (traceEnabled) {
      trace.steps.push(finishTraceStep(traceStep, {
        provider: "mock",
        status: "ok",
      }));
      writeTrace(trace);
    }
    return output;
  }

  const ocrText = await runOcrWithProvider({ imagePath });
  if (traceEnabled) {
    trace.steps.push(finishTraceStep(traceStep, {
      provider: String(process.env.CLAWSHIER_VISION_PROVIDER || "openai").trim().toLowerCase(),
      model: String(process.env.CLAWSHIER_VISION_PROVIDER || "openai").trim().toLowerCase() === "ollama"
        ? String(process.env.CLAWSHIER_OLLAMA_MODEL || "llama3.2-vision:latest").trim()
        : String(process.env.OPENAI_MODEL || "gpt-4o").trim(),
      status: "ok",
    }));
    writeTrace(trace);
  }
  return { ocr_text: ocrText };
}

async function main() {
  const imagePath = getImagePath();
  writeJsonOutput(await processReceiptOcr({ imagePath }));
}

if (require.main === module) {
  main().catch((err) => {
    process.stderr.write(JSON.stringify({ error: err.message }));
    process.exit(1);
  });
}

module.exports = {
  getImagePath,
  processReceiptOcr,
  runMockOcr,
};
