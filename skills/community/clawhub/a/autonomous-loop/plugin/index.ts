/**
 * autonomous-loop — OpenClaw Plugin
 *
 * After each successful agent reply, waits `delayMs` milliseconds and then
 * sends a follow-up message to the same session. This creates a self-sustaining
 * work loop: the agent keeps running until a stop file is placed at
 * ~/.openclaw/autonomous-loop.{agentId}.stop  —or—  the agent replies with
 * "DONE" or "HEARTBEAT_OK".
 *
 * Plugin config (via openclaw.json plugins["autonomous-loop"]):
 *   delayMs        — wait time between reply and next message (default: 30000)
 *   defaultMessage — message used when no per-agent message is configured
 *   agents         — map of agentId → custom message
 *
 * Stop/resume:
 *   Stop:   touch ~/.openclaw/autonomous-loop.{agentId}.stop
 *   Resume: rm    ~/.openclaw/autonomous-loop.{agentId}.stop
 */

import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { appendFile, access, mkdir, readFile } from "node:fs/promises";
import { watchFile } from "node:fs";
import { randomUUID, createPrivateKey, createPublicKey, sign as cryptoSign } from "node:crypto";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const OPENCLAW_HOME =
  process.env.OPENCLAW_HOME ??
  (process.env.HOME ? `${process.env.HOME}/.openclaw` : "/root/.openclaw");

const LOGS_DIR = `${OPENCLAW_HOME}/logs`;
const DEFAULT_DELAY_MS = 30_000;
const GATEWAY_SEND_TIMEOUT_MS = 10_000;

const FALLBACK_MESSAGE = `Read TASKS.md and PROGRESS.md to understand the current project state, then:\n1. If there is an in-progress task, continue it\n2. Otherwise pick the highest-priority Pending task (skip any that require user input)\n3. Execute the task, verify the result, update TASKS.md and PROGRESS.md\n4. If there are no actionable tasks, reply DONE`;

/** Word-boundary regex — avoids false matches like "condone" or "undone". */
const STOP_TOKEN_RE = /\b(DONE|HEARTBEAT_OK)\b/;

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type PluginConfig = {
  delayMs?: number;
  defaultMessage?: string;
  agents?: Record<string, string>;
};

type AgentState = { timer: ReturnType<typeof setTimeout>; sessionKey: string };

type DeviceIdentity = {
  deviceId: string;
  publicKeyBase64: string;
  privateKeyPem: string;
};

// ---------------------------------------------------------------------------
// Module-level state
// ---------------------------------------------------------------------------

const activeByAgent = new Map<string, AgentState>();
const stopWatchersByAgent = new Set<string>();
let logsDirEnsured = false;

/** Cached device identity — loaded once during gateway_start. */
let cachedDeviceIdentity: DeviceIdentity | null | undefined = undefined;

// ---------------------------------------------------------------------------
// Helpers — file paths
// ---------------------------------------------------------------------------

const getLogPath = (agentId: string): string =>
  `${LOGS_DIR}/autonomous-loop-${agentId}.log`;

const getStopPath = (agentId: string): string =>
  `${OPENCLAW_HOME}/autonomous-loop.${agentId}.stop`;

// ---------------------------------------------------------------------------
// Helpers — ensure logs directory exists (once per process)
// ---------------------------------------------------------------------------

const ensureLogsDir = async (): Promise<void> => {
  if (logsDirEnsured) return;
  await mkdir(LOGS_DIR, { recursive: true });
  logsDirEnsured = true;
};

// ---------------------------------------------------------------------------
// Helpers — logging
// ---------------------------------------------------------------------------

const logLine = async (agentId: string, line: string): Promise<void> => {
  await ensureLogsDir();
  await appendFile(
    getLogPath(agentId),
    `${new Date().toISOString()} | ${line}\n`,
    "utf8",
  );
};

// ---------------------------------------------------------------------------
// Helpers — resolve agentId from context
// ---------------------------------------------------------------------------

const resolveAgentId = (ctx: { agentId?: string; sessionKey?: string }): string => {
  if (typeof ctx.agentId === "string" && ctx.agentId.length > 0) return ctx.agentId;
  if (typeof ctx.sessionKey === "string") {
    const parts = ctx.sessionKey.split(":");
    if (parts.length >= 2 && parts[0] === "agent") return parts[1];
  }
  return "default";
};

