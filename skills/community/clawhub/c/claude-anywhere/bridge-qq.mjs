#!/usr/bin/env node
/**
 * bridge-qq.mjs — Claude Anywhere QQ Bot Bridge (thin shell)
 *
 * Uses QQ Bot official WebSocket gateway (same approach as @tencent-connect/openclaw-qqbot).
 * All business logic lives in core.mjs.
 *
 * QQ Bot limitations:
 *   - Cannot proactively push messages (only reply within interaction window)
 *   - /cron creation warns user about no push support
 *
 * WebSocket flow:
 *   1. Get access token via POST https://bots.qq.com/app/getAppAccessToken
 *   2. Get gateway URL via GET https://api.sgroup.qq.com/gateway
 *   3. Connect WebSocket, receive Hello (op=10), send Identify (op=2)
 *   4. Receive events (op=0), heartbeat (op=1), resume on disconnect
 */

import WebSocket from "ws";
import { randomUUID } from "crypto";
import {
  writeFileSync, readFileSync, existsSync, mkdirSync, unlinkSync,
} from "fs";
import { join } from "path";
import { homedir } from "os";
import { ClaudeAnywhere } from "./core.mjs";

// Load .env if present
try {
  const envPath = new URL(".env", import.meta.url).pathname;
  if (existsSync(envPath)) {
    for (const line of readFileSync(envPath, "utf-8").split("\n")) {
      const t = line.trim();
      if (!t || t.startsWith("#")) continue;
      const eq = t.indexOf("=");
      if (eq < 1) continue;
      const k = t.slice(0, eq).trim();
      const v = t.slice(eq + 1).trim();
      if (k && !(k in process.env)) process.env[k] = v;
    }
  }
} catch {}

// ============ Config ============
const QQ_APP_ID     = process.env.QQ_APP_ID;
const QQ_APP_SECRET = process.env.QQ_APP_SECRET;

if (!QQ_APP_ID || !QQ_APP_SECRET) {
  console.error("ERROR: QQ_APP_ID and QQ_APP_SECRET must be set in .env");
  process.exit(1);
}

const API_BASE  = "https://api.sgroup.qq.com";
const TOKEN_URL = "https://bots.qq.com/app/getAppAccessToken";
const TMP_DIR   = "/tmp/claude-anywhere-qq";
mkdirSync(TMP_DIR, { recursive: true });

// Intents (from QQ Bot official docs)
const INTENTS = {
  PUBLIC_GUILD_MESSAGES: 1 << 30,
  DIRECT_MESSAGE: 1 << 12,
  GROUP_AND_C2C: 1 << 25,
};
const FULL_INTENTS = INTENTS.PUBLIC_GUILD_MESSAGES | INTENTS.DIRECT_MESSAGE | INTENTS.GROUP_AND_C2C;

// Reconnect config
const RECONNECT_DELAYS = [1000, 2000, 5000, 10000, 30000, 60000];
const MAX_RECONNECT_ATTEMPTS = 100;

// ============ Core instance ============
const core = new ClaudeAnywhere({ platform: "qq" });

// QQ Bot proactive messaging was disabled by Tencent since 2025-04-21.
// Cron results cannot be delivered. Log only.
core.setCronResultHandler(async (jobId, jobName, userId, result) => {
  core.logger.warn(`[QQ] Cron job "${jobName}" executed but result cannot be pushed (QQ proactive messaging disabled by Tencent). Use Telegram or WeChat Work for cron.`);
});

// ============ Token management ============
let _accessToken = null;
let _tokenExpiry  = 0;

async function getAccessToken() {
  if (_accessToken && Date.now() < _tokenExpiry - 60_000) return _accessToken;

  try {
    const res = await fetch(TOKEN_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ appId: QQ_APP_ID, clientSecret: QQ_APP_SECRET }),
      signal: AbortSignal.timeout(10_000),
    });
    const data = await res.json();
    if (data.access_token) {
      _accessToken = data.access_token;
      _tokenExpiry = Date.now() + (parseInt(data.expires_in, 10) || 7200) * 1000;
      core.logger.info("QQ access token refreshed");
      return _accessToken;
    }
    core.logger.error("Failed to get QQ access token:", JSON.stringify(data));
    return null;
  } catch (e) {
    core.logger.error("QQ token request failed:", e.message);
    return null;
  }
}

