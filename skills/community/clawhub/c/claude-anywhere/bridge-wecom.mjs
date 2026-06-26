#!/usr/bin/env node
/**
 * bridge-wecom.mjs — Claude Anywhere WeChat Work Bridge (thin shell)
 *
 * All business logic lives in core.mjs.
 * This file handles WeCom-specific I/O and the 6-min stream timeout.
 */

import { WSClient } from "@wecom/aibot-node-sdk";
import { randomUUID } from "crypto";
import {
  writeFileSync, readFileSync, existsSync, mkdirSync, unlinkSync,
} from "fs";
import { join } from "path";
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
const BOT_ID = process.env.WECOM_BOT_ID;
const SECRET = process.env.WECOM_SECRET;

if (!BOT_ID || !SECRET) {
  console.error("ERROR: WECOM_BOT_ID and WECOM_SECRET must be set in .env");
  process.exit(1);
}

const STREAM_TIMEOUT_MS = 5 * 60 * 1000; // 5 min — WeCom limit is 6 min
const TMP_DIR = "/tmp/claude-anywhere-wecom";
mkdirSync(TMP_DIR, { recursive: true });

// ============ Core instance ============
const core = new ClaudeAnywhere({ platform: "wecom" });

// Store wsClient ref and last frame per user (for cron result delivery)
let _wsClient = null;
const lastFrameByUser = new Map();

// ============ Cron result delivery ============
core.setCronResultHandler(async (jobId, jobName, userId, result) => {
  if (!_wsClient) { core.logger.warn("wsClient not ready, cannot deliver cron result"); return; }
  const frame = lastFrameByUser.get(userId);
  if (!frame) { core.logger.warn(`No frame for userId ${userId}, cannot deliver cron result`); return; }

  const header = `⏰ 定时任务"${jobName}"已执行：\n\n`;
  const fullText = header + result;
  const chunks = core.splitText(fullText);
  const sid0 = `stream_${Date.now()}_${randomUUID().slice(0, 8)}`;

  if (chunks.length === 1) {
    try { await safeReplyStream(_wsClient, frame, sid0, chunks[0], true); } catch (e) {
      core.logger.error(`Failed to deliver cron result to ${userId}:`, e.message);
    }
  } else {
    for (let i = 0; i < chunks.length; i++) {
      const sid = i === 0 ? sid0 : `stream_${Date.now()}_${randomUUID().slice(0, 8)}`;
      const isLast = i === chunks.length - 1;
      try { await safeReplyStream(_wsClient, frame, sid, chunks[i], isLast); } catch (e) {
        core.logger.error(`Chunk ${i} delivery error:`, e.message);
      }
    }
  }
});

// ============ WeCom-specific helpers ============

async function safeReplyStream(wsClient, frame, streamId, content, isFinish) {
  try {
    await wsClient.replyStream(frame, streamId, content, isFinish);
    return true;
  } catch (err) {
    if (err?.errcode === 846608 || String(err).includes("846608")) {
      core.logger.warn(`Stream expired: ${streamId}`);
      return false;
    }
    throw err;
  }
}

async function sendResult(wsClient, frame, streamId, streamExpired, text) {
  const chunks = core.splitText(text);
  const sid = streamExpired
    ? `stream_${Date.now()}_${randomUUID().slice(0, 8)}`
    : streamId;

  if (streamExpired) core.logger.info(`Using new stream: ${sid}`);

  if (chunks.length === 1) {
    await safeReplyStream(wsClient, frame, sid, chunks[0], true);
  } else {
    for (let i = 0; i < chunks.length; i++) {
      const isLast = i === chunks.length - 1;
      const prefix = !isLast ? `[${i + 1}/${chunks.length}]\n` : "";
      await safeReplyStream(wsClient, frame, sid, prefix + chunks[i], isLast);
    }
  }
}

function newStreamId() {
  return `stream_${Date.now()}_${randomUUID().slice(0, 8)}`;
}

// ============ Claude call with 6-min stream timeout ============

