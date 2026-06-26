#!/usr/bin/env node

import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { pathToFileURL } from "node:url";
import { chromium } from "playwright-core";

const IMAGE_TYPES = new Set(["png", "svg"]);

class CliError extends Error {}

function usage() {
  console.log(`Usage:
  node {baseDir}/scripts/render-image.mjs --input ./artifacts/revenue-profit --type png
  node {baseDir}/scripts/render-image.mjs --input ./artifacts/revenue-profit/chart.html --type svg --out ./exports

Flags:
  --input <dir|chart.html>          Required. Artifact directory or chart.html path
  --type <png|svg>                  Output type. Default: png
  --out <file-or-dir>               Optional output file or directory
  --browser-executable <path>       Optional browser executable override
  --viewport-width <number>         Optional browser viewport width
  --viewport-height <number>        Optional browser viewport height
  --pixel-ratio <number>            PNG scale factor. Default: 2
  --timeout-ms <number>             Wait timeout. Default: 30000
  --wait-ms <number>                Extra settle time after chart ready. Default: 150
  --background <auto|transparent|color>  PNG background. Default: auto`);
}

function parseArgs(argv) {
  if (argv.length === 0 || argv[0] === "--help" || argv[0] === "-h") {
    return { help: true, flags: new Map() };
  }

  const flags = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      throw new CliError(`Unexpected argument: ${token}`);
    }

    const key = token.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      flags.set(key, [true]);
      continue;
    }

    if (!flags.has(key)) {
      flags.set(key, []);
    }
    flags.get(key).push(next);
    index += 1;
  }

  return { help: false, flags };
}

function getLast(flags, key, fallback = undefined) {
  const values = flags.get(key);
  return values ? values.at(-1) : fallback;
}

function requireFlag(flags, key) {
  const value = getLast(flags, key);
  if (value === undefined || value === true) {
    throw new CliError(`Missing required --${key} value`);
  }
  return value;
}

function parsePositiveInt(flags, key, fallback) {
  const raw = getLast(flags, key);
  if (raw === undefined) {
    return fallback;
  }
  const value = Number.parseInt(String(raw), 10);
  if (!Number.isFinite(value) || value <= 0) {
    throw new CliError(`--${key} must be a positive integer`);
  }
  return value;
}

function parsePositiveNumber(flags, key, fallback) {
  const raw = getLast(flags, key);
  if (raw === undefined) {
    return fallback;
  }
  const value = Number(raw);
  if (!Number.isFinite(value) || value <= 0) {
    throw new CliError(`--${key} must be a positive number`);
  }
  return value;
}

function parseImageType(flags) {
  const type = getLast(flags, "type", "png");
  if (!IMAGE_TYPES.has(type)) {
    throw new CliError(`Unsupported --type value: ${type}`);
  }
  return type;
}

async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function resolveInput(inputRaw) {
  const resolved = path.resolve(process.cwd(), inputRaw);
  const stat = await fs.stat(resolved).catch(() => null);
  if (!stat) {
    throw new CliError(`Input path not found: ${inputRaw}`);
  }

  if (stat.isDirectory()) {
    const htmlPath = path.join(resolved, "chart.html");
    if (!(await exists(htmlPath))) {
      throw new CliError(`Artifact directory is missing chart.html: ${inputRaw}`);
    }
    return { htmlPath, artifactDir: resolved };
  }

  if (path.extname(resolved).toLowerCase() !== ".html") {
    throw new CliError("--input must point to an artifact directory or a chart.html file");
  }

  return { htmlPath: resolved, artifactDir: path.dirname(resolved) };
}

function extractBootstrap(html) {
  const match = html.match(/<script id="bootstrap" type="application\/json">([\s\S]*?)<\/script>/);
  if (!match) {
    throw new CliError("Could not find bootstrap JSON inside chart.html");
  }
  return JSON.parse(match[1]);
}

function themeBackground(theme) {
  if (theme === "dark") {
    return "#10141d";
  }
  if (theme === "paper") {
    return "#f5f0e6";
  }
  return "#ffffff";
}

function splitPathEnv(value) {
  return String(value || "")
    .split(path.delimiter)
    .map((entry) => entry.trim())
    .filter(Boolean);
}

