import { saveKey } from "./credentials.mjs";

const ORIGIN = "https://aivideomaker.ai";
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const messages = {
  DENIED: "Connection cancelled. No key was saved.",
  EXPIRED: "Connection expired. Run connect again to get a new approval link.",
  CONSUMED:
    "This connection was already exchanged. Check API key settings for an unused agent key, then run connect again.",
  RATE_LIMITED: "Too many connection attempts. Wait 10 minutes and try again.",
};

async function request(path, body, fetcher, apiKey, timeoutMs = 30000) {
  let response;
  try {
    response = await fetcher(`${ORIGIN}${path}`, {
      method: body === undefined ? "GET" : "POST",
      headers: { "Content-Type": "application/json", ...(apiKey ? { key: apiKey } : {}) },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
      redirect: "error",
      signal: AbortSignal.timeout(timeoutMs),
    });
  } catch {
    throw new Error("Could not reach AI Video Maker. Check your connection and try again.");
  }
  let data;
  let invalidJson = false;
  try {
    data = await response.json();
  } catch {
    invalidJson = true; // A truncated exchange response can be recovered with the same secret.
  }
  const retryAfter = response.headers.get("retry-after");
  const seconds = retryAfter === null ? NaN : Number(retryAfter);
  const retryAfterMs = Number.isFinite(seconds)
    ? Math.max(0, seconds * 1000)
    : Math.max(0, Date.parse(retryAfter || "") - Date.now()) || 0;
  return {
    ok: response.ok,
    data,
    retryAfterMs,
    retryable:
      response.status === 408 ||
      response.status === 429 ||
      response.status >= 500 ||
      (response.ok && invalidJson),
  };
}

export async function verifyConnection(apiKey, { fetcher = fetch } = {}) {
  const account = await request("/api/v1/account", undefined, fetcher, apiKey);
  if (
    !account.ok ||
    account.data?.ok !== true ||
    account.data?.key?.status !== "ACTIVE" ||
    !Number.isFinite(account.data?.currentBalance)
  ) {
    throw new Error(
      "Connection could not be verified. No credits spent. Check your API key settings and retry.",
    );
  }
  const quote = await request(
    "/api/v1/quote/minimax",
    {
      content: "A cinematic candle on a wooden table",
      duration: 5,
      resolution: "720p",
      tier: "turbo",
      aspectRatio: "16:9",
    },
    fetcher,
    apiKey,
  );
  if (!quote.ok || quote.data?.billable !== false || !Number.isFinite(quote.data?.credits)) {
    throw new Error(
      "Account connected, but the sample quote could not be verified. No credits spent. Retry verification with the saved connection.",
    );
  }
  return {
    status: "VERIFIED",
    currentBalance: account.data.currentBalance,
    sampleQuoteCredits: quote.data.credits,
    creditsSpent: 0,
  };
}

export async function browserConnect({
  fetcher = fetch,
  directory,
  platform = process.env.AIVIDEO_AGENT_PLATFORM || "other",
  onApproval = () => {},
  sleep = wait,
  now = Date.now,
} = {}) {
  const started = await request(
    "/api/skill-connect/start",
    {
      platform: ["codex", "claude", "openclaw"].includes(platform) ? platform : "other",
    },
    fetcher,
  );
  if (!started.ok)
    throw new Error(
      messages[started.data?.error] ||
        "Browser connection is unavailable. Retry later, or use connect.mjs --manual in your own terminal.",
    );
  const { deviceCode, userCode, expiresIn, interval } = started.data ?? {};
  if (
    !/^[a-f0-9]{64}$/.test(deviceCode || "") ||
    !/^[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}$/.test(userCode || "") ||
    expiresIn !== 600 ||
    interval !== 5
  ) {
    throw new Error("Invalid connection response. No key was saved.");
  }
  const deadline = now() + expiresIn * 1000;
  // Only the public comparison code reaches the agent; the device secret stays in memory.
  onApproval({
    url: `${ORIGIN}/connect/ai-video-maker?code=${userCode}`,
    code: userCode,
    expiresIn,
  });
  const remaining = () => Math.max(0, deadline - now());
  const pause = (ms) => sleep(Math.min(ms, remaining()));
  const requestToken = (acknowledge = false) =>
    request(
      "/api/skill-connect/token",
      { deviceCode, acknowledge },
      fetcher,
      undefined,
      Math.max(1, Math.min(30000, remaining())),
    ).catch(() => ({ retryable: true, retryAfterMs: 0 }));
  const pollDelay = (interval + 0.5) * 1000;
  let delay = pollDelay;
  while (now() < deadline) {
    await pause(delay);
    if (now() >= deadline) break;
    const result = await requestToken();
    if (result.retryable) {
      delay = Math.max(Math.min(30000, delay * 2), result.retryAfterMs);
      continue;
    }
    delay = pollDelay;
    if (result.data?.error === "SLOW_DOWN" || (result.ok && result.data?.status === "PENDING"))
      continue;
    if (!result.ok)
      throw new Error(
        messages[result.data?.error] ||
          "Connection interrupted. Run connect again. No credits spent.",
      );
    if (
      result.data?.status !== "CONNECTED" ||
      !/^ak_[a-f0-9]{64}$/.test(result.data?.apiKey || "")
    ) {
      throw new Error("Invalid connection response. No key was saved.");
    }
    try {
      // Persist before verification: a temporary account/quote outage must not lose the exchanged key.
      await saveKey(result.data.apiKey, directory);
    } catch {
      throw new Error(
        "Could not save the connection privately. Revoke the new agent key in API key settings, check local permissions, and reconnect.",
      );
    }
    // Acknowledge only after the file is safely saved. ACK is idempotent; failure
    // here must not discard a working local connection. The recovery window also
    // closes automatically when this session expires.
    for (let attempt = 0; attempt < 3 && now() < deadline; attempt++) {
      const acknowledgement = await requestToken(true);
      if (!acknowledgement.retryable) break;
      if (attempt < 2) await pause(Math.max(pollDelay, acknowledgement.retryAfterMs));
    }
    return verifyConnection(result.data.apiKey, { fetcher });
  }
  throw new Error(messages.EXPIRED);
}