// ============ API helpers ============

async function qqApi(method, path, body) {
  const token = await getAccessToken();
  if (!token) return null;

  try {
    const res = await fetch(`${API_BASE}${path}`, {
      method,
      headers: {
        "Authorization": `QQBot ${token}`,
        "Content-Type": "application/json",
      },
      body: body ? JSON.stringify(body) : undefined,
      signal: AbortSignal.timeout(15_000),
    });
    if (!res.ok) {
      const text = await res.text();
      core.logger.error(`QQ API ${method} ${path} ${res.status}: ${text.slice(0, 200)}`);
      return null;
    }
    return await res.json();
  } catch (e) {
    core.logger.error(`QQ API error: ${e.message}`);
    return null;
  }
}

// Track msg_seq per msgId to handle multi-chunk replies
const msgSeqMap = new Map();
function getNextMsgSeq(msgId) {
  const seq = (msgSeqMap.get(msgId) || 0) + 1;
  msgSeqMap.set(msgId, seq);
  // Cleanup old entries
  if (msgSeqMap.size > 1000) {
    const keys = [...msgSeqMap.keys()];
    for (let i = 0; i < keys.length - 500; i++) msgSeqMap.delete(keys[i]);
  }
  return seq;
}

async function replyC2C(openid, msgId, content) {
  const chunks = core.splitText(content);
  for (const chunk of chunks) {
    const msgSeq = getNextMsgSeq(msgId);
    await qqApi("POST", `/v2/users/${openid}/messages`, {
      content: chunk,
      msg_type: 0,
      msg_id: msgId,
      msg_seq: msgSeq,
    });
  }
}

async function replyGroup(groupOpenid, msgId, content) {
  const chunks = core.splitText(content);
  for (const chunk of chunks) {
    const msgSeq = getNextMsgSeq(msgId);
    await qqApi("POST", `/v2/groups/${groupOpenid}/messages`, {
      content: chunk,
      msg_type: 0,
      msg_id: msgId,
      msg_seq: msgSeq,
    });
  }
}

// ============ Message handling ============

async function handleMessage(userId, text, replyFn) {
  if (!text?.trim()) return;
  text = text.trim();

  const msgId = `qq_${userId}_${Date.now()}`;
  if (core.isProcessing(msgId)) return;

  core.logger.info(`Text: [${userId}] ${text.slice(0, 100)}`);

  try {
    // Check for pending cron confirmation
    if (core.hasPendingCron(userId)) {
      const cronResult = core.handleCronConfirmation(userId, text);
      if (cronResult.handled) {
        if (cronResult.reply) await replyFn(cronResult.reply);
        return;
      }
    }

    const pro = await core.isProMode();
    const command = core.parseCommand(text);

    if (command) {
      const result = await core.handleCommand(userId, command, pro);
      for (const reply of result.replies) {
        await replyFn(reply);
      }
      return;
    }

    // Free tier quota check
    if (!pro) {
      const quota = core.checkQuota(userId);
      if (!quota.allowed) {
        const msg = quota.reason === "trial_expired" ? core.T.trialExpired : core.T.limitMsg;
        await replyFn(msg);
        return;
      }
    }

    // Call Claude
    await replyFn("🤔 正在思考...");
    const sessionId = pro ? core.getSessionId(userId) : null;
    const result = await core.runClaude(text, sessionId);

    if (pro && result.sessionId) {
      core.updateSession(userId, result.sessionId, text.slice(0, 30));
    }

    if (!result.text) {
      await replyFn("Claude 没有返回结果，请重试。");
      return;
    }

    const finalText = pro ? result.text : result.text + core.T.upgradeAd;
    await replyFn(finalText);
    core.logger.info(`Reply (${pro ? "pro" : "free"}): ${result.text.length} chars`);

  } catch (err) {
    core.logger.error("Message error:", err.message);
    if (String(err).includes("session") || String(err).includes("resume")) {
      core.deleteSession(userId);
    }
    await replyFn("处理出错: " + err.message);
  } finally {
    core.doneProcessing(msgId);
  }
}

