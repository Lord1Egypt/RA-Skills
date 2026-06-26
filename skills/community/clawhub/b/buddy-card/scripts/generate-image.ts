#!/usr/bin/env bun
/**
 * Minimal Gemini image generation — zero external dependencies.
 * Only needs: GOOGLE_API_KEY (or GEMINI_API_KEY) env var.
 *
 * Usage: bun generate-image.ts --prompt "..." --image output.jpg [--ar 3:4]
 */
import { writeFile } from "node:fs/promises";
import { execFileSync } from "node:child_process";

// --- Config ---
const API_KEY = process.env.GOOGLE_API_KEY || process.env.GEMINI_API_KEY;
const MODEL = process.env.GOOGLE_IMAGE_MODEL || "gemini-3-pro-image-preview";
const BASE_URL = (process.env.GOOGLE_BASE_URL || "https://generativelanguage.googleapis.com").replace(/\/+$/g, "");

// --- Args ---
const args = process.argv.slice(2);
let prompt = "", imagePath = "", ar = "3:4", quality = "2K";

for (let i = 0; i < args.length; i++) {
  if ((args[i] === "--prompt" || args[i] === "-p") && args[i + 1]) prompt = args[++i];
  else if (args[i] === "--image" && args[i + 1]) imagePath = args[++i];
  else if (args[i] === "--ar" && args[i + 1]) ar = args[++i];
  else if (args[i] === "--quality" && args[i + 1]) quality = args[++i];
}

if (!prompt || !imagePath) {
  console.error("Usage: bun generate-image.ts --prompt '...' --image out.jpg [--ar 3:4]");
  process.exit(1);
}
if (!API_KEY) {
  console.error("Error: Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable.");
  console.error("Get a free key at: https://aistudio.google.com/apikey");
  process.exit(1);
}

// --- Generate ---
const fullPrompt = `${prompt} Aspect ratio: ${ar}. High resolution ${quality === "2K" || quality === "2k" ? "2048px" : "1024px"}.`;
const url = `${BASE_URL}/v1beta/models/${MODEL}:generateContent`;
const body = JSON.stringify({
  contents: [{ role: "user", parts: [{ text: fullPrompt }] }],
  generationConfig: {
    responseModalities: ["IMAGE"],
    imageConfig: { imageSize: quality.toUpperCase() as "1K" | "2K" | "4K" },
  },
});

function extractImage(responseText: string): Uint8Array {
  const parsed = JSON.parse(responseText);
  if (parsed.error) throw new Error(`Google API error (${parsed.error.code}): ${parsed.error.message}`);
  const data = parsed.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
  if (typeof data === "string" && data.length > 0) return Uint8Array.from(Buffer.from(data, "base64"));
  throw new Error("No image in response");
}

async function generateViaFetch(): Promise<Uint8Array> {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-goog-api-key": API_KEY! },
    body,
  });
  if (!res.ok) throw new Error(`Google API error (${res.status}): ${await res.text()}`);
  return extractImage(await res.text());
}

function generateViaCurl(): Uint8Array {
  const proxy = process.env.HTTPS_PROXY || process.env.HTTP_PROXY || process.env.https_proxy || process.env.http_proxy || null;
  const curlArgs = [
    "-s", "--connect-timeout", "30", "--max-time", "300",
    ...(proxy ? ["-x", proxy] : []),
    url,
    "-H", "Content-Type: application/json",
    "-H", `x-goog-api-key: ${API_KEY}`,
    "-d", body,
  ];
  const result = execFileSync("curl", curlArgs, { maxBuffer: 100 * 1024 * 1024, timeout: 310000 });
  return extractImage(result.toString());
}

async function generate(): Promise<Uint8Array> {
  const hasProxy = !!(process.env.HTTPS_PROXY || process.env.HTTP_PROXY || process.env.https_proxy || process.env.http_proxy);
  // Use curl when behind a proxy (Bun fetch has known proxy issues)
  if (hasProxy) return generateViaCurl();
  return generateViaFetch();
}

console.log(`Generating with ${MODEL}...`);
try {
  const imageBytes = await generate();
  await writeFile(imagePath, imageBytes);
  console.log(`✅ ${imagePath}`);
} catch (e: any) {
  console.error(`Generation failed: ${e.message}`);
  console.log("Retrying...");
  try {
    const imageBytes = await generate();
    await writeFile(imagePath, imageBytes);
    console.log(`✅ ${imagePath}`);
  } catch (e2: any) {
    console.error(`Retry failed: ${e2.message}`);
    process.exit(1);
  }
}