function commandCandidates() {
  if (process.platform === "win32") {
    return ["chrome.exe", "msedge.exe", "brave.exe", "chromium.exe"];
  }
  if (process.platform === "darwin") {
    return ["Google Chrome", "Microsoft Edge", "Brave Browser", "Chromium"];
  }
  return ["google-chrome", "microsoft-edge", "chromium-browser", "chromium", "brave-browser"];
}

function commonBrowserPaths() {
  const localAppData = process.env.LOCALAPPDATA || path.join(os.homedir(), "AppData", "Local");
  if (process.platform === "win32") {
    return [
      path.join(localAppData, "Google", "Chrome", "Application", "chrome.exe"),
      path.join(localAppData, "Microsoft", "Edge", "Application", "msedge.exe"),
      path.join(localAppData, "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
      "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
      "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
      "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
      "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
      "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
    ];
  }

  if (process.platform === "darwin") {
    return [
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
      "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
      "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
      "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ];
  }

  return [
    "/usr/bin/google-chrome",
    "/usr/bin/microsoft-edge",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
    "/snap/bin/chromium",
    "/usr/bin/brave-browser",
  ];
}

async function resolveBrowserExecutable(explicitPath) {
  const candidates = [];
  for (const value of [
    explicitPath,
    process.env.ECHARTS_BROWSER_PATH,
    process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH,
    process.env.CHROME_PATH,
  ]) {
    if (value) {
      candidates.push(path.resolve(String(value)));
    }
  }

  candidates.push(...commonBrowserPaths());
  const pathDirs = splitPathEnv(process.env.PATH);
  for (const dir of pathDirs) {
    for (const command of commandCandidates()) {
      candidates.push(path.join(dir, command));
    }
  }

  const seen = new Set();
  for (const candidate of candidates) {
    const normalized = path.normalize(candidate);
    if (seen.has(normalized)) {
      continue;
    }
    seen.add(normalized);
    if (await exists(normalized)) {
      return normalized;
    }
  }

  throw new CliError(
    "Could not find a Chromium-based browser. Pass --browser-executable or set ECHARTS_BROWSER_PATH.",
  );
}

async function resolveOutputPath(outRaw, artifactDir, fileBase, type) {
  if (!outRaw) {
    return path.join(artifactDir, `${fileBase}.${type}`);
  }

  const resolved = path.resolve(process.cwd(), outRaw);
  const stat = await fs.stat(resolved).catch(() => null);
  if (stat?.isDirectory()) {
    return path.join(resolved, `${fileBase}.${type}`);
  }

  if (!path.extname(resolved)) {
    return path.join(resolved, `${fileBase}.${type}`);
  }

  return resolved;
}

function logWrite(filePath) {
  const relative = path.relative(process.cwd(), filePath) || path.basename(filePath);
  console.log(`[ok] wrote ${relative}`);
}

async function waitForChart(page, timeoutMs) {
  await page.waitForFunction(
    () => {
      const status = document.getElementById("status")?.textContent ?? "";
      return (
        Boolean(window.__ECHARTS_ARTIFACT__?.chart) || status.includes("Could not load ECharts")
      );
    },
    { timeout: timeoutMs },
  );

  const state = await page.evaluate(() => ({
    ready: Boolean(window.__ECHARTS_ARTIFACT__?.chart),
    status: document.getElementById("status")?.textContent ?? "",
  }));
  if (!state.ready) {
    throw new CliError(state.status || "Chart runtime did not become ready.");
  }
}

async function exportPng(page, outputPath, pixelRatio, backgroundColor) {
  const dataUrl = await page.evaluate(
    ({ nextPixelRatio, nextBackgroundColor }) =>
      window.__ECHARTS_ARTIFACT__.chart.getDataURL({
        type: "png",
        pixelRatio: nextPixelRatio,
        backgroundColor: nextBackgroundColor,
      }),
    { nextPixelRatio: pixelRatio, nextBackgroundColor: backgroundColor },
  );

  const base64 = String(dataUrl).replace(/^data:image\/png;base64,/, "");
  await fs.writeFile(outputPath, Buffer.from(base64, "base64"));
}

async function exportSvg(page, outputPath) {
  const svg = await page.evaluate(() => document.querySelector("#chart svg")?.outerHTML ?? null);
  if (!svg) {
    throw new CliError("SVG export requires the chart page to be generated with --renderer svg.");
  }
  await fs.writeFile(outputPath, `${svg}\n`, "utf8");
}

export async function renderArtifactImage(options) {
  const input = await resolveInput(options.inputPath);
  const html = await fs.readFile(input.htmlPath, "utf8");
  const bootstrap = extractBootstrap(html);
  const type = options.type ?? "png";
  if (!IMAGE_TYPES.has(type)) {
    throw new CliError(`Unsupported image type: ${type}`);
  }

  const pixelRatio = options.pixelRatio ?? 2;
  if (!Number.isFinite(pixelRatio) || pixelRatio <= 0) {
    throw new CliError("pixelRatio must be a positive number");
  }

  const timeoutMs = options.timeoutMs ?? 30_000;
  const waitMs = options.waitMs ?? 150;
  const viewportWidth =
    options.viewportWidth ??
    Math.max(Number(bootstrap.width) || 1280, bootstrap.pageMode === "report" ? 1480 : 1280);
  const viewportHeight =
    options.viewportHeight ??
    Math.max(
      (Number(bootstrap.height) || 720) + (bootstrap.pageMode === "report" ? 260 : 120),
      900,
    );
  const background = options.background ?? "auto";
  const backgroundColor =
    background === "auto"
      ? themeBackground(bootstrap.theme)
      : background === "transparent"
        ? "rgba(0, 0, 0, 0)"
        : background;
  const outputPath = await resolveOutputPath(
    options.outPath,
    input.artifactDir,
    bootstrap.fileBase || "chart",
    type,
  );
  const browserExecutable = await resolveBrowserExecutable(options.browserExecutable);

  await fs.mkdir(path.dirname(outputPath), { recursive: true });

  const browser = await chromium.launch({
    executablePath: browserExecutable,
    headless: true,
    args: ["--allow-file-access-from-files"],
  });

  try {
    const page = await browser.newPage({
      viewport: { width: viewportWidth, height: viewportHeight },
    });
    await page.goto(pathToFileURL(input.htmlPath).href, { waitUntil: "load", timeout: timeoutMs });
    await waitForChart(page, timeoutMs);
    if (waitMs > 0) {
      await page.waitForTimeout(waitMs);
    }

    if (type === "png") {
      await exportPng(page, outputPath, pixelRatio, backgroundColor);
    } else {
      await exportSvg(page, outputPath);
    }
  } finally {
    await browser.close();
  }

  if (options.quiet !== true) {
    logWrite(outputPath);
  }

  return {
    outputPath,
    browserExecutable,
    type,
    artifactDir: input.artifactDir,
    htmlPath: input.htmlPath,
    bootstrap,
  };
}

async function main() {
  const parsed = parseArgs(process.argv.slice(2));
  if (parsed.help) {
    usage();
    return;
  }

  await renderArtifactImage({
    inputPath: requireFlag(parsed.flags, "input"),
    type: parseImageType(parsed.flags),
    outPath: getLast(parsed.flags, "out"),
    browserExecutable: getLast(parsed.flags, "browser-executable"),
    viewportWidth: parsePositiveInt(parsed.flags, "viewport-width", undefined),
    viewportHeight: parsePositiveInt(parsed.flags, "viewport-height", undefined),
    pixelRatio: parsePositiveNumber(parsed.flags, "pixel-ratio", 2),
    timeoutMs: parsePositiveInt(parsed.flags, "timeout-ms", 30_000),
    waitMs: parsePositiveInt(parsed.flags, "wait-ms", 150),
    background: getLast(parsed.flags, "background", "auto"),
  });
}

const isMain =
  process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;
if (isMain) {
  main().catch((error) => {
    if (error instanceof CliError) {
      console.error(`[error] ${error.message}`);
      console.error("");
      usage();
      process.exitCode = 1;
      return;
    }

    console.error(error);
    process.exitCode = 1;
  });
}
