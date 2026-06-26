import type { OpenClawPluginApi, PluginRuntime } from "openclaw/plugin-sdk";
import { emptyPluginConfigSchema } from "openclaw/plugin-sdk";

// ─── Runtime singleton ───────────────────────────────────────
let pluginRuntime: PluginRuntime | null = null;
function getRuntime(): PluginRuntime {
  if (!pluginRuntime) throw new Error("HXA-Connect runtime not initialized");
  return pluginRuntime;
}

// ─── Types ───────────────────────────────────────────────────
interface HxaAccessConfig {
  dmPolicy?: "open" | "allowlist";
  dmAllowFrom?: string[];
  groupPolicy?: "open" | "allowlist" | "disabled";
  threads?: Record<string, { name?: string; allowFrom?: string[]; added_at?: string; mode?: "mention" | "smart" }>;
  threadMode?: "mention" | "smart";
}

interface HxaAccountConfig {
  enabled?: boolean;
  hubUrl?: string;
  agentToken?: string;
  agentName?: string;
  orgId?: string;
  agentId?: string;
  webhookPath?: string;
  webhookSecret?: string;
  access?: HxaAccessConfig;
  useWebSocket?: boolean;
}

interface HxaConnectChannelConfig {
  enabled?: boolean;
  /** Default hub URL for accounts that don't specify one */
  defaultHubUrl?: string;
  /** Single-account shorthand (used when no accounts map) */
  hubUrl?: string;
  agentToken?: string;
  agentName?: string;
  orgId?: string;
  agentId?: string;
  webhookPath?: string;
  webhookSecret?: string;
  access?: HxaAccessConfig;
  useWebSocket?: boolean;
  /** Multi-account map */
  accounts?: Record<string, HxaAccountConfig>;
}

function resolveHxaConnectConfig(cfg: any): HxaConnectChannelConfig {
  return migrateHxaConnectConfig((cfg?.channels?.["hxa-connect"] ?? {}) as HxaConnectChannelConfig);
}

function migrateAccessConfig(access: HxaAccessConfig | undefined): HxaAccessConfig | undefined {
  if (!access) return access;

  const threads = access.threads;
  const orgMode = access.threadMode;
  if ((!threads || typeof threads !== "object") && !("threadMode" in access)) {
    return access;
  }

  let changed = false;
  const nextThreads: NonNullable<HxaAccessConfig["threads"]> = {};

  for (const [threadId, thread] of Object.entries(threads || {})) {
    if (!thread || typeof thread !== "object") {
      nextThreads[threadId] = thread as any;
      continue;
    }
    if (thread.mode) {
      nextThreads[threadId] = thread;
      continue;
    }
    nextThreads[threadId] = { ...thread, mode: orgMode || "mention" };
    changed = true;
  }

  if (!changed && !("threadMode" in access)) {
    return access;
  }

  const nextAccess: HxaAccessConfig = {
    ...access,
    ...(threads && typeof threads === "object" ? { threads: nextThreads } : {}),
  };
  if ("threadMode" in nextAccess) {
    delete nextAccess.threadMode;
    changed = true;
  }

  return changed ? nextAccess : access;
}

function migrateAccountConfig(acct: HxaAccountConfig): HxaAccountConfig {
  return {
    ...acct,
    access: migrateAccessConfig(acct.access),
  };
}

function migrateHxaConnectConfig(hxa: HxaConnectChannelConfig): HxaConnectChannelConfig {
  const next: HxaConnectChannelConfig = {
    ...hxa,
    access: migrateAccessConfig(hxa.access),
  };
  if (hxa.accounts && typeof hxa.accounts === "object") {
    next.accounts = Object.fromEntries(
      Object.entries(hxa.accounts).map(([id, acct]) => [id, migrateAccountConfig(acct)]),
    );
  }
  return next;
}

function migrateRootConfig(cfg: any): { next: any; changed: boolean } {
  const next = structuredClone(cfg ?? {});
  next.channels = next.channels || {};
  const before = JSON.stringify(next.channels["hxa-connect"] ?? {});
  next.channels["hxa-connect"] = migrateHxaConnectConfig(
    (next.channels["hxa-connect"] ?? {}) as HxaConnectChannelConfig,
  );
  const after = JSON.stringify(next.channels["hxa-connect"] ?? {});
  return { next, changed: before !== after };
}

/** Resolve all account configs, supporting both single and multi-account. */
function resolveAccounts(hxa: HxaConnectChannelConfig): Record<string, HxaAccountConfig> {
  if (hxa.accounts && Object.keys(hxa.accounts).length > 0) {
    const resolved: Record<string, HxaAccountConfig> = {};
    for (const [id, acct] of Object.entries(hxa.accounts)) {
      resolved[id] = {
        ...acct,
        hubUrl: acct.hubUrl || hxa.defaultHubUrl || hxa.hubUrl,
      };
    }
    return resolved;
  }
  // Single-account fallback
  return {
    default: {
      enabled: hxa.enabled,
      hubUrl: hxa.hubUrl || hxa.defaultHubUrl,
      agentToken: hxa.agentToken,
      agentName: hxa.agentName,
      orgId: hxa.orgId,
      agentId: hxa.agentId,
      webhookPath: hxa.webhookPath,
      webhookSecret: hxa.webhookSecret,
      access: hxa.access,
      useWebSocket: hxa.useWebSocket,
    },
  };
}

function resolveAccountConfig(cfg: any, accountId?: string): HxaAccountConfig {
  const hxa = resolveHxaConnectConfig(cfg);
  const accounts = resolveAccounts(hxa);
  const id = accountId || "default";
  return accounts[id] || accounts[Object.keys(accounts)[0]] || {};
}

function resolveThreadMode(cfg: any, accountId: string | undefined, threadId: string): "mention" | "smart" {
  const acct = resolveAccountConfig(cfg, accountId);
  return acct.access?.threads?.[threadId]?.mode || "mention";
}

async function setThreadModeInConfig(
  runtime: PluginRuntime,
  cfg: any,
  accountId: string | undefined,
  threadId: string,
  mode: "mention" | "smart",
): Promise<{ accountId: string; threadId: string; mode: "mention" | "smart" }> {
  const nextCfg = structuredClone(cfg ?? {});
  nextCfg.channels = nextCfg.channels || {};
  nextCfg.channels["hxa-connect"] = nextCfg.channels["hxa-connect"] || {};
  const hxa = nextCfg.channels["hxa-connect"];

  if (hxa.accounts && Object.keys(hxa.accounts).length > 0) {
    const resolvedId = accountId || Object.keys(hxa.accounts)[0];
    hxa.accounts[resolvedId] = hxa.accounts[resolvedId] || {};
    hxa.accounts[resolvedId].access = hxa.accounts[resolvedId].access || {};
    hxa.accounts[resolvedId].access.threads = hxa.accounts[resolvedId].access.threads || {};
    const current = hxa.accounts[resolvedId].access.threads[threadId] || {};
    hxa.accounts[resolvedId].access.threads[threadId] = { ...current, mode };
    await runtime.config.writeConfigFile(nextCfg);
    return { accountId: resolvedId, threadId, mode };
  }

  hxa.access = hxa.access || {};
  hxa.access.threads = hxa.access.threads || {};
  const current = hxa.access.threads[threadId] || {};
  hxa.access.threads[threadId] = { ...current, mode };
  await runtime.config.writeConfigFile(nextCfg);
  return { accountId: accountId || "default", threadId, mode };
}

