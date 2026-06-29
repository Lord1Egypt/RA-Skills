#!/usr/bin/env node
import { realpathSync } from "node:fs";
import { access, mkdir, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { performance } from "node:perf_hooks";
import { fileURLToPath } from "node:url";
import { chromium as playwrightChromium } from "playwright";
import { chromium as playwrightExtraChromium } from "playwright-extra";
import StealthPlugin from "puppeteer-extra-plugin-stealth";

export const EXIT_OK = 0;
export const EXIT_UNACCEPTABLE_FETCH = 1;
export const EXIT_USAGE = 2;
export const EXIT_RUNTIME_ERROR = 3;

const VALUE_OPTIONS = new Map([
  ["--timeout", "timeout"],
  ["--user-agent", "userAgent"],
  ["--proxy-server", "proxyServer"],
  ["--chromium-path", "chromiumPath"],
  ["--wait-until", "waitUntil"],
  ["--selector", "selector"],
  ["--output", "output"],
  ["-o", "output"],
  ["--metadata", "metadata"]
]);

const FLAG_OPTIONS = new Map([
  ["--help", "help"],
  ["-h", "help"],
  ["--html", "html"],
  ["--text", "text"],
  ["--json", "json"],
  ["--include-metadata", "includeMetadata"],
  ["--no-stealth", "noStealth"],
  ["--fail", "fail"]
]);

const ALLOWED_WAIT_UNTIL = new Set(["domcontentloaded", "load", "networkidle"]);
const OPTIONAL_ERROR_FIELDS = [
  "error_message",
  "error_name",
  "error_cause_code",
  "error_cause_name",
  "error_cause_message"
];

const STRONG_BLOCKED_PATTERNS = [
  /captcha required/i,
  /complete the captcha/i,
  /solve the captcha/i,
  /please verify (that )?you are (a )?human/i,
  /unusual traffic/i,
  /robot check/i,
  /you have been blocked/i,
  /cloudflare ray id/i,
  /wikimedia error/i
];

const SOFT_BLOCKED_PATTERNS = [
  /automated requests/i,
  /rate limit/i,
  /too many requests/i
];

const DEFAULT_USER_AGENT =
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36";

if (isDirectRun()) {
  process.exitCode = await main(process.argv.slice(2));
}

export async function main(argv, io = defaultIo()) {
  let args;
  try {
    args = parseArgs(argv);
  } catch (error) {
    io.stderr.write(`${error instanceof Error ? error.message : String(error)}\n\n`);
    printHelp(io.stderr);
    return EXIT_USAGE;
  }

  if (args.help) {
    printHelp(io.stdout);
    return EXIT_OK;
  }

  const record = await runBrowserFetch(args);
  const metadata = buildMetadata(record);
  if (args.metadata) {
    await writeMetadata(args.metadata, metadata);
  }
  if (args.includeMetadata) {
    io.stderr.write(`${JSON.stringify(metadata)}\n`);
  }

  const content = record.content || "";
  if (args.json) {
    io.stdout.write(`${JSON.stringify(buildJsonResult(record), null, 2)}\n`);
  } else if (args.output) {
    await writeContent(args.output, content);
  } else {
    io.stdout.write(content);
    if (content && !content.endsWith("\n")) {
      io.stdout.write("\n");
    }
  }

  return exitCodeForRecord(record, args);
}

export function parseArgs(argv) {
  const parsed = {
    timeout: 15000,
    waitUntil: "domcontentloaded",
    selector: "body"
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (VALUE_OPTIONS.has(arg)) {
      const key = VALUE_OPTIONS.get(arg);
      const value = argv[index + 1];
      if (!value || value.startsWith("-")) {
        throw new Error(`${arg} requires a value`);
      }
      parsed[key] = value;
      index += 1;
      continue;
    }
    if (FLAG_OPTIONS.has(arg)) {
      parsed[FLAG_OPTIONS.get(arg)] = true;
      continue;
    }
    if (arg.startsWith("-")) {
      throw new Error(`unknown option: ${arg}`);
    }
    if (parsed.url) {
      throw new Error(`unexpected argument: ${arg}`);
    }
    parsed.url = arg;
  }

  if (!parsed.help && !parsed.url) {
    throw new Error("url is required");
  }
  if (parsed.json && parsed.output) {
    throw new Error("--json and --output are mutually exclusive");
  }
  if (parsed.html && parsed.text) {
    throw new Error("--html and --text are mutually exclusive");
  }
  parsed.timeout = Number(parsed.timeout);
  if (!Number.isFinite(parsed.timeout) || parsed.timeout <= 0) {
    throw new Error("--timeout must be a positive number");
  }
  if (!ALLOWED_WAIT_UNTIL.has(parsed.waitUntil)) {
    throw new Error("--wait-until must be one of: domcontentloaded, load, networkidle");
  }

  return parsed;
}

export async function runBrowserFetch(args) {
  const startedAt = performance.now();
  const proxyServer = args.proxyServer || resolveProxyServer();
  const base = {
    url: args.url,
    proxy_enabled: Boolean(proxyServer),
    proxy_server: proxyServer || null,
    stealth_enabled: !args.noStealth
  };

  try {
    const result = await browserFetch({
      url: args.url,
      timeoutMs: args.timeout,
      userAgent: args.userAgent,
      proxyServer,
      chromiumPath: args.chromiumPath,
      stealthEnabled: !args.noStealth,
      waitUntil: args.waitUntil,
      selector: args.selector,
      contentMode: args.html ? "html" : "text",
      includeContent: true
    });
    const classified = classifyFailure({
      status: result.status,
      text: result.text,
      error: null
    });
    const ok = result.ok && !classified.blocked_signal;
    return {
      ...base,
      ...result,
      ok,
      error_type: ok ? "ok" : classified.error_type,
      blocked_signal: classified.blocked_signal,
      duration_ms: Math.round(performance.now() - startedAt)
    };
  } catch (error) {
    return runtimeErrorRecord(args, error, {
      proxyServer,
      durationMs: Math.round(performance.now() - startedAt)
    });
  }
}

export function runtimeErrorRecord(args, error, { proxyServer = null, durationMs = 0 } = {}) {
  const classified = classifyFailure({ error });
  const stealthEnabled = !args.noStealth;
  return {
    url: args.url,
    proxy_enabled: Boolean(proxyServer),
    proxy_server: proxyServer || null,
    stealth_enabled: stealthEnabled,
    status: null,
    ok: false,
    error_type: classified.error_type,
    blocked_signal: classified.blocked_signal,
    duration_ms: durationMs,
    bytes: 0,
    final_url: null,
    method: methodForStealth(stealthEnabled),
    content: "",
    error_message: error instanceof Error ? error.message : String(error),
    error_name: error instanceof Error ? error.name : null,
    error_cause_code: error?.cause?.code || null,
    error_cause_name: error?.cause?.name || null,
    error_cause_message: error?.cause?.message || null
  };
}

export async function browserFetch(options) {
  const ownsBrowser = !options.browser;
  const waitUntil = options.waitUntil || options.wait_until || "domcontentloaded";
  const contentMode = options.contentMode || options.content_mode || "text";
  const includeContent = Boolean(options.includeContent || options.include_content);
  const selector = options.selector || "body";
  const browser =
    options.browser ||
    (await launchBrowser({
      proxyServer: options.proxyServer,
      chromiumPath: options.chromiumPath,
      stealthEnabled: options.stealthEnabled ?? options.stealth_enabled ?? true,
      headless: options.headless
    }));
  const stealthEnabled = Boolean(options.stealthEnabled ?? options.stealth_enabled ?? true);
  try {
    for (let attempt = 1; attempt <= 2; attempt += 1) {
      try {
        return await browserFetchAttempt({
          browser,
          url: options.url,
          waitUntil,
          timeoutMs: Number(options.timeoutMs || options.timeout_ms || 15000),
          userAgent: options.userAgent,
          contentMode,
          includeContent,
          selector,
          stealthEnabled
        });
      } catch (error) {
        if (attempt === 2 || !isRetryableNavigationError(error)) {
          throw error;
        }
      }
    }
  } finally {
    if (ownsBrowser) {
      await browser.close().catch(() => undefined);
    }
  }
}

export async function launchBrowser({ proxyServer, chromiumPath, stealthEnabled = true, headless = true } = {}) {
  const executablePath = chromiumPath || (await resolveChromiumPath());
  const chromium = resolveChromium({ stealthEnabled });
  return chromium.launch({
    executablePath,
    headless,
    proxy: proxyServer ? { server: proxyServer } : undefined,
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
      "--disable-gpu",
      "--disable-background-networking",
      "--disable-default-apps",
      "--disable-extensions"
    ]
  });
}

