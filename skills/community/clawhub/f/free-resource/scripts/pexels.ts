#!/usr/bin/env bun
/**
 * Pexels API CLI - search and download royalty-free photos & videos.
 *
 * Usage:
 *   bun ./scripts/pexels.ts search-photos --query "city skyline" --orientation landscape
 *   bun ./scripts/pexels.ts search-videos --query "ocean waves" --size medium
 *   bun ./scripts/pexels.ts download --url "https://..." --output "/path/to/file.jpg"
 */

import * as path from "path";
import * as fs from "fs";

const BASE_URL = "https://api.pexels.com/v1";
const CONFIG_FILE = path.join(import.meta.dir, "..", "config.json");

// ── helpers ──────────────────────────────────────────────────────────────

function loadConfig(): Record<string, any> {
  if (fs.existsSync(CONFIG_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(CONFIG_FILE, "utf-8"));
    } catch (e) {
      return {};
    }
  }
  return {};
}

function getApiKey(args: Record<string, string | undefined>): string {
  // Priority: CLI arg > env var > config file
  const key = args["--key"] ?? process.env.PEXELS_API_KEY ?? loadConfig()?.pexels?.api_key;
  if (!key) {
    console.error(
      "Error: API key required. Use --key, set PEXELS_API_KEY env var, or add to config.json."
    );
    process.exit(1);
  }
  return key;
}

function parseArgs(argv: string[]): {
  command: string;
  flags: Record<string, string>;
} {
  const command = argv[0] ?? "";
  const flags: Record<string, string> = {};
  for (let i = 1; i < argv.length; i++) {
    const arg = normalizeFlag(argv[i]);
    if (arg.startsWith("--") && i + 1 < argv.length && !argv[i + 1].startsWith("--")) {
      flags[arg] = argv[++i];
    } else if (arg.startsWith("--")) {
      // boolean flag
      flags[arg] = "true";
    }
  }
  return { command, flags };
}

function normalizeFlag(flag: string): string {
  switch (flag) {
    case "-q":
      return "--query";
    case "-o":
      return "--output";
    default:
      return flag;
  }
}

async function apiRequest(
  endpoint: string,
  params: Record<string, string | number | undefined>,
  key: string
): Promise<any> {
  const qs = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null && v !== "") {
      qs.set(k, String(v));
    }
  }

  const url = `${BASE_URL}${endpoint}?${qs.toString()}`;
  const resp = await fetch(url, {
    headers: {
      "Authorization": key,
      "User-Agent": "PexelsCLI/0.1",
    },
  });

  const limit = resp.headers.get("X-Ratelimit-Limit");
  const remaining = resp.headers.get("X-Ratelimit-Remaining");
  const reset = resp.headers.get("X-Ratelimit-Reset");
  if (limit) {
    console.error(`Rate limit: ${remaining}/${limit} remaining, resets at ${reset}`);
  }

  if (!resp.ok) {
    const body = await resp.text();
    console.error(`HTTP ${resp.status}: ${body}`);
    process.exit(1);
  }

  return resp.json();
}

async function downloadFile(url: string, output: string): Promise<void> {
  const resp = await fetch(url, {
    headers: { "User-Agent": "PexelsCLI/0.1" },
  });
  if (!resp.ok) {
    console.error(`Download failed - HTTP ${resp.status}`);
    process.exit(1);
  }
  const buf = await resp.arrayBuffer();
  await Bun.write(output, new Uint8Array(buf));
  console.error(`Downloaded: ${output}`);
}

function applyCommonSearchParams(
  flags: Record<string, string>,
  params: Record<string, string | number | undefined>
) {
  if (flags["--query"]) params.query = flags["--query"];
  if (flags["--orientation"]) params.orientation = flags["--orientation"];
  if (flags["--size"]) params.size = flags["--size"];
  if (flags["--locale"]) params.locale = flags["--locale"];
  if (flags["--page"]) params.page = Number(flags["--page"]);
  if (flags["--per-page"]) params.per_page = Number(flags["--per-page"]);
}

// ── commands ─────────────────────────────────────────────────────────────

async function searchPhotos(flags: Record<string, string>) {
  const key = getApiKey(flags);
  if (!flags["--query"]) {
    console.error("Error: --query is required");
    process.exit(1);
  }

  const params: Record<string, string | number | undefined> = {};

  applyCommonSearchParams(flags, params);
  if (flags["--color"]) params.color = flags["--color"];

  const data = await apiRequest("/search", params, key);
  console.error(`Found ${data.total_results ?? 0} photos (showing ${data.photos?.length ?? 0})`);

  const json = JSON.stringify(data, null, 2);
  if (flags["--output"]) {
    await Bun.write(flags["--output"], json);
    console.error(`Results saved to: ${flags["--output"]}`);
  } else {
    console.log(json);
  }
}

async function searchVideos(flags: Record<string, string>) {
  const key = getApiKey(flags);
  if (!flags["--query"]) {
    console.error("Error: --query is required");
    process.exit(1);
  }

  const params: Record<string, string | number | undefined> = {};

  applyCommonSearchParams(flags, params);

  const data = await apiRequest("/videos/search", params, key);
  console.error(`Found ${data.total_results ?? 0} videos (showing ${data.videos?.length ?? 0})`);

  const json = JSON.stringify(data, null, 2);
  if (flags["--output"]) {
    await Bun.write(flags["--output"], json);
    console.error(`Results saved to: ${flags["--output"]}`);
  } else {
    console.log(json);
  }
}

async function download(flags: Record<string, string>) {
  if (!flags["--url"]) {
    console.error("Error: --url is required");
    process.exit(1);
  }
  if (!flags["--output"]) {
    console.error("Error: --output is required");
    process.exit(1);
  }
  await downloadFile(flags["--url"], flags["--output"]);
}

// ── help ─────────────────────────────────────────────────────────────────

function printHelp() {
  console.log(`Pexels API CLI - search and download royalty-free photos & videos

Commands:
  search-photos   Search for photos
  search-videos   Search for videos
  download        Download a file by URL

Common flags:
  --key           Pexels API key (or set PEXELS_API_KEY env var)
  --query / -q    Search term
  --orientation   landscape | portrait | square
  --size          Photos: large | medium | small; Videos: large | medium | small
  --locale        Search locale, e.g. en-US, zh-CN, ja-JP
  --page          Page number (default: 1)
  --per-page      Results per page, 1-80 (default: 15)
  --output / -o   Save JSON to file

Photo-specific:
  --color         red | orange | yellow | green | turquoise | blue | violet | pink | brown | black | gray | white | hex color

Download:
  --url           URL to download
  --output        Local file path to save`);
}

// ── main ─────────────────────────────────────────────────────────────────

const rawArgs = process.argv.slice(2);
if (rawArgs.length === 0 || rawArgs[0] === "--help" || rawArgs[0] === "-h") {
  printHelp();
  process.exit(0);
}

const { command, flags } = parseArgs(rawArgs);

switch (command) {
  case "search-photos":
    await searchPhotos(flags);
    break;
  case "search-videos":
    await searchVideos(flags);
    break;
  case "download":
    await download(flags);
    break;
  default:
    console.error(`Unknown command: ${command}`);
    printHelp();
    process.exit(1);
}