/** Count total configured accounts (for display prefix logic). */
function countConfiguredAccounts(cfg: any): number {
  const hxa = resolveHxaConnectConfig(cfg);
  return Object.keys(resolveAccounts(hxa)).length;
}

// ─── Access Control ──────────────────────────────────────────

function isDmAllowed(access: HxaAccessConfig | undefined, senderName: string): boolean {
  const policy = access?.dmPolicy || "open";
  if (policy === "open") return true;
  const name = String(senderName || "").toLowerCase();
  const allowFrom = (access?.dmAllowFrom || []).map((s) => String(s).toLowerCase());
  return allowFrom.includes(name);
}

function isThreadAllowed(access: HxaAccessConfig | undefined, threadId: string): boolean {
  const policy = access?.groupPolicy || "open";
  if (policy === "disabled") return false;
  if (policy === "open") return true;
  return !!access?.threads?.[threadId];
}

function isSenderAllowed(
  access: HxaAccessConfig | undefined,
  threadId: string,
  senderName: string,
): boolean {
  const tt = access?.threads?.[threadId];
  const af = Array.isArray(tt?.allowFrom) ? tt.allowFrom : [];
  if (af.length === 0) return true;
  if (af.includes("*")) return true;
  const name = String(senderName || "").toLowerCase();
  return af.some((a) => String(a).toLowerCase() === name);
}

// ─── Outbound: send message to HXA-Connect ───────────────────
const MAX_SEND_RETRIES = 2;
const RETRY_BASE_MS = 1000;
const CHANNEL_ID_RE = /^[a-zA-Z0-9_-]{1,64}$/;
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

/** Validate a path segment to prevent path traversal. */
function assertSafePathSegment(value: string, label: string): void {
  if (!value || value.includes("/") || value.includes("\\") || value.includes("..")) {
    throw new Error(`Invalid ${label}: ${value?.slice(0, 40)}`);
  }
}

/** Make an authenticated request to the HXA-Connect API with rate-limit retry. */
async function hubFetch(
  acct: HxaAccountConfig,
  path: string,
  init: RequestInit,
): Promise<Response> {
  if (!acct.hubUrl || !acct.hubUrl.startsWith("http")) {
    throw new Error("HXA-Connect hubUrl not configured or invalid");
  }
  const url = `${acct.hubUrl.replace(/\/$/, "")}${path}`;
  const headers: Record<string, string> = {
    Authorization: `Bearer ${acct.agentToken}`,
    ...((init.headers as Record<string, string>) ?? {}),
  };
  if (acct.orgId) {
    headers["X-Org-Id"] = acct.orgId;
  }
  if (init.body) {
    headers["Content-Type"] = "application/json";
  }

  for (let attempt = 0; attempt <= MAX_SEND_RETRIES; attempt++) {
    const resp = await fetch(url, { ...init, headers });
    if (resp.ok) return resp;

    if (resp.status === 429 && attempt < MAX_SEND_RETRIES) {
      const retryAfter = parseInt(resp.headers.get("Retry-After") || "", 10);
      const delayMs = retryAfter > 0 ? retryAfter * 1000 : RETRY_BASE_MS * (attempt + 1);
      console.warn(
        `[hxa-connect] rate limited on ${path}, retrying in ${delayMs}ms (attempt ${attempt + 1})`,
      );
      await new Promise((r) => setTimeout(r, delayMs));
      continue;
    }

    const body = await resp.text().catch(() => "");
    const err = new Error(`HXA-Connect ${path} failed: ${resp.status} ${body}`);
    (err as any).status = resp.status;
    (err as any).responseBody = body;
    throw err;
  }
  throw new Error(`HXA-Connect ${path} failed: exhausted retries`);
}

/** Send a DM to an agent by name (auto-creates direct channel). */
async function sendDM(
  acct: HxaAccountConfig,
  to: string,
  text: string,
): Promise<{ ok: boolean; messageId?: string }> {
  if (!acct.hubUrl || !acct.agentToken) {
    throw new Error("HXA-Connect not configured (missing hubUrl or agentToken)");
  }
  const resp = await hubFetch(acct, "/api/send", {
    method: "POST",
    body: JSON.stringify({ to, content: text, content_type: "text" }),
  });
  const result = (await resp.json()) as any;
  return { ok: true, messageId: result?.message?.id };
}

/** Send a message to a thread. */
async function sendToThread(
  acct: HxaAccountConfig,
  threadId: string,
  text: string,
  options?: { replyTo?: string },
): Promise<{ ok: boolean; messageId?: string }> {
  if (/^\s*\[SKIP\](?:\s|$)/i.test(text)) {
    console.info(`[hxa-connect] [SKIP] filtered for thread ${threadId}`);
    return { ok: true };
  }
  if (!acct.hubUrl || !acct.agentToken) {
    throw new Error("HXA-Connect not configured (missing hubUrl or agentToken)");
  }
  assertSafePathSegment(threadId, "thread_id");
  const body: Record<string, string> = { content: text, content_type: "text" };
  if (options?.replyTo) body.reply_to = options.replyTo;

  try {
    const resp = await hubFetch(acct, `/api/threads/${threadId}/messages`, {
      method: "POST",
      body: JSON.stringify(body),
    });
    const result = (await resp.json()) as any;
    return { ok: true, messageId: result?.message?.id };
  } catch (err: any) {
    // If reply_to fails (message deleted/invalid), retry without it
    if (options?.replyTo && (err?.status === 400 || err?.status === 404)) {
      console.warn(`[hxa-connect] reply_to ${options.replyTo} failed (${err?.status}), sending without reply`);
      const fallbackBody = { content: text, content_type: "text" };
      const resp = await hubFetch(acct, `/api/threads/${threadId}/messages`, {
        method: "POST",
        body: JSON.stringify(fallbackBody),
      });
      const result = (await resp.json()) as any;
      return { ok: true, messageId: result?.message?.id };
    }
    throw err;
  }
}

/** Route an outbound message to the correct destination (thread, channel, or DM). */
async function routeOutboundMessage(
  acct: HxaAccountConfig,
  target: string,
  text: string,
  options?: { replyTo?: string },
): Promise<{ ok: boolean; messageId?: string }> {
  // Case-insensitive thread: prefix
  if (/^thread:/i.test(target)) {
    return sendToThread(acct, target.slice("thread:".length), text, options);
  }
  // UUID — probe if it's a thread; only fall back to DM on 404 probe failure
  if (UUID_RE.test(target)) {
    let isThread = false;
    try {
      await hubFetch(acct, `/api/threads/${target}`, { method: "GET" });
      isThread = true;
    } catch (probeErr: any) {
      // Only treat 404/NOT_FOUND as "not a thread" — other errors should throw
      if (probeErr?.status === 404) {
        // Target is not a thread, fall through to DM
      } else {
        throw probeErr;
      }
    }
    if (isThread) {
      return await sendToThread(acct, target, text, options);
    }
    return await sendDM(acct, target, text);
  }
  // Channel ID
  if (CHANNEL_ID_RE.test(target) && target.length > 20) {
    return sendToChannel(acct, target, text);
  }
  // Default: DM by bot name
  return sendDM(acct, target, text);
}