// ============ Attachment handling (images, files) ============

async function handleAttachments(userId, msgId, caption, attachments, replyFn) {
  const pro = await core.isProMode();
  if (!pro) {
    await replyFn(core.T.imgProOnly);
    return;
  }

  for (const att of attachments) {
    const contentType = att.content_type || "";
    const isImage = contentType.startsWith("image/");
    const url = att.url?.startsWith("http") ? att.url : `https://${att.url}`;
    const ext = att.filename?.split(".").pop() || (isImage ? "jpg" : "bin");
    const localPath = join(TMP_DIR, `${randomUUID()}.${ext}`);

    try {
      // Download attachment
      const res = await fetch(url, { signal: AbortSignal.timeout(30_000) });
      if (!res.ok) { core.logger.error(`Failed to download attachment: ${res.status}`); continue; }
      const buf = Buffer.from(await res.arrayBuffer());
      writeFileSync(localPath, buf);
      core.logger.info(`Attachment saved: [${userId}] ${att.filename || "unknown"} -> ${localPath}`);

      let message;
      if (isImage) {
        await replyFn("🤔 正在分析图片...");
        message = `图片文件: ${localPath}\n\n${caption || "请描述这张图片"}\n\n（请用 Read 工具读取上述图片文件来查看图片内容）`;
      } else {
        const fileName = att.filename || "unknown";
        if (ClaudeAnywhere.UNSUPPORTED_EXTS.includes(ext.toLowerCase())) {
          await replyFn(`❌ 不支持分析 .${ext} 文件。`);
          try { unlinkSync(localPath); } catch {}
          continue;
        }
        await replyFn(`📄 正在分析文件: ${fileName}...`);
        message = `文件已保存到: ${localPath}\n文件名: ${fileName}\n\n${caption || "请分析这个文件"}\n\n（请用 Read 工具读取该文件来分析内容）`;
      }

      const sessionId = core.getSessionId(userId);
      const result = await core.runClaude(message, sessionId);
      if (result.sessionId) core.updateSession(userId, result.sessionId, att.filename || "📎");
      setTimeout(() => { try { unlinkSync(localPath); } catch {} }, 120_000);

      if (result.text) await replyFn(result.text);
      else await replyFn("Claude 没有返回结果，请重试。");
      core.logger.info(`Attachment reply (pro): ${(result.text || "").length} chars`);
    } catch (err) {
      core.logger.error("Attachment error:", err.message);
      await replyFn("处理出错: " + err.message);
    }
  }
}

// ============ WebSocket Gateway ============

