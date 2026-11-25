import { randomUUID } from "node:crypto";
import { firstVideoScenarios } from "./first-video.mjs";
import {
  checkPrivateStorage,
  clearPendingConnection,
  loadPendingConnection,
  loadSavedKey,
  saveKey,
  savePendingConnection,
} from "./credentials.mjs";

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
    firstVideo: { flowId: randomUUID(), scenarios: firstVideoScenarios },
  };
}

// Why a connection cannot be saved, and what that means for an approval already under way.
// Fixed text only: the cause is an error code, never a path or a server response.
function storageError(error, pending) {
  const code = error?.code;
  const cause = ["EACCES", "EPERM", "EROFS"].includes(code)
    ? "it is not allowed to write its private folder ~/.aivideo-maker. If the agent runs in a sandbox, allow it to write that folder or run connect outside the sandbox."
    : code === "NOT_PRIVATE"
      ? "its private folder ~/.aivideo-maker is not private to you. It must be owned by you with owner-only access (folder 700, files 600)."
      : code === "WRONG_TYPE"
        ? "its private folder ~/.aivideo-maker is not a regular folder (for example, it is a link). Replace it with a real folder."
        : code === "NOT_REPLACEABLE"
          ? "credentials.json in ~/.aivideo-maker cannot be replaced. Remove it, or clear its read-only flag."
          : `its private folder ~/.aivideo-maker could not be written${code ? ` (${code})` : ""}. Check free disk space and that the folder is usable.`;
  const state = pending
    ? "Your pending approval is kept: fix this and run connect again to resume the same link and code."
    : "No approval link was shown and nothing was approved.";
  return new Error(
    `This agent cannot save a connection: ${cause} ${state} Alternatively run connect.mjs --manual in your own terminal, or set AIVIDEO_API_KEY in the agent's secret environment.`,
  );
}

const POLL_DELAY_MS = 5500; // Just over the server's 5-second poll interval.
// Less time than someone needs to open the link, sign in and approve.
const MIN_RESUME_MS = 60000;
// Outcomes the server will never change. Anything else may be a passing fault.
const FINAL_ERRORS = new Set(["DENIED", "EXPIRED", "CONSUMED"]);

function savedKey(directory) {
  try {
    return loadSavedKey(directory);
  } catch {
    return "";
  }
}

// The approval in progress, if it can still be finished. Stale state is removed, so an
// abandoned device secret does not outlive its session on disk.
export async function pendingApproval({ directory, now = Date.now } = {}) {
  const pending = loadPendingConnection(directory);
  if (pending && pending.expiresAt > now()) return pending;
  await clearPendingConnection(directory);
  return null;
}

export async function browserConnect({
  fetcher = fetch,
  directory,
  platform = process.env.AIVIDEO_AGENT_PLATFORM || "other",
  onApproval = () => {},
  sleep = wait,
  now = Date.now,
  resume = true,
  replacing = false,
  waitForApproval = true,
} = {}) {
  const keyAtStart = savedKey(directory);

  // Polls one session until it connects, ends, or (with `once`) answers a single time.
  const collect = async (
    { deviceCode, expiresAt: deadline },
    { fromDisk = false, once = false } = {},
  ) => {
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
    // The user may have approved while no helper was running, so a saved session asks at once.
    let delay = fromDisk ? 0 : POLL_DELAY_MS;
    while (now() < deadline) {
      await pause(delay);
      if (now() >= deadline) break;
      const result = await requestToken();
      const code = result.data?.error;
      // SLOW_DOWN arrives as HTTP 429 but is ordinary pacing, not a fault to back off from.
      const waiting = code === "SLOW_DOWN" || (result.ok && result.data?.status === "PENDING");
      if (once && (waiting || result.retryable)) return null;
      if (waiting) {
        delay = POLL_DELAY_MS;
        continue;
      }
      if (result.retryable) {
        delay = Math.max(Math.min(30000, Math.max(delay, POLL_DELAY_MS) * 2), result.retryAfterMs);
        continue;
      }
      if (!result.ok) {
        if (code === "CONSUMED") {
          // Another run of this helper finished the same session and saved its key.
          const saved = savedKey(directory);
          if (saved && (fromDisk || saved !== keyAtStart)) {
            await clearPendingConnection(directory);
            return verifyConnection(saved, { fetcher });
          }
        }
        // A passing fault keeps the session, so the next run picks the same link up again.
        if (FINAL_ERRORS.has(code)) await clearPendingConnection(directory);
        if (once && FINAL_ERRORS.has(code)) return null;
        throw new Error(
          messages[code] ||
            "Connection interrupted. Run connect again to resume it. No credits spent.",
        );
      }
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
          "Could not save the connection privately. Check local permissions and run connect again while the link is valid; otherwise revoke the unused agent key in API key settings and reconnect.",
        );
      }
      // Acknowledge only after the file is safely saved. ACK is idempotent; failure
      // here must not discard a working local connection. The recovery window also
      // closes automatically when this session expires.
      for (let attempt = 0; attempt < 3 && now() < deadline; attempt++) {
        const acknowledgement = await requestToken(true);
        if (!acknowledgement.retryable) break;
        if (attempt < 2) await pause(Math.max(POLL_DELAY_MS, acknowledgement.retryAfterMs));
      }
      await clearPendingConnection(directory);
      return verifyConnection(result.data.apiKey, { fetcher });
    }
    await clearPendingConnection(directory);
    throw new Error(messages.EXPIRED);
  };

  // A helper that was stopped before the user approved leaves its session on disk. Picking it
  // up keeps the link and code the user already has valid instead of stranding their approval.
  let pending = resume ? await pendingApproval({ directory, now }) : null;
  // Before anything is asked of the user or the server: an approval is wasted, and its key
  // orphaned, when the result cannot be stored on this computer.
  await checkPrivateStorage(directory).catch((error) => {
    throw storageError(error, pending);
  });
  if (pending && pending.expiresAt - now() < MIN_RESUME_MS) {
    // Too late to send anyone to this link, but an approval may already be waiting on it.
    const collected = await collect(pending, { fromDisk: true, once: true });
    if (collected) return collected;
    pending = null;
  }
  const resumed = pending !== null;
  if (!pending) {
    await clearPendingConnection(directory);
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
    pending = {
      deviceCode,
      userCode,
      expiresAt: now() + expiresIn * 1000,
      ...(replacing ? { replacing: true } : {}),
    };
    await savePendingConnection(pending, directory).catch((error) => {
      // While this process keeps waiting the session still completes in memory. With --start
      // nothing would be left to finish it, and the link would lead the user nowhere. The
      // session just requested stays unused on the server until it expires; the check above
      // makes this rare.
      if (!waitForApproval) throw storageError(error, null);
    });
  }
  const secondsLeft = Math.ceil(Math.max(0, pending.expiresAt - now()) / 1000);
  // Only the public comparison code reaches the agent; the device secret stays in memory
  // and in the private credentials directory, which the agent never reads.
  onApproval({
    url: `${ORIGIN}/connect/ai-video-maker?code=${pending.userCode}`,
    code: pending.userCode,
    expiresIn: secondsLeft,
    resumed,
  });
  if (!waitForApproval) return { status: "PENDING", expiresIn: secondsLeft };
  return collect(pending, { fromDisk: resumed });
}