/** Send a message to a specific channel by ID. */
async function sendToChannel(
  acct: HxaAccountConfig,
  channelId: string,
  text: string,
): Promise<{ ok: boolean; messageId?: string }> {
  if (!acct.hubUrl || !acct.agentToken) {
    throw new Error("HXA-Connect not configured (missing hubUrl or agentToken)");
  }
  if (!CHANNEL_ID_RE.test(channelId)) {
    throw new Error(`Invalid channel_id: ${channelId.slice(0, 40)}`);
  }
  const resp = await hubFetch(acct, `/api/channels/${channelId}/messages`, {
    method: "POST",
    body: JSON.stringify({ content: text, content_type: "text" }),
  });
  const result = (await resp.json()) as any;
  return { ok: true, messageId: result?.message?.id };
}

/** Fetch channel metadata. */
async function fetchChannelInfo(
  acct: HxaAccountConfig,
  channelId: string,
): Promise<{ type: string; name: string | null } | null> {
  if (!CHANNEL_ID_RE.test(channelId)) return null;
  try {
    const resp = await hubFetch(acct, `/api/channels/${channelId}`, { method: "GET" });
    const data = (await resp.json()) as any;
    return { type: data.type, name: data.name };
  } catch {
    return null;
  }
}

// ─── WebSocket Connection Manager ────────────────────────────

interface WsConnection {
  client: any; // HxaConnectClient
  threadCtx: any; // ThreadContext
  accountId: string;
  config: HxaAccountConfig;
  disconnect: () => void;
}

const wsConnections = new Map<string, WsConnection>();

/** Format display prefix for log/message context. */
function displayPrefix(accountId: string, cfg: any): string {
  const totalAccounts = countConfiguredAccounts(cfg);
  if (totalAccounts <= 1 && accountId === "default") return "HXA-Connect";
  return `HXA:${accountId}`;
}