async function handleClaudeCall(wsClient, frame, senderId, message, label, pro) {
  const streamId = newStreamId();

  try {
    await wsClient.replyStream(frame, streamId, "<think>正在思考...</think>", false);

    const currentSessionId = pro ? core.getSessionId(senderId) : null;
    let streamExpired = false;

    const streamTimer = setTimeout(async () => {
      streamExpired = true;
      core.logger.warn("Stream timeout approaching, closing current stream");
      await safeReplyStream(wsClient, frame, streamId, "⏳ 处理时间较长，完成后将发送新消息...", true);
    }, STREAM_TIMEOUT_MS);

    const result = await core.runClaude(message, currentSessionId);
    clearTimeout(streamTimer);

    if (pro) core.updateSession(senderId, result.sessionId, label);

    if (!result.text) {
      if (!streamExpired) await safeReplyStream(wsClient, frame, streamId, "Claude 没有返回结果，请重试。", true);
      return;
    }

    const finalText = pro ? result.text : result.text + core.T.upgradeAd;
    await sendResult(wsClient, frame, streamId, streamExpired, finalText);
    core.logger.info(`Reply (${pro ? "pro" : "free"}): ${result.text.length} chars`);

  } catch (err) {
    core.logger.error(`Error: ${err?.message || err}`);
    if (String(err).includes("session") || String(err).includes("resume")) {
      core.deleteSession(senderId);
    }
    try {
      await safeReplyStream(wsClient, frame, newStreamId(), `处理出错: ${err?.message || err}`, true);
    } catch {}
  }
}

// ============ Command handler ============

async function handleCommandReply(wsClient, frame, userId, command, pro) {
  const result = await core.handleCommand(userId, command, pro);
  const streamId = newStreamId();
  for (let i = 0; i < result.replies.length; i++) {
    const isLast = i === result.replies.length - 1;
    const sid = i === 0 ? streamId : newStreamId();
    await wsClient.replyStream(frame, sid, result.replies[i], isLast);
  }
}

// ============ Text message handler ============

async function handleTextMessage(wsClient, frame) {
  const msgId    = frame.body?.msgid;
  const senderId = frame.body?.from?.userid || "default";
  const text     = frame.body?.text?.content?.trim();

  if (!text || !msgId) return;
  if (core.isProcessing(msgId)) return;

  lastFrameByUser.set(senderId, frame);
  core.logger.info(`Text: [${senderId}] ${text.slice(0, 100)}`);

  try {
    // Check for pending cron confirmation
    if (core.hasPendingCron(senderId)) {
      const cronResult = core.handleCronConfirmation(senderId, text);
      if (cronResult.handled) {
        if (cronResult.reply) {
          await wsClient.replyStream(frame, newStreamId(), cronResult.reply, true);
        }
        return;
      }
    }

    const pro = await core.isProMode();
    const command = core.parseCommand(text);
    if (command) {
      await handleCommandReply(wsClient, frame, senderId, command, pro);
      return;
    }

    if (!pro) {
      const quota = core.checkQuota(senderId);
      if (!quota.allowed) {
        const { getMachineId } = await import('./license-client.mjs');
        const buyUrl = `https://claudeanywhere.com/buy.html?mid=${getMachineId()}`;
        const msg = quota.reason === "trial_expired"
          ? `⚠️ 免费试用已到期（7天）。\n\n🛒 升级 Pro，扫码付款后自动开通：\n${buyUrl}\n\n• 月付 ¥39.99 | 年付 ¥399.9（省2个月）`
          : `⚠️ 今日免费次数已用完（5/5）。\n\n🛒 升级 Pro 无限使用，扫码付款后自动开通：\n${buyUrl}\n\n• 月付 ¥39.99 | 年付 ¥399.9（省2个月）`;
        await wsClient.replyStream(frame, newStreamId(), msg, true);
        return;
      }
    }

    await handleClaudeCall(wsClient, frame, senderId, text, text.slice(0, 30), pro);
  } finally {
    core.doneProcessing(msgId);
  }
}

// ============ Image handler ============

async function handleImageMessage(wsClient, frame) {
  const msgId    = frame.body?.msgid;
  const senderId = frame.body?.from?.userid || "default";
  const image    = frame.body?.image;

  if (!image?.url || !msgId) return;
  if (core.isProcessing(msgId)) return;

  core.logger.info(`Image: [${senderId}]`);

  try {
    const pro = await core.isProMode();
    if (!pro) {
      await wsClient.replyStream(frame, newStreamId(), core.T.imgProOnly, true);
      return;
    }

    const { buffer, filename } = await wsClient.downloadFile(image.url, image.aeskey);
    const ext = (filename || "image.jpg").split(".").pop() || "jpg";
    const localPath = join(TMP_DIR, `${randomUUID()}.${ext}`);
    writeFileSync(localPath, buffer);
    core.logger.info(`Image saved: ${localPath}`);

    const message = `图片文件: ${localPath}\n\n请描述这张图片\n\n（请用 Read 工具读取上述图片文件来查看图片内容）`;
    await handleClaudeCall(wsClient, frame, senderId, message, "📷 图片", pro);
    setTimeout(() => { try { unlinkSync(localPath); } catch {} }, 60_000);

  } catch (err) {
    core.logger.error("Image error:", err?.message || err);
    try { await safeReplyStream(wsClient, frame, newStreamId(), `图片处理出错: ${err?.message || err}`, true); } catch {}
  } finally {
    core.doneProcessing(msgId);
  }
}