export async function resolveChromiumPath() {
  const candidates = [
    process.env.CHROMIUM_PATH,
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable"
  ].filter(Boolean);
  for (const candidate of candidates) {
    try {
      await access(candidate);
      return candidate;
    } catch {
      // Keep looking.
    }
  }
  return undefined;
}

export function resolveProxyServer(env = process.env) {
  return (
    firstNonEmpty(
      env.FETCH_PROXY_SERVER,
      shouldUseEnvProxy(env) ? env.HTTPS_PROXY : "",
      shouldUseEnvProxy(env) ? env.https_proxy : "",
      shouldUseEnvProxy(env) ? env.HTTP_PROXY : "",
      shouldUseEnvProxy(env) ? env.http_proxy : ""
    ) || null
  );
}

export function classifyFailure({ status, text = "", error } = {}) {
  if (error) {
    const message = error instanceof Error ? error.message : String(error);
    const causeCode = String(error?.cause?.code || "");
    const causeMessage = String(error?.cause?.message || "");
    const combined = `${message} ${causeCode} ${causeMessage}`;
    if (
      /abort|timeout|timed out|ETIMEDOUT|UND_ERR_CONNECT_TIMEOUT/i.test(combined) ||
      /ERR_TIMED_OUT/i.test(combined) ||
      error.name === "TimeoutError" ||
      error.name === "AbortError"
    ) {
      return { error_type: "timeout", blocked_signal: false };
    }
    if (/ENOTFOUND|EAI_AGAIN|DNS/i.test(combined)) {
      return { error_type: "dns", blocked_signal: false };
    }
    if (/TLS|certificate|SSL/i.test(combined)) {
      return { error_type: "tls", blocked_signal: false };
    }
    if (/proxy/i.test(combined)) {
      return { error_type: "proxy", blocked_signal: false };
    }
    if (/ECONN|socket|connect|network|fetch failed/i.test(combined)) {
      return { error_type: "connection", blocked_signal: false };
    }
    if (/browser|chromium|playwright|target page|context/i.test(combined)) {
      return { error_type: "browser", blocked_signal: false };
    }
    return { error_type: "unknown", blocked_signal: false };
  }
  if ([403, 429, 503].includes(Number(status))) {
    return { error_type: "blocked_http", blocked_signal: true };
  }
  if (Number(status) >= 400) {
    return { error_type: "http_error", blocked_signal: false };
  }
  if (STRONG_BLOCKED_PATTERNS.some((pattern) => pattern.test(text || ""))) {
    return { error_type: "blocked_content", blocked_signal: true };
  }
  if (String(text || "").length < 60000 && SOFT_BLOCKED_PATTERNS.some((pattern) => pattern.test(text || ""))) {
    return { error_type: "blocked_content", blocked_signal: true };
  }
  return { error_type: "ok", blocked_signal: false };
}