async function connectAccount(
  accountId: string,
  acct: HxaAccountConfig,
  cfg: any,
  log: any,
  abortSignal?: AbortSignal,
) {
  // Guard against duplicate connections
  if (wsConnections.has(accountId)) {
    log?.warn?.(`[hxa-connect:${accountId}] Already connected, skipping`);
    return;
  }

  // Dynamic import SDK
  let HxaConnectClient: any;
  let ThreadContext: any;
  try {
    const sdk = await import("@coco-xyz/hxa-connect-sdk");
    HxaConnectClient = sdk.HxaConnectClient;
    ThreadContext = sdk.ThreadContext;
  } catch (err: any) {
    log?.error?.(`[hxa-connect:${accountId}] Failed to load hxa-connect-sdk: ${err.message}`);
    return;
  }

  const dp = displayPrefix(accountId, cfg);
  const lp = `[hxa-connect:${accountId}]`;

  const client = new HxaConnectClient({
    url: acct.hubUrl,
    token: acct.agentToken,
    orgId: acct.orgId,
    reconnect: {
      enabled: true,
      initialDelay: 3000,
      maxDelay: 60000,
      backoffFactor: 1.5,
    },
  });

  const isSelf = (id: string, metadata?: any) => {
    if (!acct.agentId || id !== acct.agentId) return false;
    // Human-authored messages via Web UI use the bot's token but should not
    // be treated as self-echo — let them through.
    const meta =
      typeof metadata === "string"
        ? (() => { try { return JSON.parse(metadata); } catch { return null; } })()
        : metadata;
    if (meta?.provenance?.authored_by === "human") return false;
    return true;
  };
  const access = acct.access || {};

  // ─── DM Handler ──────────────────────────────────────────
  client.on("message", (msg: any) => {
    const sender = msg.sender_name || "unknown";
    const content = msg.message?.content || msg.content || "";
    if (isSelf(msg.message?.sender_id, msg.message?.metadata)) return;

    if (!isDmAllowed(access, sender)) {
      log?.info?.(`${lp} DM from ${sender} rejected (dmPolicy: ${access.dmPolicy || "open"})`);
      return;
    }

    log?.info?.(`${lp} DM from ${sender}: ${content.substring(0, 80)}`);
    dispatchInbound({
      cfg,
      accountId,
      senderName: sender,
      senderId: msg.message?.sender_id || sender,
      content,
      messageId: msg.message?.id,
      chatType: "direct",
      replyTarget: sender,
      displayPrefix: dp,
    });
  });

  // ─── Thread Handlers ─────────────────────────────────────
  const agentName = acct.agentName || "cococlaw";
  const threadCtx = new ThreadContext(client, {
    botNames: [agentName],
    botId: acct.agentId || undefined,
    triggerPatterns: [/^/],
  });

  function getThreadMode(threadId: string): "mention" | "smart" {
    return access.threads?.[threadId]?.mode || "mention";
  }

  const mentionRe = new RegExp(
    `@${agentName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`,
    "i",
  );

  function extractText(msg: any): string {
    const parts = [msg.content || ""];
    if (msg.parts) {
      for (const part of msg.parts) {
        if ("content" in part && typeof part.content === "string") {
          parts.push(part.content);
        }
      }
    }
    return parts.join(" ");
  }

  /** Display-friendly sender name (human provenance aware). */
  function msgSender(msg: any): string {
    const botName = msg.sender_name || msg.sender_id || "unknown";
    const meta =
      typeof msg.metadata === "string"
        ? (() => { try { return JSON.parse(msg.metadata); } catch { return null; } })()
        : msg.metadata;
    if (meta?.provenance?.authored_by === "human" && meta.provenance.owner_name) {
      return `${meta.provenance.owner_name} (via ${botName})`;
    }
    return botName;
  }

  threadCtx.onMention(({ threadId, message, snapshot }: any) => {
    const sender = msgSender(message);
    const content = message.content || "";

    if (!isThreadAllowed(access, threadId)) {
      log?.info?.(
        `${lp} Thread ${threadId} rejected (groupPolicy: ${access.groupPolicy || "open"})`,
      );
      return;
    }
    if (!isSenderAllowed(access, threadId, sender)) {
      log?.info?.(`${lp} Sender ${sender} rejected in thread ${threadId}`);
      return;
    }

    const isRealMention = mentionRe.test(extractText(message));
    const threadMode = getThreadMode(threadId);

    if (threadMode === "mention" && !isRealMention) {
      return;
    }

    // Build message with XML tags (consistent with Lark/TG format)
    const parts: string[] = [`[${dp} Thread:${threadId}] ${sender} said: `];

    // Thread context: previous messages (excluding trigger)
    const contextMsgs = (snapshot.newMessages || []).filter((m: any) => m.id !== message.id);
    if (contextMsgs.length > 0) {
      const lines = contextMsgs.map((m: any) => `[${msgSender(m)}]: ${m.content || ""}`);
      parts.push(`<thread-context>\n${lines.join("\n")}\n</thread-context>\n\n`);
    }

    // Smart mode hint
    if (!isRealMention && threadMode === "smart") {
      parts.push(
        "<smart-mode>\nDecide whether to respond. Reply with exactly [SKIP] when a response is unnecessary.\n</smart-mode>\n\n",
      );
    }

    // Reply-to context (like TG's replying-to format)
    if (message.reply_to_message) {
      const reply = message.reply_to_message;
      const replySender = (reply.sender_name || reply.sender_id || "unknown").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      // Escape all < and > in reply content to prevent tag injection
      const replyContent = (reply.content || "").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      parts.push(`<replying-to>\n[${replySender}]: ${replyContent}\n</replying-to>\n\n`);
    }

    // Current message
    parts.push(`<current-message>\n${content}\n</current-message>`);

    const formattedContent = parts.join("");
    log?.info?.(`${lp} Thread ${threadId} from ${sender} (${snapshot.bufferedCount} buffered)`);

    dispatchInbound({
      cfg,
      accountId,
      senderName: sender,
      senderId: message.sender_id || sender,
      content: formattedContent,
      messageId: message.id,
      chatType: "group",
      groupSubject: `thread:${threadId}`,
      replyTarget: `thread:${threadId}`,
      replyToMessageId: message.id,
      ...(message.reply_to_message ? {
        replyToBody: message.reply_to_message.content || "",
        replyToSender: message.reply_to_message.sender_name || message.reply_to_message.sender_id || "unknown",
      } : {}),
      displayPrefix: dp,
    });
  });

  // Buffer thread messages (ThreadContext handles delivery via onMention)
  client.on("thread_message", (msg: any) => {
    const message = msg.message || {};
    if (isSelf(message.sender_id, message.metadata)) return;
    const sender = message.sender_name || message.sender_id || "unknown";
    const content = message.content || "";
    log?.debug?.(
      `${lp} Thread ${msg.thread_id} from ${sender} (buffered): ${content.substring(0, 80)}`,
    );
  });

  // Thread lifecycle events
  client.on("thread_created", (msg: any) => {
    const thread = msg.thread || {};
    const topic = thread.topic || "untitled";
    const tags = thread.tags?.length ? thread.tags.join(", ") : "none";
    log?.info?.(`${lp} Thread created: "${topic}" (tags: ${tags})`);

    dispatchInbound({
      cfg,
      accountId,
      senderName: "system",
      senderId: "system",
      content: `[${dp} Thread] New thread created: "${topic}" (tags: ${tags}, id: ${thread.id})`,
      chatType: "group",
      groupSubject: `thread:${thread.id}`,
      replyTarget: `thread:${thread.id}`,
      displayPrefix: dp,
    });
  });

  client.on("thread_updated", (msg: any) => {
    const thread = msg.thread || {};
    const changes = msg.changes || [];
    log?.info?.(`${lp} Thread updated: "${thread.topic}" changes: ${changes.join(", ")}`);

    dispatchInbound({
      cfg,
      accountId,
      senderName: "system",
      senderId: "system",
      content: `[${dp} Thread:${thread.id}] Thread "${thread.topic}" updated: ${changes.join(", ")} (status: ${thread.status})`,
      chatType: "group",
      groupSubject: `thread:${thread.id}`,
      replyTarget: `thread:${thread.id}`,
      displayPrefix: dp,
    });
  });

  client.on("thread_status_changed", (msg: any) => {
    const by = msg.by ? ` (by ${msg.by})` : "";
    log?.info?.(`${lp} Thread status: "${msg.topic}" ${msg.from} -> ${msg.to}${by}`);

    dispatchInbound({
      cfg,
      accountId,
      senderName: "system",
      senderId: "system",
      content: `[${dp} Thread:${msg.thread_id}] Thread "${msg.topic}" status changed: ${msg.from} -> ${msg.to}${by}`,
      chatType: "group",
      groupSubject: `thread:${msg.thread_id}`,
      replyTarget: `thread:${msg.thread_id}`,
      displayPrefix: dp,
    });
  });

  client.on("thread_artifact", (msg: any) => {
    const artifact = msg.artifact || {};
    const action = msg.action || "added";
    log?.info?.(`${lp} Thread ${msg.thread_id} artifact ${action}: ${artifact.artifact_key}`);

    dispatchInbound({
      cfg,
      accountId,
      senderName: "system",
      senderId: "system",
      content: `[${dp} Thread:${msg.thread_id}] Artifact ${action}: "${artifact.title || artifact.artifact_key}" (type: ${artifact.type})`,
      chatType: "group",
      groupSubject: `thread:${msg.thread_id}`,
      replyTarget: `thread:${msg.thread_id}`,
      displayPrefix: dp,
    });
  });

  client.on("thread_participant", (msg: any) => {
    const botName = msg.bot_name || msg.bot_id;
    const by = msg.by ? ` (by ${msg.by})` : "";
    const labelTag = msg.label ? ` [${msg.label}]` : "";
    log?.info?.(`${lp} Thread ${msg.thread_id}: ${botName} ${msg.action}${by}`);

    dispatchInbound({
      cfg,
      accountId,
      senderName: "system",
      senderId: "system",
      content: `[${dp} Thread:${msg.thread_id}] ${botName}${labelTag} ${msg.action} the thread${by}`,
      chatType: "group",
      groupSubject: `thread:${msg.thread_id}`,
      replyTarget: `thread:${msg.thread_id}`,
      displayPrefix: dp,
    });
  });

  // Bot presence
  client.on("bot_online", (msg: any) => {
    log?.info?.(`${lp} ${msg.bot?.name || "unknown"} is online`);
  });
  client.on("bot_offline", (msg: any) => {
    log?.info?.(`${lp} ${msg.bot?.name || "unknown"} is offline`);
  });

  // Connection lifecycle
  client.on("reconnecting", ({ attempt, delay }: any) => {
    log?.warn?.(`${lp} Reconnecting (attempt ${attempt}, delay ${delay}ms)...`);
  });
  client.on("reconnected", ({ attempts }: any) => {
    log?.info?.(`${lp} Reconnected after ${attempts} attempt(s)`);
  });
  client.on("reconnect_failed", ({ attempts }: any) => {
    log?.error?.(`${lp} Reconnect failed after ${attempts} attempts`);
  });
  client.on("error", (err: any) => {
    log?.error?.(`${lp} Error: ${err?.message || err}`);
  });

  client.on("session_invalidated", ({ code, reason }: any) => {
    log?.error?.(`${lp} Session invalidated (code ${code}): ${reason || "unknown"}`);
    log?.error?.(`${lp} SDK will not auto-reconnect — connection lost`);
    threadCtx.stop();
    client.disconnect();
    wsConnections.delete(accountId);
  });

  // Listen for abort signal to disconnect gracefully
  if (abortSignal) {
    abortSignal.addEventListener(
      "abort",
      () => {
        log?.info?.(`${lp} Abort signal received, disconnecting`);
        threadCtx.stop();
        client.disconnect();
        wsConnections.delete(accountId);
      },
      { once: true },
    );
  }

  // Connect
  log?.info?.(`${lp} Connecting as "${agentName}" to ${acct.hubUrl}`);
  await client.connect();
  log?.info?.(`${lp} WebSocket connected`);
  await threadCtx.start();
  log?.info?.(`${lp} ThreadContext started (per-thread mode, default: mention, filter: @${agentName})`);

  wsConnections.set(accountId, {
    client,
    threadCtx,
    accountId,
    config: acct,
    disconnect: () => {
      threadCtx.stop();
      client.disconnect();
    },
  });
}

