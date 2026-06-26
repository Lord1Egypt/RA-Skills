#!/usr/bin/env node
import { randomUUID } from "node:crypto";
import {
  appendLog,
  enqueueFeeds,
  fetchJson,
  getApiKey,
  getApiUrl,
  paths,
  readJson,
  requireApiKey,
  sleep,
  updateStatus,
  writeJsonAtomic,
} from "./common.mjs";

const WebSocketImpl = globalThis.WebSocket;
const HEARTBEAT_FALLBACK_MS = 25_000;
const BACKFILL_LIMIT = 50;
const FALLBACK_POLL_MS = 60_000;

if (!WebSocketImpl) {
  throw new Error("This Node.js runtime does not provide WebSocket support");
}

process.on("uncaughtException", async (error) => {
  await appendLog(`[uncaughtException] ${error instanceof Error ? error.stack || error.message : String(error)}`);
  process.exit(1);
});

process.on("unhandledRejection", async (error) => {
  await appendLog(`[unhandledRejection] ${error instanceof Error ? error.stack || error.message : String(error)}`);
  process.exit(1);
});

let keepRunning = true;
let heartbeatTimer = null;

process.on("SIGINT", stop);
process.on("SIGTERM", stop);

function stop() {
  keepRunning = false;
  if (heartbeatTimer) {
    clearInterval(heartbeatTimer);
    heartbeatTimer = null;
  }
}

async function touchHeartbeat(extra = {}) {
  await updateStatus({
    pid: process.pid,
    heartbeatAt: new Date().toISOString(),
    ...extra,
  });
}

async function fetchPendingFeeds() {
  const apiUrl = getApiUrl();
  const apiKey = requireApiKey();
  const response = await fetchJson(`${apiUrl}/api/feeds/pending?limit=${BACKFILL_LIMIT}`, {
    timeoutMs: 15_000,
    headers: {
      "X-API-Key": apiKey,
    },
  });

  if (!response.ok) {
    throw new Error(`Pending feed backfill failed (${response.status})`);
  }

  const feeds = Array.isArray(response.data?.feeds) ? response.data.feeds : [];
  if (feeds.length > 0) {
    await enqueueFeeds(feeds);
  }
  await touchHeartbeat({
    lastBackfillAt: new Date().toISOString(),
    lastBackfillCount: feeds.length,
  });
  return feeds.length;
}

async function fetchRealtimeSession() {
  const apiUrl = getApiUrl();
  const apiKey = requireApiKey();
  const response = await fetchJson(`${apiUrl}/api/realtime/session`, {
    timeoutMs: 15_000,
    headers: {
      "X-API-Key": apiKey,
    },
  });

  if (response.ok && response.data?.realtime) {
    return response.data.realtime;
  }

  if (response.status === 501) {
    return null;
  }

  const message = response.data?.error || response.text || `Realtime session failed (${response.status})`;
  throw new Error(message);
}

function buildSocketUrl(session) {
  return `${session.supabaseUrl.replace(/^http/, "ws")}/realtime/v1/websocket?apikey=${encodeURIComponent(session.anonKey)}&vsn=1.0.0`;
}

function sendJson(socket, payload) {
  socket.send(JSON.stringify(payload));
}

