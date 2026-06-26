#!/usr/bin/env node

const args = process.argv.slice(2);

function getArg(name, fallback = null) {
  const index = args.indexOf(name);
  if (index === -1) return fallback;
  return args[index + 1] ?? fallback;
}

const debugPort = Number(getArg("--debug-port", "9222"));
const pageUrl = getArg("--page-url");
const jobIds = JSON.parse(getArg("--job-ids-json", "[]"));
const timeoutSeconds = Number(getArg("--timeout-seconds", "90"));
const minCount = Number(getArg("--min-count", "4"));

if (!pageUrl || !Array.isArray(jobIds) || jobIds.length === 0) {
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

async function getExistingPageTarget() {
  const list = await fetchJson(`http://127.0.0.1:${debugPort}/json/list`);
  return (
    list.find(
      (item) =>
        item.type === "page" &&
        String(item.url || "").startsWith(pageUrl),
    ) || null
  );
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

function buildImageUrlRegex() {
  return /https?:\/\/[^"' )]+cdn\.midjourney\.com[^"' )]+\.(?:png|jpe?g|webp)(?:\?[^"' )]*)?/ig;
}

function normalizeUrl(rawUrl) {
  return String(rawUrl || "")
    .replace(/^url\(["']?/, "")
    .replace(/["']?\)$/, "");
}

function extractUrlsForJobs(input, wantedJobIds) {
  const text = String(input || "");
  const matches = text.match(buildImageUrlRegex()) || [];
  const urlsByJob = new Map();
  for (const jobId of wantedJobIds) {
    urlsByJob.set(jobId, []);
  }
  for (const match of matches) {
    const cleaned = normalizeUrl(match);
    for (const jobId of wantedJobIds) {
      if (!cleaned.includes(jobId)) continue;
      urlsByJob.get(jobId).push(cleaned);
    }
  }
  return urlsByJob;
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
  return probe;
}

function makeJobState(jobId) {
  return {
    job_id: jobId,
    count: 0,
    result_urls: [],
    done: false,
    sources: [],
  };
}

function recordJobUrls(state, urls, source) {
  for (const url of urls) {
    if (!url) continue;
    if (!state.result_urls.includes(url)) {
      state.result_urls.push(url);
    }
  }
  state.count = state.result_urls.length;
  state.done = state.count >= Math.max(1, minCount);
  if (source && !state.sources.includes(source)) {
    state.sources.push(source);
  }
}

async function main() {
  const target = await getExistingPageTarget();
  if (!target?.webSocketDebuggerUrl) {
    throw new Error("No existing Midjourney imagine page is open for low-impact result watching.");
  }

  const client = new CDPClient(target.webSocketDebuggerUrl);
  await client.open();
  await client.send("Page.enable");
  await client.send("Runtime.enable");
  await client.send("Network.enable");

  const pageProbe = await assertNoSecurityChallenge(client);
  const jobState = Object.fromEntries(jobIds.map((jobId) => [jobId, makeJobState(jobId)]));
  const interestingRequests = new Map();
  let apiEventCount = 0;
  let imageEventCount = 0;

  const seedResult = await client.send("Runtime.evaluate", {
    expression: `
      (() => performance.getEntriesByType('resource').map((entry) => entry.name))()
    `,
    returnByValue: true,
  });
  const performanceUrls = Array.isArray(seedResult?.result?.value) ? seedResult.result.value : [];
  const seeded = extractUrlsForJobs(performanceUrls.join("\n"), jobIds);
  for (const jobId of jobIds) {
    recordJobUrls(jobState[jobId], seeded.get(jobId) || [], "performance");
  }

  client.on("Network.responseReceived", (params) => {
    const requestId = params.requestId;
    const responseUrl = String(params.response?.url || "");
    if (!responseUrl) return;

    if (
      responseUrl.includes("/api/imagine") ||
      responseUrl.includes("/api/imagine-update") ||
      responseUrl.includes("/api/user-queue") ||
      responseUrl.includes("/api/job-status")
    ) {
      interestingRequests.set(requestId, responseUrl);
      apiEventCount += 1;
    }

    if (!responseUrl.includes("cdn.midjourney.com")) return;
    for (const jobId of jobIds) {
      if (!responseUrl.includes(jobId)) continue;
      recordJobUrls(jobState[jobId], [responseUrl], "network_response");
      imageEventCount += 1;
    }
  });

  client.on("Network.loadingFinished", async (params) => {
    const responseUrl = interestingRequests.get(params.requestId);
    if (!responseUrl) return;
    interestingRequests.delete(params.requestId);
    try {
      const bodyResult = await client.send("Network.getResponseBody", { requestId: params.requestId });
      const bodyText = bodyResult?.base64Encoded
        ? Buffer.from(bodyResult.body || "", "base64").toString("utf8")
        : String(bodyResult?.body || "");
      const extracted = extractUrlsForJobs(`${responseUrl}\n${bodyText}`, jobIds);
      for (const jobId of jobIds) {
        recordJobUrls(jobState[jobId], extracted.get(jobId) || [], "api_response");
      }
    } catch (_) {
      // Response bodies are best-effort only.
    }
  });

  const startedAt = Date.now();
  const deadline = startedAt + timeoutSeconds * 1000;
  while (Date.now() < deadline) {
    if (jobIds.every((jobId) => jobState[jobId].done)) {
      break;
    }
    await sleep(500);
  }

  const completedAt = Date.now();
  client.close();

  process.stdout.write(
    JSON.stringify({
      done: jobIds.every((jobId) => jobState[jobId].done),
      elapsed_seconds: Number(((completedAt - startedAt) / 1000).toFixed(3)),
      min_count: minCount,
      page_probe: pageProbe,
      event_counts: {
        apiEventCount,
        imageEventCount,
        pendingRequests: interestingRequests.size,
      },
      jobs: jobState,
    }),
  );
}

main().catch((error) => {
  console.error(error.message || String(error));
  process.exit(1);
});