// ─── Inbound Dispatch (shared by WS + Webhook) ──────────────

interface InboundParams {
  cfg: any;
  accountId: string;
  senderName: string;
  senderId: string;
  content: string;
  messageId?: string;
  chatType: "direct" | "group";
  groupSubject?: string;
  replyTarget: string; // bot name for DM, "thread:<id>" for threads
  replyToMessageId?: string; // message ID for reply-to on outbound
  replyToBody?: string; // reply-to message content (for context)
  replyToSender?: string; // reply-to sender name (for context)
  displayPrefix: string;
}

async function dispatchInbound(params: InboundParams) {
  const core = getRuntime();
  const {
    cfg,
    accountId,
    senderName,
    senderId,
    content,
    messageId,
    chatType,
    groupSubject,
    replyTarget,
  } = params;

  const from = `hxa-connect:${senderId}`;
  const to = `hxa-connect:${accountId}`;

  const route = core.channel.routing.resolveAgentRoute({
    channel: "hxa-connect",
    from,
    chatType,
    groupSubject: chatType === "group" ? (groupSubject || replyTarget) : undefined,
    cfg,
  });

  const envelopeOptions = core.channel.reply.resolveEnvelopeFormatOptions(cfg);
  const formattedBody = core.channel.reply.formatAgentEnvelope({
    channel: "HXA-Connect",
    from: senderName,
    timestamp: new Date(),
    envelope: envelopeOptions,
    body: content,
  });

  const ctxPayload = core.channel.reply.finalizeInboundContext({
    Body: formattedBody,
    BodyForAgent: content,
    RawBody: content,
    CommandBody: content,
    From: from,
    To: to,
    SessionKey: route.sessionKey,
    AccountId: accountId,
    ChatType: chatType,
    GroupSubject: chatType === "group" ? (groupSubject || replyTarget) : undefined,
    SenderName: senderName,
    SenderId: senderId,
    Provider: "hxa-connect" as const,
    Surface: "hxa-connect" as const,
    MessageSid: messageId || `hxa-connect-${Date.now()}`,
    Timestamp: Date.now(),
    WasMentioned: true,
    CommandAuthorized: true,
    OriginatingChannel: "hxa-connect" as const,
    OriginatingTo: to,
    ConversationLabel: chatType === "group" ? (groupSubject || senderName) : senderName,
    ...(params.replyToMessageId ? { ReplyToId: params.replyToMessageId } : {}),
    ...(params.replyToBody ? { ReplyToBody: params.replyToBody } : {}),
    ...(params.replyToSender ? { ReplyToSender: params.replyToSender } : {}),
  });

  const acct = resolveAccountConfig(cfg, accountId);
  const isThread = replyTarget.startsWith("thread:");
  const threadId = isThread ? replyTarget.slice("thread:".length) : undefined;

  await core.channel.reply.dispatchReplyWithBufferedBlockDispatcher({
    ctx: ctxPayload,
    cfg,
    dispatcherOptions: {
      deliver: async (payload: any) => {
        const text =
          typeof payload === "string"
            ? payload
            : payload?.text ?? payload?.body ?? String(payload);
        if (!text?.trim()) return;

        try {
          if (threadId) {
            await sendToThread(acct, threadId, text, {
              replyTo: params.replyToMessageId,
            });
          } else {
            await sendDM(acct, replyTarget, text);
          }
        } catch (err: any) {
          console.error(`[hxa-connect] reply failed:`, err);
        }
      },
      onError: (err: any, info: any) => {
        console.error(`[hxa-connect] ${info?.kind ?? "unknown"} reply error:`, err);
      },
    },
    replyOptions: {},
  });
}

// ─── Channel Plugin ──────────────────────────────────────────

const hxaConnectChannel = {
  id: "hxa-connect" as const,
  meta: {
    id: "hxa-connect" as const,
    label: "HXA-Connect",
    selectionLabel: "HXA-Connect (Agent-to-Agent)",
    docsPath: "/channels/hxa-connect",
    docsLabel: "hxa-connect",
    blurb: "Agent-to-agent messaging via HXA-Connect with WebSocket + webhook support.",
    aliases: ["hxa-connect", "hub"],
    order: 90,
  },
  capabilities: {
    chatTypes: ["direct" as const, "channel" as const],
    polls: false,
    threads: true,
    media: false,
    reactions: false,
    edit: false,
    reply: false,
  },
  messaging: {
    targetResolver: {
      hint: 'Use bot name for DMs (e.g. "zylos01") or "thread:<uuid>" for threads',
      looksLikeId: (raw: string, _normalized?: string): boolean => {
        const trimmed = raw.trim();
        if (!trimmed) return false;
        // thread:<uuid> format
        if (/^thread:/i.test(trimmed)) return true;
        // UUID format (could be a thread or channel ID)
        if (UUID_RE.test(trimmed)) return true;
        // For HXA-Connect, any non-empty string is a valid target
        // (bot name for DM, or other identifier) — sendText handles resolution
        return true;
      },
    },
  },
  config: {
    listAccountIds: (cfg: any) => {
      const hxa = resolveHxaConnectConfig(cfg);
      return Object.keys(resolveAccounts(hxa));
    },
    resolveAccount: (cfg: any, accountId?: string) => {
      const acct = resolveAccountConfig(cfg, accountId);
      return {
        accountId: accountId || "default",
        enabled: acct.enabled !== false,
        configured: !!(acct.hubUrl && acct.agentToken),
        hubUrl: acct.hubUrl,
        agentToken: acct.agentToken,
        webhookPath: acct.webhookPath ?? "/hxa-connect/inbound",
        webhookSecret: acct.webhookSecret,
        config: acct,
      };
    },
  },
  outbound: {
    deliveryMode: "direct" as const,
    textChunkLimit: 8000,
    sendText: async (params: {
      cfg: any;
      to: string;
      text: string;
      accountId?: string;
      replyToId?: string;
    }) => {
      const acct = resolveAccountConfig(params.cfg, params.accountId);
      const result = await routeOutboundMessage(acct, params.to, params.text, {
        replyTo: params.replyToId,
      });
      return { channel: "hxa-connect" as const, ...result };
    },
    sendMedia: async (params: {
      cfg: any;
      to: string;
      text: string;
      mediaUrl?: string;
      accountId?: string;
      replyToId?: string;
    }) => {
      // HXA-Connect doesn't support native media — send as text with URL
      const caption = params.text || "";
      const mediaUrl = params.mediaUrl || "";
      const text = [caption, mediaUrl].filter(Boolean).join("\n");
      const acct = resolveAccountConfig(params.cfg, params.accountId);

      const result = await routeOutboundMessage(acct, params.to, text, {
        replyTo: params.replyToId,
      });
      return { channel: "hxa-connect" as const, ...result };
    },
  },
  gateway: {
    startAccount: async (ctx: any) => {
      const acct = resolveAccountConfig(ctx.cfg, ctx.accountId);
      const log = ctx.log;
      const accountId = ctx.accountId || "default";
      log?.info?.(`hxa-connect: starting account ${accountId}`);
      ctx.setStatus?.({ accountId });

      // Start WebSocket connection for this account
      if (acct.useWebSocket !== false && acct.hubUrl && acct.agentToken) {
        try {
          await connectAccount(accountId, acct, ctx.cfg, log, ctx.abortSignal);
        } catch (err: any) {
          log?.warn?.(
            `hxa-connect: WebSocket failed for ${accountId}: ${err.message}. Falling back to webhook-only.`,
          );
        }
      }

      // Keep the account task alive until the gateway aborts/stops it.
      await new Promise<void>((resolve) => {
        if (ctx.abortSignal?.aborted) return resolve();
        ctx.abortSignal?.addEventListener("abort", () => resolve(), { once: true });
      });
    },
    stopAccount: async (ctx: any) => {
      const accountId = ctx.accountId || "default";
      const log = ctx.log;
      const conn = wsConnections.get(accountId);
      if (conn) {
        conn.disconnect();
        wsConnections.delete(accountId);
      }
      log?.info?.(`hxa-connect: stopped account ${accountId}`);
    },
  },
};

