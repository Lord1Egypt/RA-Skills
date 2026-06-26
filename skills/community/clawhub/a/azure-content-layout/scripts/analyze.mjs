#!/usr/bin/env node
/**
 * Azure Content Understanding - Layout Analyzer
 *
 * Extracts document structure as Markdown and structured JSON using
 * Azure Content Understanding prebuilt-layout analyzer.
 *
 * Usage:
 *   node analyze.mjs --url "https://example.com/doc.pdf" [--output result.json] [--markdown result.md]
 *   cat document.pdf | node analyze.mjs --stdin [--output result.json] [--markdown result.md]
 *
 * Environment:
 *   AZURE_CU_ENDPOINT  - Azure Content Understanding endpoint (e.g. https://xxx.services.ai.azure.com/)
 *   AZURE_CU_API_KEY   - Subscription key (Ocp-Apim-Subscription-Key)
 *   AZURE_CU_API_VERSION - API version (default: 2025-05-01-preview)
 */

import { writeFileSync } from "fs";
import { argv, env, exit, stdin } from "process";

const API_VERSION = env.AZURE_CU_API_VERSION || "2025-05-01-preview";
const POLL_INTERVAL_MS = 3000;
const MAX_POLL_ATTEMPTS = 120; // 6 minutes max

function parseArgs() {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === "--url" && argv[i + 1]) args.url = argv[++i];
    else if (argv[i] === "--stdin") args.stdin = true;
    else if (argv[i] === "--output" && argv[i + 1]) args.output = argv[++i];
    else if (argv[i] === "--markdown" && argv[i + 1]) args.markdown = argv[++i];
    else if (argv[i] === "--api-version" && argv[i + 1]) args.apiVersion = argv[++i];
  }
  return args;
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function readStdin() {
  return new Promise((resolve, reject) => {
    const chunks = [];
    stdin.on("data", (chunk) => chunks.push(chunk));
    stdin.on("end", () => resolve(Buffer.concat(chunks)));
    stdin.on("error", reject);
  });
}

async function submitAnalysis(endpoint, apiKey, apiVersion, source) {
  const analyzeUrl = `${endpoint.replace(/\/+$/, "")}/contentunderstanding/analyzers/prebuilt-layout:analyze?api-version=${apiVersion}`;

  let res;
  if (source.url) {
    // URL-based: body format depends on API version
    const body = apiVersion >= "2025-11-01"
      ? { inputs: [{ url: source.url }] }
      : { url: source.url };

    res = await fetch(analyzeUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": apiKey,
      },
      body: JSON.stringify(body),
    });
  } else {
    // Binary data from stdin
    res = await fetch(analyzeUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": apiKey,
      },
      body: source.data,
    });
  }

  if (res.status !== 202) {
    const text = await res.text();
    console.error(`Submit failed (${res.status}): ${text}`);
    exit(1);
  }

  const operationLocation = res.headers.get("operation-location");
  const body = await res.json();
  return { operationLocation, id: body.id };
}

async function pollResult(operationLocation, apiKey) {
  for (let i = 0; i < MAX_POLL_ATTEMPTS; i++) {
    await sleep(POLL_INTERVAL_MS);
    const res = await fetch(operationLocation, {
      headers: { "Ocp-Apim-Subscription-Key": apiKey },
    });
    const data = await res.json();

    if (data.status === "Succeeded") return data;
    if (data.status === "Failed") {
      console.error("Analysis failed:", JSON.stringify(data, null, 2));
      exit(1);
    }
    process.stderr.write(".");
  }
  console.error("\nTimeout waiting for analysis result");
  exit(1);
}

async function main() {
  const args = parseArgs();
  const endpoint = env.AZURE_CU_ENDPOINT;
  const apiKey = env.AZURE_CU_API_KEY;
  const apiVersion = args.apiVersion || API_VERSION;

  if (!endpoint || !apiKey) {
    console.error("Error: Set AZURE_CU_ENDPOINT and AZURE_CU_API_KEY environment variables");
    exit(1);
  }
  if (!args.url && !args.stdin) {
    console.error("Error: --url or --stdin is required");
    console.error("  node analyze.mjs --url \"https://example.com/doc.pdf\"");
    console.error("  cat doc.pdf | node analyze.mjs --stdin");
    exit(1);
  }

  let source;
  if (args.url) {
    source = { url: args.url };
    console.error(`Analyzing: ${args.url}`);
  } else {
    console.error("Reading from stdin...");
    const data = await readStdin();
    source = { data };
    console.error(`Analyzing: stdin (${data.length} bytes)`);
  }

  const { operationLocation } = await submitAnalysis(endpoint, apiKey, apiVersion, source);
  console.error("Waiting for result");
  const result = await pollResult(operationLocation, apiKey);
  console.error("\nDone!");

  // Extract markdown from first content
  const content = result.result?.contents?.[0];
  const markdown = content?.markdown || "";

  // Save outputs
  if (args.markdown) {
    writeFileSync(args.markdown, markdown);
    console.error(`Markdown saved: ${args.markdown} (${markdown.length} chars)`);
  }

  if (args.output) {
    writeFileSync(args.output, JSON.stringify(result, null, 2));
    console.error(`Full JSON saved: ${args.output}`);
  }

  // If no output files specified, print markdown to stdout
  if (!args.markdown && !args.output) {
    console.log(markdown);
  }
}

main().catch((e) => {
  console.error(e);
  exit(1);
});
