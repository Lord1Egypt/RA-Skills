#!/usr/bin/env node
/**
 * chat.mjs
 *
 * Chat with xAI Grok via Responses API.
 * Supports optional image attachments.
 *
 * Examples:
 *   node {baseDir}/scripts/chat.mjs "What is xAI?"
 *   node {baseDir}/scripts/chat.mjs --model grok-4-1-fast "Summarize today's AI news"
 *   node {baseDir}/scripts/chat.mjs --image ./pic.jpg "What's in this image?"
 *   node {baseDir}/scripts/chat.mjs --json "Return a JSON object with keys a,b"
 */

import fs from "node:fs";
import path from "node:path";

import { collectCitations, getRuntimeConfig, readApiKeys } from "./shared.mjs";

function usage(msg) {
  if (msg) console.error(msg);
  console.error(
    "Usage: chat.mjs [--model <id>] [--json] [--raw] [--image <path>]... <prompt>"
  );
  process.exit(2);
}

function readKeyFromClawdbotConfig() {
  return readApiKeys().apiKey;
}

function mimeFor(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === ".jpg" || ext === ".jpeg") return "image/jpeg";
  if (ext === ".png") return "image/png";
  if (ext === ".webp") return "image/webp";
  if (ext === ".gif") return "image/gif";
  return null;
}

function toDataUrl(filePath) {
  const mime = mimeFor(filePath);
  if (!mime) throw new Error(`Unsupported image type: ${filePath}`);
  const buf = fs.readFileSync(filePath);
  return `data:${mime};base64,${buf.toString("base64")}`;
}

const args = process.argv.slice(2);
if (!args.length) usage();

const runtime = getRuntimeConfig();
let model = runtime.model;
let jsonOut = false;
let rawOut = false;
let images = [];
let promptParts = [];

for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "--model") {
    const v = args[++i];
    if (!v) usage("Missing value for --model");
    model = v;
  } else if (a === "--json") jsonOut = true;
  else if (a === "--raw") rawOut = true;
  else if (a === "--image") {
    const v = args[++i];
    if (!v) usage("Missing value for --image");
    images.push(v);
  } else if (a.startsWith("-")) usage(`Unknown flag: ${a}`);
  else promptParts.push(a);
}

const prompt = promptParts.join(" ").trim();
if (!prompt) usage("Missing <prompt>");

const apiKey = readKeyFromClawdbotConfig();
if (!apiKey) {
  console.error("Missing CUSTOM_GROK_APIKEY/XAI_API_KEY.");
  process.exit(1);
}

const content = [{ type: "input_text", text: prompt }];
for (const img of images) {
  content.push({ type: "input_image", image_url: toDataUrl(img) });
}

const body = {
  model,
  input: [{ role: "user", content }],
  store: false,
};

const res = await fetch(`${runtime.baseUrl}/responses`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${apiKey}`,
    ...(runtime.userAgent ? { "User-Agent": runtime.userAgent } : {}),
  },
  body: JSON.stringify(body),
});

if (!res.ok) {
  const t = await res.text().catch(() => "");
  console.error(`xAI-compatible API error: ${res.status} ${res.statusText}`);
  console.error(t.slice(0, 4000));
  process.exit(1);
}

const data = await res.json();
const text =
  data.output_text ||
  data?.output
    ?.flatMap((o) => (Array.isArray(o?.content) ? o.content : []))
    ?.find((c) => c?.type === "output_text" && typeof c?.text === "string")
    ?.text ||
  "";

if (jsonOut) {
  console.log(JSON.stringify({ model, prompt, text, citations: collectCitations(data) }, null, 2));
  if (rawOut) console.error(JSON.stringify(data, null, 2));
  process.exit(0);
}

console.log(text.trim());
const cites = collectCitations(data);
if (cites.length) {
  console.log("\nCitations:");
  for (const c of cites) console.log(`- ${c}`);
}

if (rawOut) {
  console.error("\n--- RAW RESPONSE (debug) ---\n");
  console.error(JSON.stringify(data, null, 2));
}