// ─── Inbound webhook handler (fallback / non-WS mode) ────────
async function handleInboundWebhook(req: any, res: any) {
  const core = getRuntime();
  const cfg = await core.config.loadConfig();

  // Determine which account this webhook is for
  const requestPath = req.url || req.path || "";
  const hxa = resolveHxaConnectConfig(cfg);
  const accounts = resolveAccounts(hxa);

  let matchedAccountId = "default";
  for (const [id, acct] of Object.entries(accounts)) {
    const webhookPath = acct.webhookPath ?? "/hxa-connect/inbound";
    if (requestPath.includes(webhookPath.replace(/^\//, ""))) {
      matchedAccountId = id;
      break;
    }
  }

  const acct = accounts[matchedAccountId] || accounts[Object.keys(accounts)[0]];

  // Verify webhook secret if configured
  if (acct?.webhookSecret) {
    const authHeader = req.headers?.authorization ?? "";
    const token = authHeader.startsWith("Bearer ") ? authHeader.slice(7) : "";
    if (token !== acct.webhookSecret) {
      res.writeHead(401, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Unauthorized" }));
      return;
    }
  }

  // Parse body with error handling
  let body: any;
  try {
    if (typeof req.body === "object" && req.body !== null) {
      body = req.body;
    } else {
      const chunks: Buffer[] = [];
      for await (const chunk of req) chunks.push(chunk);
      body = JSON.parse(Buffer.concat(chunks).toString("utf-8"));
    }
  } catch (err: any) {
    res.writeHead(400, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: `Invalid JSON body: ${err.message}` }));
    return;
  }

  // Parse webhook payload (v1 envelope or legacy flat format)
  let channel_id: string | undefined;
  let sender_name: string | undefined;
  let sender_id: string | undefined;
  let content: string | undefined;
  let message_id: string | undefined;
  let chat_type: string | undefined;
  let group_name: string | undefined;
  let reply_to_message: any | undefined;

  if (body.webhook_version === "1") {
    const msg = body.message;
    channel_id = body.channel_id;
    sender_name = body.sender_name;
    sender_id = msg?.sender_id;
    content = msg?.content;
    message_id = msg?.id;
    reply_to_message = msg?.reply_to_message;

    if (channel_id && acct) {
      const channelInfo = await fetchChannelInfo(acct, channel_id);
      if (channelInfo) {
        chat_type = channelInfo.type;
        group_name = channelInfo.name ?? undefined;
      } else {
        console.warn(
          `[hxa-connect] fetchChannelInfo failed for ${channel_id}, defaulting to channel-based reply`,
        );
        chat_type = "group";
      }
    }
  } else {
    channel_id = body.channel_id;
    sender_name = body.sender_name;
    sender_id = body.sender_id;
    content = body.content;
    message_id = body.message_id;
    chat_type = body.chat_type;
    group_name = body.group_name;
    reply_to_message = body.reply_to_message;
  }

  if (!content || !sender_name) {
    res.writeHead(400, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "Missing content or sender_name" }));
    return;
  }

  // Access control
  const access = acct?.access || {};
  const isGroup = chat_type === "group";

  if (!isGroup && !isDmAllowed(access, sender_name)) {
    console.log(
      `[hxa-connect] DM from ${sender_name} rejected (dmPolicy: ${access.dmPolicy || "open"})`,
    );
    res.writeHead(403, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "Forbidden" }));
    return;
  }

  // Thread access control for group messages
  if (isGroup && channel_id) {
    if (!isThreadAllowed(access, channel_id)) {
      console.log(
        `[hxa-connect] Thread ${channel_id} rejected (groupPolicy: ${access.groupPolicy || "open"})`,
      );
      res.writeHead(403, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Forbidden" }));
      return;
    }
    if (!isSenderAllowed(access, channel_id, sender_name)) {
      console.log(`[hxa-connect] Sender ${sender_name} rejected in thread ${channel_id}`);
      res.writeHead(403, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Forbidden" }));
      return;
    }
  }

  console.log(`[hxa-connect] inbound from ${sender_name}: ${content.slice(0, 100)}`);

  // Inject reply-to context (matching WS path behavior)
  let finalContent = content;
  if (reply_to_message && typeof reply_to_message === "object") {
    const rawSender = String(reply_to_message.sender_name || reply_to_message.sender_id || "unknown");
    const rawContent = String(reply_to_message.content || "");
    const replySender = rawSender.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    const replyContent = rawContent.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    finalContent = `<replying-to>\n[${replySender}]: ${replyContent}\n</replying-to>\n\n${content}`;
  }

  const dp = displayPrefix(matchedAccountId, cfg);
  const replyTarget = isGroup ? (channel_id || sender_name) : sender_name;

  await dispatchInbound({
    cfg,
    accountId: matchedAccountId,
    senderName: sender_name,
    senderId: sender_id || sender_name,
    content: finalContent,
    messageId: message_id,
    chatType: isGroup ? "group" : "direct",
    groupSubject: isGroup ? (group_name || channel_id) : undefined,
    replyTarget,
    replyToMessageId: message_id,
    ...(reply_to_message ? {
      replyToBody: reply_to_message.content || "",
      replyToSender: reply_to_message.sender_name || reply_to_message.sender_id || "unknown",
    } : {}),
    displayPrefix: dp,
  });

  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ ok: true }));
}

// ─── Agent Tool Registration ─────────────────────────────────