// ============ File handler ============

async function handleFileMessage(wsClient, frame) {
  const msgId    = frame.body?.msgid;
  const senderId = frame.body?.from?.userid || "default";
  const file     = frame.body?.file;

  if (!file?.url || !msgId) return;
  if (core.isProcessing(msgId)) return;

  const fileName = file.filename || "unknown";
  core.logger.info(`File: [${senderId}] ${fileName}`);

  try {
    const pro = await core.isProMode();
    if (!pro) {
      await wsClient.replyStream(frame, newStreamId(), core.T.fileProOnly, true);
      return;
    }

    const { buffer, filename } = await wsClient.downloadFile(file.url, file.aeskey);
    const actualName = filename || fileName;
    const localPath  = join(TMP_DIR, `${randomUUID()}_${actualName}`);
    writeFileSync(localPath, buffer);
    core.logger.info(`File saved: ${localPath}`);

    const ext = actualName.split(".").pop()?.toLowerCase() || "";

    if (ClaudeAnywhere.UNSUPPORTED_EXTS.includes(ext)) {
      await wsClient.replyStream(frame, newStreamId(), `❌ 不支持分析 .${ext} 文件。\n\n支持: 图片/PDF/TXT/CSV/Excel/代码文件等`, true);
      try { unlinkSync(localPath); } catch {}
      return;
    }

    const message = ClaudeAnywhere.IMAGE_EXTS.includes(ext)
      ? `图片文件: ${localPath}\n\n请描述这张图片\n\n（请用 Read 工具读取上述图片文件来查看图片内容）`
      : `文件已保存到: ${localPath}\n文件名: ${actualName}\n\n请分析这个文件\n\n（请用 Read 工具读取该文件来分析内容）`;

    await handleClaudeCall(wsClient, frame, senderId, message, `📄 ${actualName}`, pro);
    setTimeout(() => { try { unlinkSync(localPath); } catch {} }, 120_000);

  } catch (err) {
    core.logger.error("File error:", err?.message || err);
    try { await safeReplyStream(wsClient, frame, newStreamId(), `文件处理出错: ${err?.message || err}`, true); } catch {}
  } finally {
    core.doneProcessing(msgId);
  }
}

// ============ Start ============

async function start() {
  const pro = await core.isProMode();
  core.logger.info(`Claude Anywhere v2 (WeChat Work) — ${pro ? "Pro" : "Free"} mode`);

  const wsClient = new WSClient({
    botId:                BOT_ID,
    secret:               SECRET,
    logger:               { info: () => {}, warn: core.logger.warn, error: core.logger.error, debug: () => {} },
    heartbeatInterval:    30_000,
    maxReconnectAttempts: -1,
    reconnectInterval:    3000,
    requestTimeout:       15_000,
  });

  wsClient.on("connected",     () => core.logger.info("WebSocket connected"));
  wsClient.on("authenticated", () => core.logger.info("Authenticated, waiting for messages..."));
  wsClient.on("disconnected",  reason => core.logger.warn("Disconnected:", reason));
  wsClient.on("error",         err    => core.logger.error("WebSocket error:", err?.message || err));

  wsClient.on("message.text",  frame => handleTextMessage(wsClient, frame).catch(e  => core.logger.error("Text handler:", e?.message)));
  wsClient.on("message.image", frame => handleImageMessage(wsClient, frame).catch(e => core.logger.error("Image handler:", e?.message)));
  wsClient.on("message.file",  frame => handleFileMessage(wsClient, frame).catch(e  => core.logger.error("File handler:", e?.message)));

  wsClient.on("event.enter_chat", async frame => {
    try {
      const welcome = pro
        ? "Claude Anywhere Pro 已就绪。\n/new 新对话 | /sessions 历史 | /help 帮助"
        : "Claude Anywhere 已就绪（免费版）。\n发文字即可对话。/status 查看用量 | /help 帮助";
      await wsClient.replyWelcome(frame, { msgtype: "text", text: { content: welcome } });
    } catch (e) {
      core.logger.warn("Welcome message failed:", e?.message);
    }
  });

  _wsClient = wsClient;
  wsClient.connect();

  process.on("SIGINT",  () => { wsClient.disconnect(); process.exit(0); });
  process.on("SIGTERM", () => { wsClient.disconnect(); process.exit(0); });
}

start();
