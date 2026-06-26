#!/usr/bin/env node

const args = process.argv.slice(2);

function getArg(name, fallback = null) {
  const index = args.indexOf(name);
  if (index === -1) return fallback;
  return args[index + 1] ?? fallback;
}

const debugPort = Number(getArg("--debug-port", "9222"));
const pageUrl = getArg("--page-url");
const expression = getArg("--expression");
const cookieHeader = getArg("--cookie-header", "");
const timeoutSeconds = Number(getArg("--timeout-seconds", "30"));
const forceNavigate = getArg("--force-navigate", "false") === "true";

if (!pageUrl || !expression) {
  console.error("Missing required arguments");
  process.exit(1);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const text = await response.text();
  return text ? JSON.parse(text) : {};
}

async function getOrCreatePageTarget() {
  const list = await fetchJson(`http://127.0.0.1:${debugPort}/json/list`);
  let target = list.find(
    (item) =>
      item.type === "page" &&
      String(item.url || "").startsWith(pageUrl),
  );
  if (target) return target;
  if (pageUrl.includes("/jobs/")) {
    target = list.find(
      (item) =>
        item.type === "page" &&
        String(item.url || "").includes("alpha.midjourney.com/jobs/"),
    );
    if (target) return target;
  }
  target = await fetchJson(`http://127.0.0.1:${debugPort}/json/new?${encodeURIComponent(pageUrl)}`, {
    method: "PUT",
  });
  await sleep(1500);
  return target;
}

function parseCookieHeader(cookieHeaderValue) {
  if (!cookieHeaderValue) return [];
  return cookieHeaderValue
    .split(";")
    .map((part) => part.trim())
    .filter(Boolean)
    .map((part) => {
      const eq = part.indexOf("=");
      return {
        name: part.slice(0, eq),
        value: part.slice(eq + 1),
      };
    });
}

class CDPClient {
  constructor(webSocketUrl) {
    this.socket = new WebSocket(webSocketUrl);
    this.nextId = 1;
    this.pending = new Map();
  }

  async open() {
    await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error("CDP websocket timeout")), 10000);
      this.socket.addEventListener("open", () => {
        clearTimeout(timer);
        resolve();
      });
      this.socket.addEventListener("error", (event) => {
        clearTimeout(timer);
        reject(new Error(String(event.message || "CDP websocket error")));
      });
    });

    this.socket.addEventListener("message", (event) => {
      const message = JSON.parse(event.data);
      if (message.id && this.pending.has(message.id)) {
        const { resolve, reject } = this.pending.get(message.id);
        this.pending.delete(message.id);
        if (message.error) reject(new Error(message.error.message || "CDP error"));
        else resolve(message.result);
      }
    });
  }

  send(methodName, params = {}) {
    const id = this.nextId++;
    const payload = JSON.stringify({ id, method: methodName, params });
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.socket.send(payload);
    });
  }

  close() {
    this.socket.close();
  }
}

async function assertNoSecurityChallenge(client) {
  const probeResult = await client.send("Runtime.evaluate", {
    expression: `
      (() => ({
        href: location.href,
        title: document.title,
        body: (document.body && document.body.innerText ? document.body.innerText.slice(0, 1000) : "")
      }))()
    `,
    returnByValue: true,
  });
  const probe = probeResult?.result?.value || {};
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

async function main() {
  const target = await getOrCreatePageTarget();
  const client = new CDPClient(target.webSocketDebuggerUrl);
  await client.open();
  await client.send("Page.enable");
  await client.send("Runtime.enable");
  await client.send("Network.enable");

  const cookies = parseCookieHeader(cookieHeader);
  for (const cookie of cookies) {
    const candidateParams = [];
    if (cookie.name.startsWith("__Host-")) {
      candidateParams.push({
        name: cookie.name,
        value: cookie.value,
        path: "/",
        secure: true,
        url: "https://alpha.midjourney.com/",
      });
      candidateParams.push({
        name: cookie.name,
        value: cookie.value,
        path: "/",
        secure: true,
        url: "https://www.midjourney.com/",
      });
    } else {
      candidateParams.push({
        name: cookie.name,
        value: cookie.value,
        path: "/",
        secure: true,
        domain: ".midjourney.com",
        url: "https://alpha.midjourney.com/",
      });
    }
    for (const params of candidateParams) {
      try {
        await client.send("Network.setCookie", params);
      } catch (_) {
        // Ignore cookie-set failures for non-critical cookies.
      }
    }
  }

  const currentUrlResult = await client.send("Runtime.evaluate", {
    expression: "location.href",
    returnByValue: true,
  });
  const currentUrl = String(currentUrlResult?.result?.value || "");
  if (forceNavigate || !currentUrl.startsWith(pageUrl)) {
    await client.send("Page.navigate", { url: pageUrl });
    await sleep(2000);
  }

  await assertNoSecurityChallenge(client);

  const deadline = Date.now() + timeoutSeconds * 1000;
  let result;
  while (Date.now() < deadline) {
    result = await client.send("Runtime.evaluate", {
      expression,
      awaitPromise: true,
      returnByValue: true,
    });
    if (result?.result) break;
    await sleep(300);
  }

  client.close();

  if (!result?.result) {
    throw new Error("No evaluation result");
  }
  const value = result.result.value;
  process.stdout.write(JSON.stringify(value));
}

main().catch((error) => {
  console.error(error.message || String(error));
  process.exit(1);
});