// ---------------------------------------------------------------------------
// Helpers — resolve message for agent
// ---------------------------------------------------------------------------

const resolveMessage = (agentId: string, config: PluginConfig): string =>
  config.agents?.[agentId] ?? config.defaultMessage ?? FALLBACK_MESSAGE;

// ---------------------------------------------------------------------------
// Helpers — extract last assistant text from messages array
// ---------------------------------------------------------------------------

const extractLastAssistantText = (messages: unknown[] | undefined): string | undefined => {
  if (!Array.isArray(messages)) return undefined;
  for (let i = messages.length - 1; i >= 0; i--) {
    const msg = messages[i] as Record<string, unknown>;
    if (msg?.role !== "assistant") continue;
    const content = msg.content;
    if (typeof content === "string" && content.length > 0) return content;
    if (Array.isArray(content)) {
      const blocks = content
        .filter((b): b is Record<string, unknown> => !!b && typeof b === "object")
        .filter((b) => b.type === "text" && typeof b.text === "string")
        .map((b) => b.text as string);
      if (blocks.length > 0) return blocks.join("\n");
    }
  }
  return undefined;
};

// ---------------------------------------------------------------------------
// Helpers — check if reply contains a stop token (word-boundary match)
// ---------------------------------------------------------------------------

const replyContainsStopToken = (text: string): boolean => STOP_TOKEN_RE.test(text);

// ---------------------------------------------------------------------------
// Helpers — stop file
// ---------------------------------------------------------------------------

const stopFileExists = async (agentId: string): Promise<boolean> => {
  try {
    await access(getStopPath(agentId));
    return true;
  } catch {
    return false;
  }
};

const installStopWatcher = (
  agentId: string,
  logger: { info: (m: string) => void },
): void => {
  if (stopWatchersByAgent.has(agentId)) return;
  const stopPath = getStopPath(agentId);
  watchFile(stopPath, { interval: 500 }, (cur) => {
    if (cur.mtimeMs <= 0 || !cur.isFile()) return;
    const state = activeByAgent.get(agentId);
    if (state) {
      clearTimeout(state.timer);
      activeByAgent.delete(agentId);
    }
    void logLine(agentId, `stop-file-detected | path=${stopPath}`);
    logger.info(`[autonomous-loop] Stop file detected for ${agentId}. Loop paused.`);
  });
  stopWatchersByAgent.add(agentId);
};

// ---------------------------------------------------------------------------
// Helpers — device identity (required for operator.write, OpenClaw 2026.3.13+)
// ---------------------------------------------------------------------------

const loadDeviceIdentity = async (
  logger?: { info: (m: string) => void },
): Promise<DeviceIdentity | null> => {
  // Return cached value if already resolved
  if (cachedDeviceIdentity !== undefined) return cachedDeviceIdentity;

  const identityPath = `${OPENCLAW_HOME}/identity/device.json`;

  // Stage 1: check if the file exists at all
  let raw: string;
  try {
    raw = await readFile(identityPath, "utf8");
  } catch {
    cachedDeviceIdentity = null;
    return null;
  }

  // Stage 2: parse and validate — warn if file exists but is malformed
  try {
    const data = JSON.parse(raw) as {
      deviceId?: string;
      publicKeyPem?: string;
      privateKeyPem?: string;
    };
    if (!data?.deviceId || !data?.publicKeyPem || !data?.privateKeyPem) {
      logger?.info(`[autonomous-loop] device.json missing required fields — device auth disabled.`);
      cachedDeviceIdentity = null;
      return null;
    }

    // Extract raw 32-byte Ed25519 public key from SPKI DER
    const pub = createPublicKey(data.publicKeyPem);
    const spki = pub.export({ type: "spki", format: "der" }) as Buffer;
    const rawKey = spki.subarray(-32);
    const publicKeyBase64 = rawKey.toString("base64").replace(/=+$/, "");

    cachedDeviceIdentity = { deviceId: data.deviceId, publicKeyBase64, privateKeyPem: data.privateKeyPem };
    return cachedDeviceIdentity;
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    logger?.info(`[autonomous-loop] Failed to parse device.json: ${msg} — device auth disabled.`);
    cachedDeviceIdentity = null;
    return null;
  }
};

