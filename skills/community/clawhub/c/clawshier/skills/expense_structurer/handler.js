#!/usr/bin/env node
require("dotenv").config({ path: require("path").resolve(__dirname, "../../.env") });

const fs = require("fs");
const path = require("path");
const OpenAI = require("openai");
const { isTraceEnabled, readTrace, writeTrace, startTraceStep, finishTraceStep } = require("../../lib/trace");
const { readJsonInput, writeJsonOutput } = require("../../lib/io");

const isTestMode = process.env.CLAWSHIER_TEST_MODE === "1";
const openai = isTestMode ? null : new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const model = process.env.OPENAI_MODEL || "gpt-4o";

const SYSTEM_PROMPT = `You are a receipt parser. Given raw OCR text from a receipt or invoice, extract structured data as JSON.

Required fields:
- date: The date as it appears on the receipt, including day, month, and year. Preserve the original format (do not reorder components). Infer the year if missing.
- vendor: Business or store name.
- items: Array of { description, quantity, amount }. Each amount MUST be a number (use 0 if not visible). Use quantity 1 if not specified.
- subtotal: Number. If missing, sum the item amounts.
- tax: Number. Use 0 if not visible.
- total: Number. The final total paid.
- currency: ISO 4217 code (e.g. USD, EUR). Infer from symbols or country context.
- category: One of: "Food & Drink", "Transport", "Groceries", "Shopping", "Utilities", "Health", "Entertainment", "Travel", "Office", "Other".

Respond ONLY with valid JSON matching this schema. No markdown, no explanation.`;

function readMockStructured() {
  const fixturePath = process.env.CLAWSHIER_TEST_STRUCTURED_FIXTURE || path.resolve(__dirname, "../../test/fixtures/mock-structured.json");
  return JSON.parse(fs.readFileSync(fixturePath, "utf8"));
}

async function processExpenseStructure(input) {
  const { ocr_text } = input || {};
  if (!ocr_text) throw new Error("Missing ocr_text in input");

  const traceEnabled = isTraceEnabled();
  const trace = traceEnabled ? (readTrace() || { steps: [] }) : null;
  const traceStep = traceEnabled ? startTraceStep("structure", {
    kind: "llm",
    provider: "openai",
    model,
  }) : null;

  if (isTestMode) {
    const output = readMockStructured();
    if (traceEnabled) {
      trace.steps.push(finishTraceStep(traceStep, { provider: "mock", status: "ok" }));
      writeTrace(trace);
    }
    return output;
  }

  const response = await openai.chat.completions.create({
    model,
    response_format: { type: "json_object" },
    messages: [
      { role: "system", content: SYSTEM_PROMPT },
      { role: "user", content: ocr_text },
    ],
    max_tokens: 1024,
  });

  const structured = JSON.parse(response.choices[0].message.content);

  const required = ["date", "vendor", "items", "total", "currency", "category"];
  for (const field of required) {
    if (structured[field] === undefined || structured[field] === null) {
      throw new Error(`Missing required field: ${field}`);
    }
  }

  if (traceEnabled) {
    trace.steps.push(finishTraceStep(traceStep, {
      status: "ok",
      usage: response.usage || null,
    }));
    writeTrace(trace);
  }

  return structured;
}

async function main() {
  writeJsonOutput(await processExpenseStructure(await readJsonInput()));
}

if (require.main === module) {
  main().catch((err) => {
    process.stderr.write(JSON.stringify({ error: err.message }));
    process.exit(1);
  });
}

module.exports = {
  processExpenseStructure,
  readMockStructured,
};
