#!/usr/bin/env node

import { chromium } from "playwright-core";

const args = process.argv.slice(2);

function getArg(name, fallback = null) {
  const index = args.indexOf(name);
  if (index === -1) return fallback;
  return args[index + 1] ?? fallback;
}

const mode = getArg("--mode");
const debugPort = Number(getArg("--debug-port", "9222"));
const pageUrl = getArg("--page-url");
const requestUrl = getArg("--request-url");
const method = getArg("--method", "GET");
const headers = JSON.parse(getArg("--headers-json", "{}"));
const payloadJson = getArg("--payload-json");
const payload = payloadJson ? JSON.parse(payloadJson) : null;
const expression = getArg("--expression");
const timeoutSeconds = Number(getArg("--timeout-seconds", "30"));
const forceNavigate = getArg("--force-navigate", "false") === "true";

if (!mode || !pageUrl) {
  console.error("Missing required arguments");
  process.exit(1);
}

async function connectBrowser() {
  return chromium.connectOverCDP(`http://127.0.0.1:${debugPort}`);
}

function pageMatches(page, expectedUrl) {
  const url = String(page.url() || "");
  return url.startsWith(expectedUrl);
}

function pageMatchesFamily(page, expectedUrl) {
  const url = String(page.url() || "");
  if (url.startsWith(expectedUrl)) return true;
  if (expectedUrl.includes("/jobs/")) {
    return url.includes("alpha.midjourney.com/jobs/");
  }
  return false;
}

async function getOrCreatePage(browser, expectedUrl) {
  const contexts = browser.contexts();
  for (const context of contexts) {
    for (const page of context.pages()) {
      if (pageMatches(page, expectedUrl)) return page;
    }
  }
  for (const context of contexts) {
    for (const page of context.pages()) {
      if (pageMatchesFamily(page, expectedUrl)) return page;
    }
  }
  const context = contexts[0] || (await browser.newContext());
  return context.newPage();
}

async function assertNoSecurityChallenge(page) {
  const probe = await page.evaluate(() => ({
    href: location.href,
    title: document.title,
    body: document.body && document.body.innerText ? document.body.innerText.slice(0, 1000) : "",
  }));
  const haystack = `${probe.href || ""}\n${probe.title || ""}\n${probe.body || ""}`.toLowerCase();
  const markers = [
    "verify you are human",
    "performing security verification",
    "just a moment",
    "cloudflare",
    "security service to protect against malicious bots",
  ];
  if (markers.some((marker) => haystack.includes(marker))) {
    throw new Error("Cloudflare challenge detected on the active Midjourney page. Resolve it manually in Chrome, then retry.");
  }
}

async function ensurePageReady(page, expectedUrl) {
  if (forceNavigate || !page.url().startsWith(expectedUrl)) {
    await page.goto(expectedUrl, {
      waitUntil: "domcontentloaded",
      timeout: timeoutSeconds * 1000,
    });
  }
  await assertNoSecurityChallenge(page);
}

async function runFetch(page) {
  if (!requestUrl) {
    throw new Error("--request-url is required for fetch mode");
  }
  const result = await page.evaluate(
    async ({ requestUrl: targetUrl, requestMethod, requestHeaders, requestBody }) => {
      try {
        const response = await fetch(targetUrl, {
          method: requestMethod,
          headers: requestHeaders,
          credentials: "include",
          body: requestBody ? JSON.stringify(requestBody) : undefined,
        });
        const text = await response.text();
        return {
          ok: response.ok,
          status: response.status,
          text,
        };
      } catch (error) {
        return {
          ok: false,
          status: 0,
          text: "",
          error: String(error),
        };
      }
    },
    {
      requestUrl,
      requestMethod: method,
      requestHeaders: headers,
      requestBody: payload,
    },
  );
  if (!result?.ok) {
    throw new Error(`${result?.error || `HTTP ${result?.status}`}: ${String(result?.text || "").slice(0, 500)}`);
  }
  process.stdout.write(result.text);
}

async function runEval(page) {
  if (!expression) {
    throw new Error("--expression is required for eval mode");
  }
  const value = await page.evaluate(({ source }) => {
    // Local bridge for trusted local expressions only.
    return eval(source);
  }, { source: expression });
  process.stdout.write(JSON.stringify(value));
}

async function main() {
  const browser = await connectBrowser();
  try {
    const page = await getOrCreatePage(browser, pageUrl);
    page.setDefaultTimeout(timeoutSeconds * 1000);
    await ensurePageReady(page, pageUrl);
    if (mode === "fetch") {
      await runFetch(page);
      return;
    }
    if (mode === "eval") {
      await runEval(page);
      return;
    }
    throw new Error(`Unsupported mode: ${mode}`);
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error.message || String(error));
  process.exit(1);
});