const buildDeviceBlock = (
  identity: DeviceIdentity,
  nonce: string,
  gatewayToken: string,
): { id: string; publicKey: string; signature: string; signedAt: number; nonce: string } => {
  const signedAt = Date.now();
  const scopes = "operator.read,operator.write";
  const payload = `v2|${identity.deviceId}|gateway-client|backend|operator|${scopes}|${signedAt}|${gatewayToken}|${nonce}`;
  const key = createPrivateKey({ key: identity.privateKeyPem, format: "pem" });
  const sigBuffer = cryptoSign(null, Buffer.from(payload, "utf8"), key);
  return {
    id: identity.deviceId,
    publicKey: identity.publicKeyBase64,
    signature: sigBuffer.toString("base64"),
    signedAt,
    nonce,
  };
};

// ---------------------------------------------------------------------------
// Helpers — send message to session via Gateway WebSocket
// ---------------------------------------------------------------------------

const sendMessage = async (details: {
  sessionKey: string;
  gatewayToken: string;
  gatewayPort: number;
  message: string;
}): Promise<void> => {
  const WS = (
    globalThis as unknown as {
      WebSocket?: new (url: string) => {
        send: (d: string) => void;
        close: () => void;
        addEventListener: (type: string, fn: (e: { data?: unknown }) => void) => void;
        onopen?: (() => void) | null;
        onerror?: ((e: unknown) => void) | null;
        onclose?: (() => void) | null;
      };
    }
  ).WebSocket;

  if (!WS) throw new Error("[autonomous-loop] WebSocket unavailable in this runtime.");

  const deviceIdentity = await loadDeviceIdentity();
  const ws = new WS(`ws://127.0.0.1:${details.gatewayPort}`);
  const connectId = randomUUID();
  const chatId = randomUUID();
  const idempotencyKey = randomUUID();

  await new Promise<void>((resolve, reject) => {
    const timeout = setTimeout(() => {
      ws.close();
      reject(new Error(`[autonomous-loop] Gateway timeout. sessionKey=${details.sessionKey}`));
    }, GATEWAY_SEND_TIMEOUT_MS);

    const waitForAck = (expectedId: string): Promise<void> =>
      new Promise((res, rej) => {
        ws.addEventListener("message", (event) => {
          const raw = typeof event.data === "string" ? event.data : "";
          if (!raw) return;
          let parsed: Record<string, unknown>;
          try {
            parsed = JSON.parse(raw) as Record<string, unknown>;
          } catch {
            return;
          }
          if (parsed.type !== "res" || parsed.id !== expectedId) return;
          if (parsed.ok !== true) {
            rej(new Error(`[autonomous-loop] Gateway rejected request ${expectedId}: ${JSON.stringify(parsed.error)}`));
          } else {
            res();
          }
        });
        // Reject if the socket closes before the ack arrives
        ws.addEventListener("close", () => {
          rej(new Error(`[autonomous-loop] WebSocket closed before ack for ${expectedId}`));
        });
      });

    ws.addEventListener("message", async (event) => {
      const raw = typeof event.data === "string" ? event.data : "";
      if (!raw) return;
      try {
        const parsed = JSON.parse(raw) as Record<string, unknown>;
        if (parsed.type !== "event" || parsed.event !== "connect.challenge") return;

        const nonce =
          typeof (parsed.payload as Record<string, unknown>)?.nonce === "string"
            ? (parsed.payload as Record<string, unknown>).nonce as string
            : "";

        const connectParams: Record<string, unknown> = {
          minProtocol: 3,
          maxProtocol: 3,
          client: {
            id: "autonomous-loop",
            version: "1.0.0",
            platform: process.platform,
            mode: "backend",
          },
          role: "operator",
          scopes: ["operator.read", "operator.write"],
          caps: [],
          commands: [],
          permissions: {},
          auth: { token: details.gatewayToken },
          locale: "en-US",
          userAgent: "autonomous-loop",
        };

        if (deviceIdentity && nonce) {
          connectParams.device = buildDeviceBlock(deviceIdentity, nonce, details.gatewayToken);
        }

        try {
          const connectAck = waitForAck(connectId);
          ws.send(JSON.stringify({ type: "req", id: connectId, method: "connect", params: connectParams }));
          await connectAck;

          const chatAck = waitForAck(chatId);
          ws.send(JSON.stringify({
            type: "req",
            id: chatId,
            method: "chat.send",
            params: { sessionKey: details.sessionKey, message: details.message, idempotencyKey },
          }));
          await chatAck;

          clearTimeout(timeout);
          ws.close();
          resolve();
        } catch (err) {
          clearTimeout(timeout);
          ws.close();
          reject(err);
        }
      } catch {
        /* ignore non-JSON frames */
      }
    });

    ws.onerror = () => {
      clearTimeout(timeout);
      reject(new Error(`[autonomous-loop] WebSocket connection failed. sessionKey=${details.sessionKey}`));
    };
  });
};