export function buildMetadata(record) {
  const metadata = {
    ok: Boolean(record.ok),
    status: record.status,
    url: record.url,
    final_url: record.final_url,
    method: record.method || "playwright-chromium",
    bytes: record.bytes,
    duration_ms: record.duration_ms,
    error_type: record.error_type,
    blocked_signal: Boolean(record.blocked_signal),
    stealth_enabled: Boolean(record.stealth_enabled),
    proxy_enabled: Boolean(record.proxy_enabled),
    proxy_server: record.proxy_server
  };

  for (const field of OPTIONAL_ERROR_FIELDS) {
    if (record[field] !== undefined && record[field] !== null) {
      metadata[field] = record[field];
    }
  }

  return metadata;
}

export function buildJsonResult(record) {
  return { ...buildMetadata(record), content: record.content || "" };
}

export async function writeMetadata(path, metadata) {
  await writeJsonFile(path, metadata);
}

export function exitCodeForRecord(record, args = {}) {
  if (!record.ok && record.status === null) {
    return EXIT_RUNTIME_ERROR;
  }
  if (record.blocked_signal) {
    return EXIT_UNACCEPTABLE_FETCH;
  }
  if (args.fail && Number(record.status) >= 400) {
    return EXIT_UNACCEPTABLE_FETCH;
  }
  return EXIT_OK;
}