async function startGateway() {
  const accessToken = await getAccessToken();
  if (!accessToken) {
    core.logger.error("Cannot start: failed to get access token");
    process.exit(1);
  }

  // Get gateway URL
  const gatewayData = await qqApi("GET", "/gateway");
  if (!gatewayData?.url) {
    core.logger.error("Cannot get gateway URL");
    process.exit(1);
  }

  let sessionId = null;
  let lastSeq = null;
  let heartbeatTimer = null;
  let reconnectAttempts = 0;
  let ws = null;

  function connect() {
    core.logger.info(`Connecting to QQ gateway: ${gatewayData.url}`);
    ws = new WebSocket(gatewayData.url);

    ws.on("open", () => {
      core.logger.info("WebSocket connected");
      reconnectAttempts = 0;
    });

    ws.on("message", async (raw) => {
      let payload;
      try {
        payload = JSON.parse(raw.toString());
      } catch { return; }

      const { op, t, d, s } = payload;
      if (s) lastSeq = s;

      switch (op) {
        case 10: // Hello — send Identify or Resume
          if (sessionId && lastSeq !== null) {
            core.logger.info(`Resuming session ${sessionId}`);
            ws.send(JSON.stringify({
              op: 6,
              d: { token: `QQBot ${_accessToken}`, session_id: sessionId, seq: lastSeq },
            }));
          } else {
            core.logger.info(`Sending Identify with intents: ${FULL_INTENTS}`);
            ws.send(JSON.stringify({
              op: 2,
              d: { token: `QQBot ${_accessToken}`, intents: FULL_INTENTS, shard: [0, 1] },
            }));
          }

          // Start heartbeat
          const interval = d?.heartbeat_interval || 30000;
          if (heartbeatTimer) clearInterval(heartbeatTimer);
          heartbeatTimer = setInterval(() => {
            if (ws?.readyState === WebSocket.OPEN) {
              ws.send(JSON.stringify({ op: 1, d: lastSeq }));
            }
          }, interval);
          break;

        case 0: // Dispatch — events
          if (t === "READY") {
            sessionId = d?.session_id;
            core.logger.info(`Ready! Session: ${sessionId}`);
          } else if (t === "RESUMED") {
            core.logger.info("Session resumed");
          } else if (t === "C2C_MESSAGE_CREATE") {
            // Private chat message (text + attachments)
            const openid = d?.author?.user_openid;
            const msgId = d?.id;
            const content = d?.content?.trim() || "";
            const attachments = d?.attachments || [];
            const replyFn = (text) => replyC2C(openid, msgId, text);

            if (attachments.length > 0 && openid) {
              handleAttachments(openid, msgId, content, attachments, replyFn);
            } else if (openid && content) {
              handleMessage(openid, content, replyFn);
            }
          } else if (t === "GROUP_AT_MESSAGE_CREATE") {
            // Group @bot message (text + attachments)
            const groupOpenid = d?.group_openid;
            const msgId = d?.id;
            let content = d?.content?.trim() || "";
            if (content) content = content.replace(/^<@!\d+>\s*/, "").trim();
            const attachments = d?.attachments || [];
            const userId = d?.author?.member_openid || groupOpenid;
            const replyFn = (text) => replyGroup(groupOpenid, msgId, text);

            if (attachments.length > 0 && groupOpenid) {
              handleAttachments(userId, msgId, content, attachments, replyFn);
            } else if (groupOpenid && content) {
              handleMessage(userId, content, replyFn);
            }
          }
          break;

        case 9: // Invalid session
          core.logger.warn("Invalid session, reconnecting with new Identify");
          sessionId = null;
          lastSeq = null;
          ws.close();
          break;

        case 11: // Heartbeat ACK
          break;

        default:
          core.logger.info(`Unknown op: ${op}`);
      }
    });

    ws.on("close", (code, reason) => {
      core.logger.warn(`WebSocket closed: ${code} ${reason}`);
      if (heartbeatTimer) { clearInterval(heartbeatTimer); heartbeatTimer = null; }
      scheduleReconnect();
    });

    ws.on("error", (err) => {
      core.logger.error(`WebSocket error: ${err.message}`);
    });
  }

  function scheduleReconnect() {
    if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
      core.logger.error("Max reconnect attempts reached, exiting");
      process.exit(1);
    }
    const delay = RECONNECT_DELAYS[Math.min(reconnectAttempts, RECONNECT_DELAYS.length - 1)];
    reconnectAttempts++;
    core.logger.info(`Reconnecting in ${delay}ms (attempt ${reconnectAttempts})`);

    setTimeout(async () => {
      // Refresh token before reconnect
      await getAccessToken();
      connect();
    }, delay);
  }

  connect();
}

// ============ Start ============

core.logger.info("Claude Anywhere v2 (QQ Bot) starting...");
startGateway();

process.on("SIGINT",  () => process.exit(0));
process.on("SIGTERM", () => process.exit(0));

core.logger.info("Bot started. Waiting for messages...");