function registerTools(api: OpenClawPluginApi) {
  /** Create a short-lived SDK client for REST API calls. */
  async function createClient(acct: HxaAccountConfig): Promise<any> {
    const sdk = await import("@coco-xyz/hxa-connect-sdk");
    return new sdk.HxaConnectClient({
      url: acct.hubUrl,
      token: acct.agentToken,
      orgId: acct.orgId,
    });
  }

  api.registerTool({
    name: "hxa_connect",
    description: `Interact with HXA-Connect Hub (agent-to-agent collaboration platform).

Commands:
  Query: peers, threads, thread, messages, profile, org, inbox
  Thread ops: thread-create, thread-update, thread-join, thread-leave, thread-invite
  Artifacts: artifact-add, artifact-update, artifact-list, artifact-versions
  Profile: profile-update, rename
  Admin: role, ticket-create, rotate-secret, set-thread-mode, show-thread-mode

To send messages, use the message tool: message(action="send", channel="hxa-connect", target="bot_name" or "thread:<id>", message="...")
Important: In threads, @mention the target bot in your message text (e.g. "@bot_name hello") — bots in mention mode only receive messages where they are @mentioned.`,
    parameters: {
      type: "object",
      properties: {
        command: {
          type: "string",
          enum: [
            "peers",
            "threads",
            "thread",
            "messages",
            "profile",
            "org",
            "inbox",
            "thread-create",
            "thread-update",
            "thread-join",
            "thread-leave",
            "thread-invite",
            "artifact-add",
            "artifact-update",
            "artifact-list",
            "artifact-versions",
            "profile-update",
            "rename",
            "role",
            "ticket-create",
            "rotate-secret",
            "set-thread-mode",
            "show-thread-mode",
          ],
          description: "The HXA-Connect command to execute",
        },
        account: {
          type: "string",
          description: "Account ID for multi-account setups (uses default if omitted)",
        },
        // Query params
        thread_id: {
          type: "string",
          description: "Thread ID (for thread, messages, thread-update, thread-join, thread-leave, thread-invite, artifact-*)",
        },
        thread_mode: {
          type: "string",
          enum: ["mention", "smart"],
          description: "Per-thread mode for set-thread-mode",
        },
        status: {
          type: "string",
          description: "Thread status filter (for threads: active|blocked|reviewing|resolved|closed) or new status (for thread-update)",
        },
        limit: {
          type: "number",
          description: "Max results to return (for messages)",
        },
        since: {
          type: "number",
          description: "Timestamp in ms — return items after this time (for messages, inbox)",
        },
        before: {
          type: "number",
          description: "Timestamp in ms — return items before this time (for messages)",
        },
        // Thread create/update params
        topic: {
          type: "string",
          description: "Thread topic (for thread-create, thread-update)",
        },
        tags: {
          type: "array",
          items: { type: "string" },
          description: "Thread tags (for thread-create)",
        },
        participants: {
          type: "array",
          items: { type: "string" },
          description: "Bot names to invite (for thread-create)",
        },
        context: {
          type: "string",
          description: "Thread context text (for thread-create, thread-update)",
        },
        close_reason: {
          type: "string",
          enum: ["manual", "timeout", "error"],
          description: "Reason for closing (for thread-update with status=closed)",
        },
        // Thread invite params
        bot_id: {
          type: "string",
          description: "Bot name or ID (for thread-invite, role)",
        },
        label: {
          type: "string",
          description: "Role label for participant (for thread-invite)",
        },
        // Artifact params
        artifact_key: {
          type: "string",
          description: "Artifact key identifier (for artifact-add, artifact-update, artifact-versions)",
        },
        artifact_type: {
          type: "string",
          enum: ["markdown", "code", "text", "link"],
          description: "Artifact type (for artifact-add)",
        },
        title: {
          type: "string",
          description: "Artifact title (for artifact-add, artifact-update)",
        },
        body: {
          type: "string",
          description: "Artifact content body (for artifact-add, artifact-update)",
        },
        url: {
          type: "string",
          description: "URL for link artifacts (for artifact-add)",
        },
        language: {
          type: "string",
          description: "Programming language for code artifacts (for artifact-add)",
        },
        // Profile params
        bio: {
          type: "string",
          description: "Bot bio (for profile-update)",
        },
        role_text: {
          type: "string",
          description: "Bot role description (for profile-update)",
        },
        team: {
          type: "string",
          description: "Team name (for profile-update)",
        },
        status_text: {
          type: "string",
          description: "Status text (for profile-update)",
        },
        timezone: {
          type: "string",
          description: "Timezone (for profile-update)",
        },
        new_name: {
          type: "string",
          description: "New bot name (for rename)",
        },
        // Admin params
        bot_role: {
          type: "string",
          enum: ["admin", "member"],
          description: "Role to assign (for role command)",
        },
        reusable: {
          type: "boolean",
          description: "Whether invite ticket is reusable (for ticket-create)",
        },
        expires_in: {
          type: "number",
          description: "Ticket expiry in seconds (for ticket-create)",
        },
      },
      required: ["command"],
    },
    async execute(_id: string, params: Record<string, any>) {
      try {
        const cfg = await getRuntime().config.loadConfig();
        const acct = resolveAccountConfig(cfg, params.account);

        if (!acct.hubUrl || !acct.agentToken) {
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({
                  error: "HXA-Connect not configured (missing hubUrl or agentToken)",
                }),
              },
            ],
          };
        }

        const client = await createClient(acct);
        let result: any;

        switch (params.command) {
          // ─── Query ──────────────────────────────────────────
          case "peers": {
            result = await client.listPeers();
            break;
          }

          case "threads": {
            const opts = params.status ? { status: params.status } : undefined;
            result = await client.listThreads(opts);
            break;
          }

          case "thread": {
            if (!params.thread_id) {
              return errResult("thread_id is required");
            }
            result = await client.getThread(params.thread_id);
            break;
          }

          case "messages": {
            if (!params.thread_id) {
              return errResult("thread_id is required");
            }
            const opts: any = {};
            if (params.limit != null) opts.limit = params.limit;
            if (params.since != null) opts.since = params.since;
            if (params.before != null) opts.before = params.before;
            result = await client.getThreadMessages(params.thread_id, opts);
            break;
          }

          case "profile": {
            result = await client.getProfile();
            break;
          }

          case "org": {
            result = await client.getOrgInfo();
            break;
          }

          case "inbox": {
            if (params.since == null) {
              return errResult("since (timestamp in ms) is required for inbox");
            }
            result = await client.inbox(params.since);
            break;
          }

          // ─── Thread Operations ──────────────────────────────
          case "thread-create": {
            if (!params.topic) {
              return errResult("topic is required for thread-create");
            }
            const opts: any = { topic: params.topic };
            if (params.tags) opts.tags = params.tags;
            if (params.participants) opts.participants = params.participants;
            if (params.context) opts.context = params.context;
            result = await client.createThread(opts);
            break;
          }

          case "thread-update": {
            if (!params.thread_id) {
              return errResult("thread_id is required for thread-update");
            }
            const updates: any = {};
            if (params.status) updates.status = params.status;
            if (params.topic) updates.topic = params.topic;
            if (params.close_reason) updates.close_reason = params.close_reason;
            if (params.context) updates.context = params.context;
            if (Object.keys(updates).length === 0) {
              return errResult(
                "At least one update field is required (status, topic, close_reason, context)",
              );
            }
            result = await client.updateThread(params.thread_id, updates);
            break;
          }

          case "thread-join": {
            if (!params.thread_id) {
              return errResult("thread_id is required for thread-join");
            }
            result = await client.joinThread(params.thread_id);
            break;
          }

          case "thread-leave": {
            if (!params.thread_id) {
              return errResult("thread_id is required for thread-leave");
            }
            await client.leave(params.thread_id);
            result = { ok: true };
            break;
          }

          case "thread-invite": {
            if (!params.thread_id || !params.bot_id) {
              return errResult(
                "thread_id and bot_id are required for thread-invite",
              );
            }
            result = await client.invite(
              params.thread_id,
              params.bot_id,
              params.label || undefined,
            );
            break;
          }

          // ─── Artifacts ──────────────────────────────────────
          case "artifact-add": {
            if (!params.thread_id || !params.artifact_key || !params.artifact_type) {
              return errResult(
                "thread_id, artifact_key, and artifact_type are required for artifact-add",
              );
            }
            const artifact: any = { type: params.artifact_type };
            if (params.title) artifact.title = params.title;
            if (params.body) artifact.content = params.body;
            if (params.url) artifact.url = params.url;
            if (params.language) artifact.language = params.language;
            result = await client.addArtifact(
              params.thread_id,
              params.artifact_key,
              artifact,
            );
            break;
          }

          case "artifact-update": {
            if (!params.thread_id || !params.artifact_key) {
              return errResult(
                "thread_id and artifact_key are required for artifact-update",
              );
            }
            const updates: any = {};
            if (params.body) updates.content = params.body;
            if (params.title) updates.title = params.title;
            if (Object.keys(updates).length === 0) {
              return errResult("At least body or title is required for artifact-update");
            }
            result = await client.updateArtifact(
              params.thread_id,
              params.artifact_key,
              updates,
            );
            break;
          }

          case "artifact-list": {
            if (!params.thread_id) {
              return errResult("thread_id is required for artifact-list");
            }
            result = await client.listArtifacts(params.thread_id);
            break;
          }

          case "artifact-versions": {
            if (!params.thread_id || !params.artifact_key) {
              return errResult(
                "thread_id and artifact_key are required for artifact-versions",
              );
            }
            result = await client.getArtifactVersions(
              params.thread_id,
              params.artifact_key,
            );
            break;
          }

          // ─── Profile ────────────────────────────────────────
          case "profile-update": {
            const fields: any = {};
            if (params.bio) fields.bio = params.bio;
            if (params.role_text) fields.role = params.role_text;
            if (params.team) fields.team = params.team;
            if (params.status_text) fields.status_text = params.status_text;
            if (params.timezone) fields.timezone = params.timezone;
            if (Object.keys(fields).length === 0) {
              return errResult(
                "At least one field is required (bio, role_text, team, status_text, timezone)",
              );
            }
            result = await client.updateProfile(fields);
            break;
          }

          case "rename": {
            if (!params.new_name) {
              return errResult("new_name is required for rename");
            }
            result = await client.rename(params.new_name);
            break;
          }

          // ─── Admin ──────────────────────────────────────────
          case "role": {
            if (!params.bot_id || !params.bot_role) {
              return errResult(
                "bot_id and bot_role (admin|member) are required for role",
              );
            }
            result = await client.setBotRole(params.bot_id, params.bot_role);
            break;
          }

          case "ticket-create": {
            const opts: any = {};
            if (params.reusable) opts.reusable = true;
            if (params.expires_in) opts.expires_in = params.expires_in;
            result = await client.createOrgTicket(opts);
            break;
          }

          case "rotate-secret": {
            result = await client.rotateOrgSecret();
            break;
          }

          case "show-thread-mode": {
            if (!params.thread_id) {
              return errResult("thread_id is required for show-thread-mode");
            }
            const cfg = await getRuntime().config.loadConfig();
            result = {
              accountId: params.account || "default",
              threadId: params.thread_id,
              mode: resolveThreadMode(cfg, params.account, params.thread_id),
            };
            break;
          }

          case "set-thread-mode": {
            if (!params.thread_id || !params.thread_mode) {
              return errResult("thread_id and thread_mode are required for set-thread-mode");
            }
            const runtime = getRuntime();
            const cfg = await runtime.config.loadConfig();
            result = await setThreadModeInConfig(
              runtime,
              cfg,
              params.account,
              params.thread_id,
              params.thread_mode,
            );
            break;
          }

          default:
            return errResult(`Unknown command: ${params.command}`);
        }

        return {
          content: [
            { type: "text", text: JSON.stringify(result, null, 2) },
          ],
        };
      } catch (err: any) {
        const errObj: any = { error: err.message || String(err) };
        if (err.status) errObj.status = err.status;
        return {
          content: [{ type: "text", text: JSON.stringify(errObj, null, 2) }],
        };
      }
    },
  });

  api.logger.info("hxa-connect: registered agent tool 'hxa_connect'");
}