// ---------------------------------------------------------------------------
// Plugin entry
// ---------------------------------------------------------------------------

export default definePluginEntry({
  id: "autonomous-loop",
  name: "Autonomous Loop",
  description: "Keeps the agent working by sending a follow-up message after each reply.",

  register(api) {
    const cfg = (api.pluginConfig ?? {}) as PluginConfig;
    const delayMs = cfg.delayMs ?? DEFAULT_DELAY_MS;

    api.registerHook(["gateway_start"], async () => {
      // Warm up device identity cache so the first send has no extra latency
      await loadDeviceIdentity(api.logger);
      await logLine("_plugin", `loaded | delayMs=${delayMs}`);
      api.logger.info(`[autonomous-loop] Loaded. delayMs=${delayMs}`);
    });

    api.registerHook(["agent_end"], async (event, ctx) => {
      const agentId = resolveAgentId(ctx);

      if (event.success !== true) {
        await logLine(agentId, `skipped-error | error=${String(event.error)}`);
        return;
      }

      const lastText = extractLastAssistantText(event.messages);
      if (!lastText) {
        await logLine(agentId, `skipped-no-assistant-text`);
        return;
      }

      // Content-based stop: agent signalled it has nothing left to do
      if (replyContainsStopToken(lastText)) {
        await logLine(agentId, `skipped-stop-token | sessionKey=${ctx.sessionKey} | preview=${JSON.stringify(lastText.slice(0, 80))}`);
        api.logger.info(`[autonomous-loop] Agent ${agentId} replied with stop token. Loop idle.`);
        return;
      }

      if (!ctx.sessionKey) {
        await logLine(agentId, `skipped-no-session-key`);
        return;
      }

      const gatewayPort = api.config?.gateway?.port;
      const gatewayToken = api.config?.gateway?.auth?.token;
      if (typeof gatewayPort !== "number" || !gatewayToken) {
        await logLine(agentId, `skipped-no-gateway-config`);
        return;
      }

      installStopWatcher(agentId, api.logger);

      if (await stopFileExists(agentId)) {
        await logLine(agentId, `skipped-stop-flag | sessionKey=${ctx.sessionKey}`);
        api.logger.info(`[autonomous-loop] Stop flag set for ${agentId}. Skipping.`);
        return;
      }

      // Cancel any existing countdown for this agent
      const existing = activeByAgent.get(agentId);
      if (existing) {
        clearTimeout(existing.timer);
        activeByAgent.delete(agentId);
      }

      await logLine(
        agentId,
        `countdown-started | sessionKey=${ctx.sessionKey} | delayMs=${delayMs} | preview=${JSON.stringify(lastText.slice(0, 100))}`,
      );

      const sessionKey = ctx.sessionKey;
      const timer = setTimeout(() => {
        void (async () => {
          activeByAgent.delete(agentId);

          if (await stopFileExists(agentId)) {
            await logLine(agentId, `countdown-cancelled-stop-flag | sessionKey=${sessionKey}`);
            return;
          }

          const message = resolveMessage(agentId, cfg);
          try {
            await sendMessage({ sessionKey, gatewayPort, gatewayToken, message });
            await logLine(
              agentId,
              `message-sent | sessionKey=${sessionKey} | preview=${JSON.stringify(message.slice(0, 80))}`,
            );
            api.logger.info(`[autonomous-loop] Sent to ${agentId} (${sessionKey})`);
          } catch (err) {
            const msg = err instanceof Error ? err.message : String(err);
            await logLine(agentId, `send-error | message=${JSON.stringify(msg)}`);
            api.logger.info(`[autonomous-loop] Send failed for ${agentId}: ${msg}`);
          }
        })();
      }, delayMs);

      activeByAgent.set(agentId, { timer, sessionKey });
    });
  },
});