async function connectRealtime(session) {
  const socketUrl = buildSocketUrl(session);
  const channelTopic = `realtime:${session.topic}`;
  const joinRef = randomUUID();
  const heartbeatMs = Number(session.heartbeatIntervalMs) || HEARTBEAT_FALLBACK_MS;
  const tokenRefreshAt = Math.max(heartbeatMs, new Date(session.expiresAt).getTime() - Date.now() - 60_000);

  await appendLog(`[realtime] connecting ${session.topic}`);
  await touchHeartbeat({
    state: "connecting",
    mode: "realtime",
    topic: session.topic,
    message: "Connecting to Supabase Realtime",
    lastError: null,
  });

  return new Promise((resolve, reject) => {
    let settled = false;
    let subscribed = false;
    let refreshTimer = null;

    const socket = new WebSocketImpl(socketUrl);

    const cleanup = () => {
      if (heartbeatTimer) {
        clearInterval(heartbeatTimer);
        heartbeatTimer = null;
      }
      if (refreshTimer) {
        clearTimeout(refreshTimer);
        refreshTimer = null;
      }
    };

    const finish = (error = null) => {
      if (settled) return;
      settled = true;
      cleanup();
      try {
        socket.close();
      } catch {}
      if (error) {
        reject(error);
      } else {
        resolve();
      }
    };

    socket.addEventListener("open", () => {
      sendJson(socket, {
        topic: channelTopic,
        event: "phx_join",
        payload: {
          config: {
            private: true,
            broadcast: {
              ack: false,
              self: false,
            },
            presence: {
              enabled: false,
            },
          },
          access_token: session.accessToken,
        },
        ref: joinRef,
        join_ref: joinRef,
      });

      heartbeatTimer = setInterval(() => {
        if (socket.readyState !== WebSocketImpl.OPEN) return;
        sendJson(socket, {
          topic: "phoenix",
          event: "heartbeat",
          payload: {},
          ref: randomUUID(),
        });
        void touchHeartbeat({ state: subscribed ? "connected" : "connecting", mode: "realtime", topic: session.topic });
      }, heartbeatMs);

      refreshTimer = setTimeout(() => {
        void appendLog("[realtime] refreshing session before token expiry");
        finish();
      }, tokenRefreshAt);
    });

    socket.addEventListener("message", (event) => {
      void (async () => {
        let message;
        try {
          message = JSON.parse(typeof event.data === "string" ? event.data : String(event.data));
        } catch {
          return;
        }

        if (message?.event === "phx_reply" && message?.ref === joinRef) {
          const status = message?.payload?.status;
          if (status !== "ok") {
            finish(new Error(message?.payload?.response?.reason || "Failed to join realtime channel"));
            return;
          }

          subscribed = true;
          await touchHeartbeat({
            state: "connected",
            mode: "realtime",
            topic: session.topic,
            connectedAt: new Date().toISOString(),
            message: "Realtime channel subscribed",
            lastError: null,
          });
          await fetchPendingFeeds();
          return;
        }

        if (message?.event === "phx_error") {
          finish(new Error("Realtime channel returned phx_error"));
          return;
        }

        if (message?.event === "phx_close") {
          finish();
          return;
        }

        if (message?.event !== "broadcast") {
          return;
        }

        const broadcastEvent = message?.payload?.event;
        const feed = message?.payload?.payload?.feed;
        if (broadcastEvent !== session.event || !feed) {
          return;
        }

        await enqueueFeeds([feed]);
        await touchHeartbeat({
          state: "connected",
          mode: "realtime",
          topic: session.topic,
          lastFeedAt: new Date().toISOString(),
        });
      })().catch((error) => {
        void appendLog(`[realtime] message handler error: ${error instanceof Error ? error.message : String(error)}`);
      });
    });

    socket.addEventListener("error", () => {
      finish(new Error("Realtime socket error"));
    });

    socket.addEventListener("close", () => {
      finish();
    });
  });
}

async function runFallbackLoop(reason) {
  await appendLog(`[fallback] ${reason}`);
  while (keepRunning) {
    try {
      const count = await fetchPendingFeeds();
      await touchHeartbeat({
        state: "fallback",
        mode: "polling",
        message: reason,
        lastError: null,
        lastBackfillCount: count,
      });
    } catch (error) {
      await touchHeartbeat({
        state: "fallback-error",
        mode: "polling",
        message: reason,
        lastError: error instanceof Error ? error.message : String(error),
      });
      await appendLog(`[fallback] ${error instanceof Error ? error.message : String(error)}`);
    }

    await sleep(FALLBACK_POLL_MS);
  }
}

async function main() {
  requireApiKey();
  await writeJsonAtomic(paths.pid, {
    pid: process.pid,
    startedAt: new Date().toISOString(),
    mode: process.env.FEEDTO_DISABLE_REALTIME === "1" ? "polling" : "realtime",
  });

  let retryDelayMs = 1_000;

  while (keepRunning) {
    if (getApiKey() === "") {
      await touchHeartbeat({ state: "stopped", mode: "polling", message: "FEEDTO_API_KEY missing" });
      return;
    }

    if (process.env.FEEDTO_DISABLE_REALTIME === "1") {
      await runFallbackLoop("Realtime disabled by FEEDTO_DISABLE_REALTIME=1");
      return;
    }

    try {
      const session = await fetchRealtimeSession();
      if (!session) {
        await runFallbackLoop("Realtime not configured on server, using polling fallback");
        return;
      }

      retryDelayMs = 1_000;
      await connectRealtime(session);
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      await touchHeartbeat({
        state: "reconnecting",
        mode: "realtime",
        message: "Realtime connection dropped, retrying",
        lastError: message,
        nextRetryInMs: retryDelayMs,
      });
      await appendLog(`[realtime] ${message}`);
      await fetchPendingFeeds().catch(async (backfillError) => {
        await appendLog(`[realtime] backfill after disconnect failed: ${backfillError instanceof Error ? backfillError.message : String(backfillError)}`);
      });
      await sleep(retryDelayMs);
      retryDelayMs = Math.min(retryDelayMs * 2, 30_000);
    }
  }
}

main().catch(async (error) => {
  await touchHeartbeat({
    state: "crashed",
    mode: process.env.FEEDTO_DISABLE_REALTIME === "1" ? "polling" : "realtime",
    lastError: error instanceof Error ? error.message : String(error),
  });
  await appendLog(`[fatal] ${error instanceof Error ? error.stack || error.message : String(error)}`);
  process.exit(1);
});