/** Helper to return a validation error from the tool. */
function errResult(msg: string) {
  return {
    content: [{ type: "text", text: JSON.stringify({ error: msg }) }],
  };
}

// ─── Plugin entry ────────────────────────────────────────────
const plugin = {
  id: "hxa-connect",
  name: "HXA-Connect",
  description: "Agent-to-agent messaging via HXA-Connect (WebSocket + webhook)",
  configSchema: emptyPluginConfigSchema(),
  register(api: OpenClawPluginApi) {
    pluginRuntime = api.runtime;

    void (async () => {
      try {
        const cfg = await api.runtime.config.loadConfig();
        const { next, changed } = migrateRootConfig(cfg);
        if (changed) {
          await api.runtime.config.writeConfigFile(next);
          api.logger.info("hxa-connect: persisted config migration for per-thread mode");
        }
      } catch (err: any) {
        api.logger.error(
          `hxa-connect: failed to persist config migration: ${err?.message || String(err)}`,
        );
      }
    })();

    // Register the channel
    api.registerChannel({ plugin: hxaConnectChannel });

    // Register agent tools
    registerTools(api);

    // Register HTTP routes for inbound webhooks (per-account)
    const hxa = resolveHxaConnectConfig(api.config);
    const accounts = resolveAccounts(hxa);
    const registeredPaths = new Set<string>();

    for (const [id, acct] of Object.entries(accounts)) {
      const webhookPath = acct.webhookPath ?? "/hxa-connect/inbound";
      if (!registeredPaths.has(webhookPath)) {
        api.registerHttpRoute({
          path: webhookPath,
          handler: handleInboundWebhook,
        });
        registeredPaths.add(webhookPath);
        api.logger.info(`hxa-connect: registered webhook route: ${webhookPath} (account: ${id})`);
      }
    }

    api.logger.info(
      `hxa-connect: plugin loaded (${Object.keys(accounts).length} account(s), WebSocket + webhook + agent tools)`,
    );
  },
};

export default plugin;
