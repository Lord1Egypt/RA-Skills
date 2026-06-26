#!/usr/bin/env node

const args = process.argv.slice(2);

function getArg(name, fallback = null) {
  const index = args.indexOf(name);
  if (index === -1) return fallback;
  return args[index + 1] ?? fallback;
}

const debugPort = Number(getArg("--debug-port", "9222"));
const pageUrl = getArg("--page-url");
const requestUrl = getArg("--request-url");
const method = getArg("--method", "GET");
const headers = JSON.parse(getArg("--headers-json", "{}"));
const payloadJson = getArg("--payload-json");
const payload = payloadJson ? JSON.parse(payloadJson) : null;
const cookieHeader = getArg("--cookie-header", "");
const timeoutSeconds = Number(getArg("--timeout-seconds", "60"));

if (!pageUrl || !requestUrl) {
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

async function getOrCreatePageTarget() {
  const list = await fetchJson(`http://127.0.0.1:${debugPort}/json/list`);
  let target = list.find(
    (item) =>
      item.type === "page" &&
      String(item.url || "").startsWith(pageUrl),
  );
  if (target) return target;
  target = await fetchJson(`http://127.0.0.1:${debugPort}/json/new?${encodeURIComponent(pageUrl)}`, {
    method: "PUT",
  });
  await sleep(1500);
  return target;
}

class CDPClient {
  constructor(webSocketUrl) {
    this.socket = new WebSocket(webSocketUrl);
    this.nextId = 1;
    this.pending = new Map();
    this.events = new Map();
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
        return;
      }
      if (message.method) {
        const handlers = this.events.get(message.method) || [];
        for (const handler of handlers) handler(message.params || {});
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

  on(eventName, handler) {
    const handlers = this.events.get(eventName) || [];
    handlers.push(handler);
    this.events.set(eventName, handlers);
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
  if (!currentUrl.startsWith(pageUrl)) {
    let loadSeen = false;
    client.on("Page.loadEventFired", () => {
      loadSeen = true;
    });
    await client.send("Page.navigate", { url: pageUrl });
    const loadDeadline = Date.now() + 15000;
    while (!loadSeen && Date.now() < loadDeadline) {
      await sleep(200);
    }
  }

  await assertNoSecurityChallenge(client);

  const expression = `
    (async () => {
      try {
        const response = await fetch(${JSON.stringify(requestUrl)}, ${JSON.stringify({
          method,
          headers,
          credentials: "include",
          body: payload ? JSON.stringify(payload) : undefined,
        })});
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
    })()
  `;

  const result = await client.send("Runtime.evaluate", {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
  client.close();

  const value = result.result?.value;
  if (value === undefined || value === null) {
    throw new Error("Empty CDP fetch response");
  }
  const parsed = typeof value === "string" ? JSON.parse(value) : value;
  if (!parsed.ok) {
    throw new Error(`${parsed.error || `HTTP ${parsed.status}`}: ${String(parsed.text).slice(0, 500)}`);
  }
  process.stdout.write(parsed.text);
}

main().catch((error) => {
  console.error(error.message || String(error));
  process.exit(1);
});
