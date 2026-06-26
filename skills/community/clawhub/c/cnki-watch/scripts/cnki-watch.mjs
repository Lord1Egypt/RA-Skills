#!/usr/bin/env node

import { promises as fs } from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { randomUUID, createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { parseScheduleSpec } from "./cnki_watch_core.mjs";

const SKILL_KEY = "cnki-watch";
const SCRIPT_PATH = fileURLToPath(import.meta.url);
const SKILL_DIR = path.resolve(path.dirname(SCRIPT_PATH), "..");
const RUNTIME_DIR = path.join(SKILL_DIR, "runtime");
const STATE_PATH = path.join(RUNTIME_DIR, "subscriptions.json");
const PACKAGE_JSON_PATH = path.join(SKILL_DIR, "package.json");
const PACKAGE_LOCK_PATH = path.join(SKILL_DIR, "package-lock.json");
const USER_AGENT =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36";
const DEFAULTS = {
  browserProfile: "chrome",
  timezone: "Asia/Shanghai",
  defaultSchedule: "daily@09:00",
  maxManualResults: 10,
  maxPushResults: 20,
};
const PAPER_DATABASES = new Set(["期刊", "学位论文", "会议", "学术辑刊"]);
const PROXY_ENV_KEYS = [
  "HTTP_PROXY",
  "HTTPS_PROXY",
  "ALL_PROXY",
  "NO_PROXY",
  "http_proxy",
  "https_proxy",
  "all_proxy",
  "no_proxy",
];
const DATE_SORT_TEXT = "发表时间";
const GATEWAY_DEFAULT_URL = "ws://127.0.0.1:18789";

function createRequireSafe(target) {
  try {
    return createRequire(target);
  } catch {
    return null;
  }
}

function summarizeLoadError(error) {
  if (!error) {
    return "unknown error";
  }
  if (error.code === "MODULE_NOT_FOUND") {
    return "module not found";
  }
  return cleanText(error.message || String(error));
}

function autoInstallDisabled() {
  const value = String(process.env.CNKI_WATCH_AUTO_INSTALL ?? "").trim().toLowerCase();
  return value && ["0", "false", "no", "off"].includes(value);
}

async function installProjectDependencies() {
  if (autoInstallDisabled()) {
    throw new Error(
      "playwright-core is missing and automatic npm install is disabled by CNKI_WATCH_AUTO_INSTALL.",
    );
  }

  const npmCommand = process.platform === "win32" ? "npm.cmd" : "npm";
  const installArgs = (await pathExists(PACKAGE_LOCK_PATH))
    ? ["ci", "--no-audit", "--no-fund"]
    : ["install", "--no-audit", "--no-fund"];

  await new Promise((resolve, reject) => {
    const child = spawn(npmCommand, installArgs, {
      cwd: SKILL_DIR,
      env: process.env,
      stdio: "inherit",
    });
    child.on("error", () => {
      reject(
        new Error(
          `Failed to start ${npmCommand}. Install Node.js/npm first or run inside the OpenClaw gateway container.`,
        ),
      );
    });
    child.on("close", (code) => {
      if (code === 0) {
        resolve();
        return;
      }
      reject(new Error(`${npmCommand} ${installArgs.join(" ")} failed with exit code ${code}.`));
    });
  });
}

async function loadPlaywrightModule() {
  const resolutionNotes = [];
  const localCandidates = [
    { label: "skill script", loader: createRequireSafe(import.meta.url) },
    { label: "skill root", loader: createRequireSafe(PACKAGE_JSON_PATH) },
  ].filter((candidate) => candidate.loader);

  for (const candidate of localCandidates) {
    try {
      return candidate.loader("playwright-core");
    } catch (error) {
      resolutionNotes.push(`${candidate.label}: ${summarizeLoadError(error)}`);
    }
  }

  let installError = null;
  if (await pathExists(PACKAGE_JSON_PATH)) {
    try {
      await installProjectDependencies();
      for (const candidate of localCandidates) {
        try {
          return candidate.loader("playwright-core");
        } catch (error) {
          resolutionNotes.push(`${candidate.label} after npm install: ${summarizeLoadError(error)}`);
        }
      }
    } catch (error) {
      installError = error;
      resolutionNotes.push(`npm install: ${summarizeLoadError(error)}`);
    }
  } else {
    resolutionNotes.push("skill root package.json is missing");
  }

  if (await pathExists("/app/package.json")) {
    const containerLoader = createRequireSafe("/app/package.json");
    if (containerLoader) {
      try {
        return containerLoader("playwright-core");
      } catch (error) {
        resolutionNotes.push(`OpenClaw container fallback: ${summarizeLoadError(error)}`);
      }
    }
  }

  const guidance = [
    "playwright-core is unavailable.",
    `Run \`npm install\` in ${SKILL_DIR}.`,
    "If you are running inside the OpenClaw gateway container, make sure the runtime dependencies are installed there.",
  ];
  if (installError && autoInstallDisabled()) {
    guidance.push("Automatic npm install is disabled by CNKI_WATCH_AUTO_INSTALL.");
  }
  if (resolutionNotes.length > 0) {
    guidance.push(`Resolution attempts: ${resolutionNotes.join("; ")}.`);
  }
  throw new Error(guidance.join(" "));
}

const { chromium } = await loadPlaywrightModule();

function nowIso() {
  return new Date().toISOString();
}

function stripProxyEnv(baseEnv) {
  const env = { ...baseEnv };
  for (const key of PROXY_ENV_KEYS) {
    delete env[key];
  }
  return env;
}

function cleanText(value) {
  return String(value ?? "")
    .replace(/\u00a0/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function normalizeComparable(value) {
  return cleanText(value)
    .replace(/[《》“”"'`]/g, "")
    .replace(/\s+/g, "")
    .toLowerCase();
}

function digest(value) {
  return createHash("sha1").update(value).digest("hex");
}

function recordKey(record) {
  if (record.recordId) {
    return `rid:${record.recordId}`;
  }
  if (record.url) {
    return `url:${record.url}`;
  }
  return `hash:${digest(
    [
      normalizeComparable(record.title),
      normalizeComparable(record.source),
      cleanText(record.publishDate),
    ].join("|"),
  )}`;
}

function slugify(value) {
  const slug = cleanText(value)
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fff]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 40);
  return slug || "subscription";
}

function toInt(value, fallback) {
  const parsed = Number.parseInt(String(value ?? ""), 10);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function usage() {
  return `
cnki-watch commands:
  auth-check
  query-topic --topic <topic> [--limit <n>] [--json]
  query-journal --journal <journal> [--limit <n>] [--json]
  subscribe-topic --topic <topic> [--schedule daily@09:00]
  subscribe-journal --journal <journal> [--schedule daily@09:00]
  list-subscriptions [--json]
  unsubscribe --id <subscription-id>
  run-subscription --id <subscription-id> [--session-key main] [--json]
`;
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      args._.push(token);
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

async function pathExists(targetPath) {
  try {
    await fs.access(targetPath);
    return true;
  } catch {
    return false;
  }
}

async function ensureRuntimeDir() {
  await fs.mkdir(RUNTIME_DIR, { recursive: true });
}

async function loadJson(filePath, fallback) {
  try {
    const raw = await fs.readFile(filePath, "utf8");
    return JSON.parse(raw);
  } catch (error) {
    if (error.code === "ENOENT") {
      return fallback;
    }
    throw error;
  }
}

async function saveJson(filePath, value) {
  await ensureRuntimeDir();
  await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

async function loadState() {
  return loadJson(STATE_PATH, { version: 1, subscriptions: [] });
}

async function saveState(state) {
  await saveJson(STATE_PATH, state);
}

function findSubscription(state, id) {
  return state.subscriptions.find((item) => item.id === id) ?? null;
}

async function loadOpenClawConfig() {
  const configPath =
    process.env.OPENCLAW_CONFIG_PATH ||
    path.join(os.homedir(), ".openclaw", "openclaw.json");
  return loadJson(configPath, {});
}

async function loadSettings() {
  const openClawConfig = await loadOpenClawConfig();
  const skillEntry = openClawConfig.skills?.entries?.[SKILL_KEY] ?? {};
  const settings = {
    config: {
      ...DEFAULTS,
      ...(skillEntry.config ?? {}),
    },
    env: {
      ...(skillEntry.env ?? {}),
    },
    gateway: {
      port: openClawConfig.gateway?.port ?? 18789,
      token: openClawConfig.gateway?.auth?.token ?? null,
    },
  };
  settings.config.maxManualResults = toInt(
    settings.config.maxManualResults,
    DEFAULTS.maxManualResults,
  );
  settings.config.maxPushResults = toInt(
    settings.config.maxPushResults,
    DEFAULTS.maxPushResults,
  );
  return settings;
}

function resolveCredential(settings, key) {
  return process.env[key] || settings.env[key] || "";
}

async function resolveChromiumExecutable() {
  if (process.env.CNKI_WATCH_CHROMIUM) {
    return process.env.CNKI_WATCH_CHROMIUM;
  }

  const cacheRoots = [
    process.env.PLAYWRIGHT_BROWSERS_PATH,
    path.join(os.homedir(), ".cache", "ms-playwright"),
    path.join(os.homedir(), "Library", "Caches", "ms-playwright"),
    process.env.LOCALAPPDATA ? path.join(process.env.LOCALAPPDATA, "ms-playwright") : null,
  ].filter(Boolean);

  for (const cacheDir of cacheRoots) {
    if (!(await pathExists(cacheDir))) {
      continue;
    }
    const entries = await fs.readdir(cacheDir, { withFileTypes: true }).catch(() => []);
    const matches = entries
      .filter((entry) => entry.isDirectory() && entry.name.startsWith("chromium-"))
      .map((entry) => ({
        name: entry.name,
        version: toInt(entry.name.split("-")[1], 0),
        executablePaths: [
          path.join(cacheDir, entry.name, "chrome-linux", "chrome"),
          path.join(cacheDir, entry.name, "chrome-linux64", "chrome"),
          path.join(
            cacheDir,
            entry.name,
            "chrome-mac",
            "Chromium.app",
            "Contents",
            "MacOS",
            "Chromium",
          ),
          path.join(cacheDir, entry.name, "chrome-win", "chrome.exe"),
        ],
      }))
      .sort((left, right) => right.version - left.version);

    for (const match of matches) {
      for (const executablePath of match.executablePaths) {
        if (await pathExists(executablePath)) {
          return executablePath;
        }
      }
    }
  }

  const programFiles = process.env.ProgramFiles || process.env.PROGRAMFILES;
  const programFilesX86 =
    process.env["ProgramFiles(x86)"] || process.env.PROGRAMFILES_X86;
  const localAppData = process.env.LOCALAPPDATA;
  const systemCandidates = [
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/lib/chromium/chromium",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/snap/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    programFiles ? path.join(programFiles, "Google", "Chrome", "Application", "chrome.exe") : null,
    programFilesX86
      ? path.join(programFilesX86, "Google", "Chrome", "Application", "chrome.exe")
      : null,
    localAppData
      ? path.join(localAppData, "Google", "Chrome", "Application", "chrome.exe")
      : null,
    programFiles
      ? path.join(programFiles, "Microsoft", "Edge", "Application", "msedge.exe")
      : null,
    programFilesX86
      ? path.join(programFilesX86, "Microsoft", "Edge", "Application", "msedge.exe")
      : null,
    localAppData
      ? path.join(localAppData, "Microsoft", "Edge", "Application", "msedge.exe")
      : null,
  ].filter(Boolean);

  for (const candidate of systemCandidates) {
    if (await pathExists(candidate)) {
      return candidate;
    }
  }
  return null;
}

async function buildBrowserEnv(baseEnv) {
  const runtimeEnvHome = path.join(RUNTIME_DIR, "browser-home");
  const runtimeConfigDir = path.join(runtimeEnvHome, ".config");
  const runtimeCacheDir = path.join(runtimeEnvHome, ".cache");
  await fs.mkdir(runtimeConfigDir, { recursive: true });
  await fs.mkdir(runtimeCacheDir, { recursive: true });

  return {
    ...stripProxyEnv(baseEnv),
    HOME: runtimeEnvHome,
    XDG_CONFIG_HOME: runtimeConfigDir,
    XDG_CACHE_HOME: runtimeCacheDir,
  };
}

async function launchCnkiBrowser() {
  const executablePath = await resolveChromiumExecutable();
  if (!executablePath) {
    throw new Error(
      [
        "No Chromium/Chrome executable was found.",
        "Set CNKI_WATCH_CHROMIUM, install Google Chrome or Microsoft Edge locally,",
        "or run `npm run install:browser` (or `npx playwright install chromium`).",
      ].join(" "),
    );
  }
  const browserEnv = await buildBrowserEnv(process.env);
  const browser = await chromium.launch({
    headless: true,
    executablePath,
    args: ["--no-sandbox", "--disable-blink-features=AutomationControlled", "--no-proxy-server"],
    env: browserEnv,
  });
  const context = await browser.newContext({
    ignoreHTTPSErrors: true,
    locale: "zh-CN",
    timezoneId: "Asia/Shanghai",
    userAgent: USER_AGENT,
    viewport: { width: 1440, height: 960 },
  });
  return { browser, context };
}

function resolveQueryArg(kind, args) {
  const direct = kind === "journal" ? args.journal : args.topic;
  return cleanText(direct || args.name || args.query || args._[1] || "");
}

function parseCookieString(cookieString) {
  const trimmed = cookieString.trim();
  if (!trimmed) {
    return [];
  }
  if (trimmed.startsWith("[")) {
    const parsed = JSON.parse(trimmed);
    if (!Array.isArray(parsed)) {
      throw new Error("CNKI_COOKIE JSON must be an array of cookie objects.");
    }
    return parsed;
  }
  const base = trimmed.replace(/^Cookie:\s*/i, "");
  const cookiePairs = base
    .split(/;\s*/)
    .map((part) => part.trim())
    .filter(Boolean)
    .map((part) => {
      const idx = part.indexOf("=");
      if (idx < 1) {
        return null;
      }
      return {
        name: part.slice(0, idx).trim(),
        value: part.slice(idx + 1).trim(),
      };
    })
    .filter(Boolean);
  const domains = [".cnki.net", "www.cnki.net", "kns.cnki.net", "navi.cnki.net", "my.cnki.net"];
  const cookies = [];
  for (const pair of cookiePairs) {
    for (const domain of domains) {
      cookies.push({
        ...pair,
        domain,
        path: "/",
        secure: true,
        httpOnly: false,
      });
    }
  }
  return cookies;
}

async function applyCookieAuth(context, cookieString) {
  const cookies = parseCookieString(cookieString);
  if (cookies.length > 0) {
    await context.addCookies(cookies);
  }
  return cookies.length;
}

async function maybeLoginWithAccount(page, credentials) {
  if (!credentials.username || !credentials.password) {
    return { used: false, success: false, detail: "missing-account-credentials" };
  }
  await page.goto("https://www.cnki.net/", { waitUntil: "domcontentloaded", timeout: 30000 });
  const loginToggle = page.locator(".ecp_header_personal_loginbg").first();
  if ((await loginToggle.count()) > 0) {
    await loginToggle.click({ timeout: 5000 }).catch(() => {});
  }
  const usernameInput = page.locator(".ecp_userName").first();
  const passwordInput = page.locator(".ecp_passWord").first();
  if ((await usernameInput.count()) === 0 || (await passwordInput.count()) === 0) {
    throw new Error("CNKI login form not found.");
  }
  await usernameInput.fill(credentials.username);
  await passwordInput.fill(credentials.password);
  const agreement = page.locator("#agreement").first();
  if ((await agreement.count()) > 0 && !(await agreement.isChecked())) {
    await agreement.check().catch(() => {});
  }
  const loginButton = page.locator("button.ecp-account-login").first();
  await loginButton.click({ timeout: 10000 });
  await page.waitForLoadState("domcontentloaded", { timeout: 15000 }).catch(() => {});
  if (page.url().includes("/verify/home")) {
    await maybeSolveCaptcha(page);
  }
  await page.waitForTimeout(2500);
  const bodyText = cleanText(await page.locator("body").innerText());
  const loggedIn =
    bodyText.includes("退出") ||
    bodyText.includes("我的账户") ||
    (await page.locator(".ecp_mycnki_logout").count()) > 0;
  if (!loggedIn) {
    throw new Error("CNKI account login did not complete successfully.");
  }
  return { used: true, success: true, detail: "account-login-ok" };
}

async function computeCaptchaGap(page) {
  await page.waitForFunction(
    () =>
      document.querySelectorAll("img").length >= 2 &&
      Array.from(document.querySelectorAll("img"))
        .slice(0, 2)
        .every((img) => img.complete && (img.naturalWidth || img.width) > 0),
    null,
    { timeout: 10000 },
  );
  return page.evaluate(() => {
    function imageDataFrom(img) {
      const canvas = document.createElement("canvas");
      canvas.width = img.naturalWidth || img.width;
      canvas.height = img.naturalHeight || img.height;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0);
      return ctx.getImageData(0, 0, canvas.width, canvas.height);
    }

    const images = Array.from(document.querySelectorAll("img")).filter(
      (img) => (img.naturalWidth || img.width) > 0,
    );
    const backgroundImg =
      images.find((img) => (img.naturalWidth || img.width) >= 300) || images[0];
    const pieceImg =
      images.find((img) => (img.naturalWidth || img.width) < 100) || images[1];
    const background = imageDataFrom(backgroundImg);
    const piece = imageDataFrom(pieceImg);
    const backgroundGray = new Float32Array(background.width * background.height);
    const pieceGray = new Float32Array(piece.width * piece.height);
    for (let i = 0, p = 0; i < background.data.length; i += 4, p += 1) {
      backgroundGray[p] =
        (background.data[i] + background.data[i + 1] + background.data[i + 2]) / 3;
    }
    for (let i = 0, p = 0; i < piece.data.length; i += 4, p += 1) {
      pieceGray[p] = (piece.data[i] + piece.data[i + 1] + piece.data[i + 2]) / 3;
    }
    let minX = piece.width;
    let maxX = 0;
    let minY = piece.height;
    let maxY = 0;
    for (let y = 0; y < piece.height; y += 1) {
      for (let x = 0; x < piece.width; x += 1) {
        const alpha = piece.data[(y * piece.width + x) * 4 + 3];
        if (alpha > 0) {
          if (x < minX) minX = x;
          if (x > maxX) maxX = x;
          if (y < minY) minY = y;
          if (y > maxY) maxY = y;
        }
      }
    }
    const pieceWidth = maxX - minX + 1;
    const coords = [];
    const pieceValues = [];
    for (let y = minY; y <= maxY; y += 1) {
      for (let x = minX; x <= maxX; x += 1) {
        const index = y * piece.width + x;
        if (piece.data[index * 4 + 3] > 0) {
          coords.push((y - minY) * pieceWidth + (x - minX));
          pieceValues.push(pieceGray[index]);
        }
      }
    }
    const pieceMean = pieceValues.reduce((sum, value) => sum + value, 0) / pieceValues.length;
    const centered = pieceValues.map((value) => value - pieceMean);
    let best = { corr: Number.NEGATIVE_INFINITY, x: 0 };
    for (let x = 0; x <= background.width - pieceWidth; x += 1) {
      let regionSum = 0;
      const regionValues = new Array(coords.length);
      for (let i = 0; i < coords.length; i += 1) {
        const rel = coords[i];
        const relY = Math.floor(rel / pieceWidth);
        const relX = rel % pieceWidth;
        const value = backgroundGray[(minY + relY) * background.width + (x + relX)];
        regionValues[i] = value;
        regionSum += value;
      }
      const regionMean = regionSum / regionValues.length;
      let numerator = 0;
      let pieceSquared = 0;
      let regionSquared = 0;
      for (let i = 0; i < regionValues.length; i += 1) {
        const left = centered[i];
        const right = regionValues[i] - regionMean;
        numerator += left * right;
        pieceSquared += left * left;
        regionSquared += right * right;
      }
      const corr = numerator / Math.sqrt(pieceSquared * regionSquared);
      if (corr > best.corr) {
        best = { corr, x };
      }
    }
    return best;
  });
}

async function maybeSolveCaptcha(page) {
  for (let attempt = 0; attempt < 5; attempt += 1) {
    if (!page.url().includes("/verify/home")) {
      return true;
    }
    const gap = await computeCaptchaGap(page);
    const panel = await page.locator(".verify-img-panel").boundingBox();
    const piece = await page.locator(".verify-sub-block").boundingBox();
    const block = await page.locator(".verify-move-block").boundingBox();
    const initialLeft = piece.x - panel.x;
    const delta = gap.x - initialLeft;
    const startX = block.x + block.width / 2;
    const startY = block.y + block.height / 2;
    await page.mouse.move(startX, startY);
    await page.mouse.down();
    const steps = [0.12, 0.25, 0.38, 0.52, 0.66, 0.79, 0.9, 0.97, 1].map((value) =>
      Math.round(delta * value),
    );
    for (const step of steps) {
      await page.mouse.move(startX + step, startY + (Math.random() * 1.6 - 0.8), { steps: 4 });
      await page.waitForTimeout(90 + Math.floor(Math.random() * 90));
    }
    await page.mouse.up();
    await page.waitForTimeout(2500);
    if (!page.url().includes("/verify/home")) {
      return true;
    }
  }
  return false;
}

async function waitForResultRows(page) {
  await page.waitForFunction(
    () => document.querySelectorAll("tbody tr").length > 0,
    null,
    { timeout: 30000 },
  );
}

async function maybeSortByDate(page) {
  for (let attempt = 0; attempt < 2; attempt += 1) {
    const state = await page.evaluate((targetText) => {
      const items = Array.from(document.querySelectorAll(".order-group li"));
      const item = items.find((node) => (node.textContent || "").trim() === targetText);
      return item ? { className: item.className || "" } : null;
    }, DATE_SORT_TEXT);
    if (!state) {
      return false;
    }
    if (state.className.includes("cur") && state.className.includes("DESC")) {
      return true;
    }
    const before = await page
      .locator("tbody tr td.name a")
      .first()
      .getAttribute("href")
      .catch(() => null);
    await page.evaluate((targetText) => {
      const items = Array.from(document.querySelectorAll(".order-group li"));
      const item = items.find((node) => (node.textContent || "").trim() === targetText);
      item?.click();
    }, DATE_SORT_TEXT);
    await page.waitForTimeout(1500);
    await page
      .waitForFunction(
        (previousHref) =>
          (document.querySelector("tbody tr td.name a")?.getAttribute("href") || null) !==
          previousHref,
        before,
        { timeout: 10000 },
      )
      .catch(() => {});
  }
  return false;
}

async function extractResults(page) {
  return page.evaluate(() =>
    Array.from(document.querySelectorAll("tbody tr")).map((row) => ({
      title: (row.querySelector("td.name a")?.textContent || "").trim().replace(/\s+/g, " "),
      url: row.querySelector("td.name a")?.href || "",
      authors: Array.from(row.querySelectorAll("td.author a"))
        .map((link) => (link.textContent || "").trim())
        .filter(Boolean),
      source: (row.querySelector("td.source")?.textContent || "")
        .trim()
        .replace(/\s+/g, " "),
      publishDate: (row.querySelector("td.date")?.textContent || "").trim(),
      database: (row.querySelector("td.data")?.textContent || "").trim(),
      cited: (row.querySelector("td.cite")?.textContent || "").trim(),
      download: (row.querySelector("td.download")?.textContent || "").trim(),
    })),
  );
}

async function nextPage(page) {
  const nextButton = page.locator("#Page_next_top").first();
  if ((await nextButton.count()) === 0) {
    return false;
  }
  const firstHref = await page
    .locator("tbody tr td.name a")
    .first()
    .getAttribute("href")
    .catch(() => null);
  await nextButton.click({ timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(1500);
  if (page.url().includes("/verify/home")) {
    const ok = await maybeSolveCaptcha(page);
    if (!ok) {
      throw new Error("CNKI captcha solve failed while moving to the next page.");
    }
  }
  await waitForResultRows(page);
  await page
    .waitForFunction(
      (previousHref) =>
        (document.querySelector("tbody tr td.name a")?.getAttribute("href") || null) !==
        previousHref,
      firstHref,
      { timeout: 15000 },
    )
    .catch(() => {});
  return true;
}

async function runCnkiQuery({
  kind,
  query,
  limit,
  maxPages = 1,
  exactSource = false,
  preferDateSort = false,
  strictAuth = false,
}) {
  const settings = await loadSettings();
  const cookie = resolveCredential(settings, "CNKI_COOKIE");
  const username = resolveCredential(settings, "CNKI_USERNAME");
  const password = resolveCredential(settings, "CNKI_PASSWORD");
  const field = kind === "journal" ? "LY" : "SU";
  const browserBundle = await launchCnkiBrowser();
  const authInfo = {
    mode: "anonymous",
    cookiesApplied: 0,
    accountAttempted: false,
  };
  try {
    if (cookie) {
      authInfo.cookiesApplied = await applyCookieAuth(browserBundle.context, cookie);
      authInfo.mode = "cookie";
    } else if (username && password) {
      authInfo.accountAttempted = true;
      try {
        await maybeLoginWithAccount(await browserBundle.context.newPage(), {
          username,
          password,
        });
        authInfo.mode = "account";
      } catch (error) {
        if (strictAuth) {
          throw error;
        }
        authInfo.mode = "anonymous";
        authInfo.accountError = error.message;
      }
    }
    const page = await browserBundle.context.newPage();
    const searchUrl = `https://kns.cnki.net/kns8s/defaultresult/index?korder=${field}&kw=${encodeURIComponent(
      query,
    )}`;
    await page.goto(searchUrl, { waitUntil: "domcontentloaded", timeout: 30000 });
    if (page.url().includes("/verify/home")) {
      const solved = await maybeSolveCaptcha(page);
      if (!solved) {
        throw new Error("CNKI slider verification could not be solved automatically.");
      }
    }
    await waitForResultRows(page);
    if (preferDateSort) {
      await maybeSortByDate(page);
      await waitForResultRows(page);
    }
    const items = [];
    let currentPage = 1;
    while (currentPage <= maxPages && items.length < limit) {
      const pageItems = await extractResults(page);
      let filtered = pageItems;
      if (kind === "topic") {
        filtered = filtered.filter((item) => PAPER_DATABASES.has(item.database));
      } else {
        filtered = filtered.filter((item) => item.database === "期刊");
        if (exactSource) {
          const target = normalizeComparable(query);
          filtered = filtered.filter(
            (item) => normalizeComparable(item.source) === target,
          );
        }
      }
      for (const item of filtered) {
        const normalizedTitle = cleanText(item.title);
        if (!normalizedTitle || items.some((existing) => existing.url === item.url)) {
          continue;
        }
        items.push({
          recordId: item.url ? digest(item.url).slice(0, 16) : null,
          title: normalizedTitle,
          authors: item.authors,
          source: cleanText(item.source),
          publishDate: cleanText(item.publishDate),
          database: cleanText(item.database),
          url: cleanText(item.url),
          matchedType: kind,
          matchedQuery: query,
        });
        if (items.length >= limit) {
          break;
        }
      }
      if (items.length >= limit || currentPage >= maxPages) {
        break;
      }
      const moved = await nextPage(page);
      if (!moved) {
        break;
      }
      currentPage += 1;
    }
    return {
      auth: authInfo,
      query,
      kind,
      exactSource,
      results: items.slice(0, limit),
      retrievedAt: nowIso(),
    };
  } finally {
    await browserBundle.context.close().catch(() => {});
    await browserBundle.browser.close().catch(() => {});
  }
}

function formatRecords(records, header) {
  if (records.length === 0) {
    return `${header}\n未找到匹配结果。`;
  }
  const lines = [header];
  records.forEach((record, index) => {
    lines.push(`${index + 1}. ${record.title}`);
    lines.push(`来源：${record.source || "未知"} | 日期：${record.publishDate || "未知"}`);
    if (record.authors?.length) {
      lines.push(`作者：${record.authors.join("；")}`);
    }
    lines.push(`链接：${record.url}`);
  });
  return lines.join("\n");
}

function formatQueryResult(result) {
  if (result.kind === "journal") {
    return formatRecords(
      result.results,
      `CNKI 期刊检索：${result.query}（精确来源匹配）`,
    );
  }
  return formatRecords(result.results, `CNKI 主题检索：${result.query}`);
}

function normalizeRecordForJson(record) {
  return {
    record_id: record.recordId || "",
    title: cleanText(record.title),
    authors: Array.isArray(record.authors) ? record.authors : cleanText(record.authors),
    source: cleanText(record.source),
    publish_date: cleanText(record.publishDate),
    database: cleanText(record.database),
    url: cleanText(record.url),
    matched_type: cleanText(record.matchedType),
    matched_query: cleanText(record.matchedQuery),
  };
}

function normalizeQueryPayload(result) {
  return {
    ok: true,
    type: result.kind,
    query: result.query,
    count: result.results.length,
    records: result.results.map(normalizeRecordForJson),
    retrieved_at: result.retrievedAt,
    auth: result.auth,
  };
}

function formatSubscriptionMessage(subscription, newRecords, truncatedCount) {
  const kindLabel = subscription.kind === "journal" ? "期刊订阅" : "主题订阅";
  const header = `【CNKI${kindLabel}】${subscription.query} 新增 ${newRecords.length} 条`;
  const body = formatRecords(newRecords, header);
  if (truncatedCount > 0) {
    return `${body}\n另有 ${truncatedCount} 条未展开。`;
  }
  return body;
}

async function runCommand(command, args, options = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      cwd: options.cwd || process.cwd(),
      env: options.env || process.env,
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    child.on("error", reject);
    child.on("close", (code) => {
      if (code === 0) {
        resolve({ stdout, stderr });
        return;
      }
      reject(new Error(`${command} ${args.join(" ")} failed (${code}): ${stderr || stdout}`));
    });
  });
}

async function openClawCall(args) {
  return runCommand("openclaw", args);
}

async function injectMessage(message, sessionKey = "main", label = "CNKI Watch") {
  const settings = await loadSettings();
  const gatewayArgs = [
    "gateway",
    "call",
    "--json",
    "--url",
    `ws://127.0.0.1:${settings.gateway.port || 18789}`,
  ];
  if (settings.gateway.token) {
    gatewayArgs.push("--token", settings.gateway.token);
  }
  gatewayArgs.push(
    "--params",
    JSON.stringify({ sessionKey, message, label }, null, 0),
    "chat.inject",
  );
  await openClawCall(gatewayArgs);
}

function parseSchedule(scheduleString, timezone) {
  const parsed = parseScheduleSpec(scheduleString, timezone);
  if (parsed.kind === "every") {
    return { mode: "every", every: parsed.cliArgs[1], timezone, normalized: parsed.normalized };
  }
  if (parsed.kind === "at") {
    return { mode: "at", at: parsed.cliArgs[1], timezone, normalized: parsed.normalized };
  }
  return {
    mode: "cron",
    cron: parsed.cliArgs[1],
    timezone,
    exact: parsed.cliArgs.includes("--exact"),
    normalized: parsed.normalized,
  };
}

function buildCronPrompt(subscription) {
  const containerScriptPath = path.join(
    os.homedir(),
    ".openclaw",
    "workspace",
    "skills",
    SKILL_KEY,
    "scripts",
    "cnki_watch.mjs",
  );
  return [
    `Run this command exactly once and do not ask follow-up questions:`,
    `node ${containerScriptPath} run-subscription --id ${subscription.id} --session-key ${subscription.sessionKey}`,
    `Do not modify the command.`,
  ].join("\n");
}

async function createCronJob(subscription) {
  const parsedSchedule = parseSchedule(subscription.schedule, subscription.timezone);
  const args = [
    "cron",
    "add",
    "--json",
    "--name",
    `cnki-watch-${slugify(subscription.query)}-${subscription.id.slice(0, 8)}`,
    "--description",
    `CNKI ${subscription.kind} subscription for ${subscription.query}`,
    "--session",
    "isolated",
    "--no-deliver",
    "--thinking",
    "minimal",
    "--timeout-seconds",
    "1800",
    "--message",
    buildCronPrompt(subscription),
  ];
  if (parsedSchedule.mode === "every") {
    args.push("--every", parsedSchedule.every);
  } else if (parsedSchedule.mode === "at") {
    args.push("--at", parsedSchedule.at);
  } else {
    args.push("--cron", parsedSchedule.cron);
    if (parsedSchedule.timezone) {
      args.push("--tz", parsedSchedule.timezone);
    }
    if (parsedSchedule.exact) {
      args.push("--exact");
    }
  }
  const { stdout } = await openClawCall(args);
  const payload = JSON.parse(stdout);
  return payload.job?.id || payload.id || null;
}

async function removeCronJob(cronJobId) {
  if (!cronJobId) {
    return;
  }
  await openClawCall(["cron", "rm", "--json", cronJobId]);
}

async function forceRunCronJob(cronJobId) {
  if (!cronJobId) {
    throw new Error("Cron job id is required.");
  }
  await openClawCall(["cron", "run", cronJobId]);
}

async function handleQuery(kind, args) {
  const settings = await loadSettings();
  const name = resolveQueryArg(kind, args);
  if (!name) {
    throw new Error(`Missing --${kind === "journal" ? "journal" : "topic"}.`);
  }
  const limit =
    toInt(args.limit, kind === "journal" ? settings.config.maxManualResults : settings.config.maxManualResults) ||
    DEFAULTS.maxManualResults;
  const result = await runCnkiQuery({
    kind,
    query: name,
    limit,
    maxPages: kind === "journal" ? 6 : 2,
    exactSource: kind === "journal",
    preferDateSort: kind === "journal",
  });
  if (args.json) {
    console.log(JSON.stringify(normalizeQueryPayload(result), null, 2));
    return;
  }
  console.log(formatQueryResult(result));
}

async function handleAuthCheck(args) {
  const settings = await loadSettings();
  const cookie = resolveCredential(settings, "CNKI_COOKIE");
  const username = resolveCredential(settings, "CNKI_USERNAME");
  const password = resolveCredential(settings, "CNKI_PASSWORD");
  const browserBundle = await launchCnkiBrowser();
  const summary = {
    cookieConfigured: Boolean(cookie),
    accountConfigured: Boolean(username && password),
    mode: "anonymous",
    cookiesApplied: 0,
    accountLogin: null,
    queryReady: false,
  };
  try {
    if (cookie) {
      summary.cookiesApplied = await applyCookieAuth(browserBundle.context, cookie);
      summary.mode = "cookie";
    }
    const page = await browserBundle.context.newPage();
    if (!cookie && username && password) {
      try {
        summary.accountLogin = await maybeLoginWithAccount(page, { username, password });
        summary.mode = "account";
      } catch (error) {
        summary.accountLogin = { used: true, success: false, detail: error.message };
        if (args.strict) {
          throw error;
        }
      }
    } else {
      await page.goto("https://www.cnki.net/", { waitUntil: "domcontentloaded", timeout: 30000 });
    }
    const probe = await runCnkiQuery({
      kind: "topic",
      query: cleanText(args.probe || "人工智能"),
      limit: 1,
      maxPages: 1,
      exactSource: false,
      preferDateSort: false,
      strictAuth: Boolean(args.strict),
    });
    summary.queryReady = probe.results.length >= 0;
    if (args.json) {
      console.log(JSON.stringify(summary, null, 2));
      return;
    }
    console.log(
      [
        "CNKI auth check",
        `mode: ${summary.mode}`,
        `cookieConfigured: ${summary.cookieConfigured ? "yes" : "no"}`,
        `accountConfigured: ${summary.accountConfigured ? "yes" : "no"}`,
        `queryReady: ${summary.queryReady ? "yes" : "no"}`,
        summary.accountLogin ? `accountLogin: ${summary.accountLogin.success ? "ok" : summary.accountLogin.detail}` : null,
      ]
        .filter(Boolean)
        .join("\n"),
    );
  } finally {
    await browserBundle.context.close().catch(() => {});
    await browserBundle.browser.close().catch(() => {});
  }
}

async function createSubscription(kind, args) {
  const settings = await loadSettings();
  const query = resolveQueryArg(kind, args);
  if (!query) {
    throw new Error(`Missing --${kind === "journal" ? "journal" : "topic"}.`);
  }
  const schedule = cleanText(args.schedule || settings.config.defaultSchedule);
  const timezone = cleanText(args.timezone || settings.config.timezone || DEFAULTS.timezone);
  const sessionKey = cleanText(args["session-key"] || "main");
  const state = await loadState();
  const existing = state.subscriptions.find(
    (item) =>
      item.kind === kind &&
      normalizeComparable(item.query) === normalizeComparable(query) &&
      item.schedule === schedule,
  );
  if (existing) {
    if (args.json) {
      console.log(
        JSON.stringify(
          {
            ok: true,
            reused: true,
            subscription: existing,
          },
          null,
          2,
        ),
      );
      return;
    }
    console.log(`Subscription already exists: ${existing.id}`);
    return;
  }
  const preview = await runCnkiQuery({
    kind,
    query,
    limit: kind === "journal" ? 5 : 5,
    maxPages: kind === "journal" ? 6 : 2,
    exactSource: kind === "journal",
    preferDateSort: kind === "journal",
  });
  if (preview.results.length === 0) {
    throw new Error(`No CNKI results found for ${query}.`);
  }
  const subscription = {
    id: randomUUID(),
    kind,
    query,
    schedule,
    timezone,
    sessionKey,
    createdAt: nowIso(),
    updatedAt: nowIso(),
    lastRunAt: null,
    lastSuccessAt: null,
    lastError: null,
    seenKeys: preview.results.map((record) => recordKey(record)),
    cronJobId: null,
  };
  subscription.cronJobId = await createCronJob(subscription);
  state.subscriptions.push(subscription);
  await saveState(state);
  if (args.json) {
    console.log(
      JSON.stringify(
        {
          ok: true,
          subscription,
        },
        null,
        2,
      ),
    );
    return;
  }
  console.log(
    [
      `Created ${kind} subscription ${subscription.id}`,
      `query: ${query}`,
      `schedule: ${schedule} (${timezone})`,
      `cronJobId: ${subscription.cronJobId || "unknown"}`,
      `seededSeenRecords: ${subscription.seenKeys.length}`,
    ].join("\n"),
  );
}

async function handleListSubscriptions(args) {
  const state = await loadState();
  if (args.json) {
    console.log(JSON.stringify(state.subscriptions, null, 2));
    return;
  }
  if (state.subscriptions.length === 0) {
    console.log("No subscriptions.");
    return;
  }
  const lines = [];
  for (const subscription of state.subscriptions) {
    lines.push(
      [
        `${subscription.id}`,
        `type=${subscription.kind}`,
        `query=${subscription.query}`,
        `schedule=${subscription.schedule}`,
        `cron=${subscription.cronJobId || "-"}`,
        `lastRun=${subscription.lastRunAt || "-"}`,
      ].join(" | "),
    );
  }
  console.log(lines.join("\n"));
}

async function handleUnsubscribe(args) {
  const id = cleanText(args.id || args._[1] || "");
  if (!id) {
    throw new Error("Missing --id.");
  }
  const state = await loadState();
  const subscription = findSubscription(state, id);
  if (!subscription) {
    throw new Error(`Subscription not found: ${id}`);
  }
  await removeCronJob(subscription.cronJobId).catch(() => {});
  state.subscriptions = state.subscriptions.filter((item) => item.id !== id);
  await saveState(state);
  if (args.json) {
    console.log(
      JSON.stringify(
        {
          ok: true,
          removed: id,
          cron_job_id: subscription.cronJobId || null,
        },
        null,
        2,
      ),
    );
    return;
  }
  console.log(`Removed subscription ${id}`);
}

async function executeSubscription(subscription, args = {}) {
  const settings = await loadSettings();
  const limit = settings.config.maxPushResults;
  const result = await runCnkiQuery({
    kind: subscription.kind,
    query: subscription.query,
    limit: limit + 20,
    maxPages: subscription.kind === "journal" ? 6 : 2,
    exactSource: subscription.kind === "journal",
    preferDateSort: true,
  });
  const seen = new Set(subscription.seenKeys || []);
  const newRecords = [];
  for (const record of result.results) {
    const key = recordKey(record);
    if (seen.has(key)) {
      continue;
    }
    newRecords.push({ ...record, dedupeKey: key });
  }
  subscription.lastRunAt = nowIso();
  subscription.updatedAt = nowIso();
  subscription.lastError = null;
  if (newRecords.length === 0) {
    return { delivered: false, newCount: 0, message: "NO_UPDATE" };
  }
  const deliverable = newRecords.slice(0, limit);
  const truncatedCount = Math.max(0, newRecords.length - deliverable.length);
  for (const record of newRecords) {
    seen.add(record.dedupeKey);
  }
  subscription.seenKeys = Array.from(seen).slice(-5000);
  subscription.lastSuccessAt = nowIso();
  const message = formatSubscriptionMessage(subscription, deliverable, truncatedCount);
  await injectMessage(message, cleanText(args["session-key"] || subscription.sessionKey || "main"));
  return {
    delivered: true,
    newCount: newRecords.length,
    sentCount: deliverable.length,
    truncatedCount,
    message,
  };
}

async function handleRunSubscription(args) {
  const id = cleanText(args.id || args._[1] || "");
  if (!id) {
    throw new Error("Missing --id.");
  }
  const state = await loadState();
  const subscription = findSubscription(state, id);
  if (!subscription) {
    throw new Error(`Subscription not found: ${id}`);
  }
  try {
    const result = await executeSubscription(subscription, args);
    await saveState(state);
    if (args.json) {
      console.log(JSON.stringify(result, null, 2));
      return;
    }
    console.log(result.message);
  } catch (error) {
    subscription.lastRunAt = nowIso();
    subscription.updatedAt = nowIso();
    subscription.lastError = error.message;
    await saveState(state);
    if (!args.json) {
      const sessionKey = cleanText(args["session-key"] || subscription.sessionKey || "main");
      await injectMessage(
        `【CNKI订阅运行失败】${subscription.query}\n错误：${error.message}`,
        sessionKey,
      ).catch(() => {});
    }
    throw error;
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];
  if (!command || args.help) {
    console.log(usage());
    return;
  }
  await ensureRuntimeDir();
  switch (command) {
    case "auth-check":
      await handleAuthCheck(args);
      return;
    case "query-topic":
      await handleQuery("topic", args);
      return;
    case "query-journal":
      await handleQuery("journal", args);
      return;
    case "subscribe-topic":
      await createSubscription("topic", args);
      return;
    case "subscribe-journal":
      await createSubscription("journal", args);
      return;
    case "list-subscriptions":
      await handleListSubscriptions(args);
      return;
    case "unsubscribe":
      await handleUnsubscribe(args);
      return;
    case "run-subscription":
      await handleRunSubscription(args);
      return;
    case "run-cron-now": {
      const id = cleanText(args.id || args._[1] || "");
      if (!id) {
        throw new Error("Missing --id.");
      }
      const state = await loadState();
      const subscription = findSubscription(state, id);
      if (!subscription || !subscription.cronJobId) {
        throw new Error(`Cron job not found for subscription: ${id}`);
      }
      await forceRunCronJob(subscription.cronJobId);
      console.log(`Triggered cron job ${subscription.cronJobId}`);
      return;
    }
    default:
      throw new Error(`Unknown command: ${command}`);
  }
}

main().catch((error) => {
  console.error(`cnki-watch error: ${error.message}`);
  process.exitCode = 1;
});