export function printHelp(stream = process.stdout) {
  stream.write(`usage: browser-fetch <url> [options]

Options:
  --timeout MS           Navigation timeout in milliseconds (default: 15000)
  --user-agent VALUE     Override the browser user agent
  --proxy-server URL     Proxy server for this request
  --chromium-path PATH   Chromium executable path
  --no-stealth           Disable default stealth evasions
  --wait-until VALUE     domcontentloaded, load, or networkidle
  --selector CSS         CSS selector for text extraction (default: body)
  --html                 Output full page HTML
  --text                 Output extracted page text (default)
  --json                 Output JSON metadata plus content
  --output PATH, -o PATH Write content to a file
  --metadata PATH        Write metadata JSON to a file
  --include-metadata     Write compact metadata JSON to stderr
  --fail                 Exit non-zero for HTTP status >= 400
  --help, -h             Show this help
`);
}

async function browserFetchAttempt({
  browser,
  url,
  waitUntil,
  timeoutMs,
  userAgent,
  contentMode,
  includeContent,
  selector,
  stealthEnabled
}) {
  const context = await browser.newContext({
    userAgent: userAgent || DEFAULT_USER_AGENT,
    ignoreHTTPSErrors: false
  });
  const page = await context.newPage();
  try {
    const response = await page.goto(url, {
      waitUntil,
      timeout: timeoutMs
    });
    const content =
      contentMode === "html"
        ? await page.content()
        : await page.locator(selector).textContent({ timeout: 2000 }).catch(() => page.content());
    const normalizedContent = content || "";
    const status = response ? response.status() : null;
    const result = {
      status,
      ok: status !== null && status >= 200 && status < 400,
      bytes: Buffer.byteLength(normalizedContent),
      final_url: page.url(),
      text: truncateForClassification(normalizedContent),
      method: methodForStealth(stealthEnabled),
      stealth_enabled: Boolean(stealthEnabled)
    };
    if (includeContent) {
      result.content = normalizedContent;
    }
    return result;
  } finally {
    await page.close().catch(() => undefined);
    await context.close().catch(() => undefined);
  }
}

async function writeContent(path, content) {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, content, "utf8");
}

async function writeJsonFile(path, payload) {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function isRetryableNavigationError(error) {
  const message = error instanceof Error ? error.message : String(error);
  return (
    /page\.goto/i.test(message) &&
    (/net::ERR_(CONNECTION_CLOSED|SOCKET_NOT_CONNECTED)/i.test(message) ||
      /timeout|timed out/i.test(message) ||
      error?.name === "TimeoutError")
  );
}

function shouldUseEnvProxy(env) {
  return String(env.FETCH_USE_ENV_PROXY || "").trim() !== "0";
}

function truncateForClassification(text) {
  return String(text || "").slice(0, 200000);
}

function resolveChromium({ stealthEnabled }) {
  if (!stealthEnabled) {
    return playwrightChromium;
  }
  if (!resolveChromium.stealthRegistered) {
    playwrightExtraChromium.use(StealthPlugin());
    resolveChromium.stealthRegistered = true;
  }
  return playwrightExtraChromium;
}

function methodForStealth(stealthEnabled) {
  return stealthEnabled ? "playwright-chromium-stealth" : "playwright-chromium";
}

function firstNonEmpty(...values) {
  for (const value of values) {
    if (typeof value === "string" && value.trim()) {
      return value.trim();
    }
  }
  return "";
}

function defaultIo() {
  return {
    stdout: process.stdout,
    stderr: process.stderr
  };
}

function isDirectRun() {
  if (!process.argv[1]) {
    return false;
  }
  return realpathSync(resolve(process.argv[1])) === realpathSync(fileURLToPath(import.meta.url));
}
