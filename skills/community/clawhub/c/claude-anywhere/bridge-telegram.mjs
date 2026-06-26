#!/usr/bin/env node
/**
 * bridge-telegram.mjs — Claude Anywhere Telegram Bridge (thin shell)
 *
 * All business logic lives in core.mjs.
 * This file only handles Telegram-specific I/O.
 */

import TelegramBot from "node-telegram-bot-api";
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
const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
if (!BOT_TOKEN) {
  console.error("ERROR: TELEGRAM_BOT_TOKEN is not set. Copy .env.example to .env and fill in the token.");
  process.exit(1);
}

const TMP_DIR = "/tmp/claude-anywhere-telegram";
mkdirSync(TMP_DIR, { recursive: true });

// ============ Core instance ============
const core = new ClaudeAnywhere({ platform: "telegram" });

// ============ Cron result delivery ============
core.setCronResultHandler(async (jobId, jobName, userId, result) => {
  const chatId = core.getChatId(userId);
  if (!chatId) { core.logger.warn(`No chatId for userId ${userId}, cannot deliver cron result`); return; }
  const header = `⏰ Scheduled job "${jobName}" completed:\n\n`;
  const fullText = header + result;
  for (const chunk of core.splitText(fullText)) {
    try { await bot.sendMessage(chatId, chunk); } catch (e) {
      core.logger.error(`Failed to deliver cron result to ${userId}:`, e.message);
    }
  }
});

// ============ Bot ============
const bot = new TelegramBot(BOT_TOKEN, { polling: true });

core.logger.info("Claude Anywhere v2 (Telegram) starting...");

// Helper: send multiple replies
async function sendReplies(chatId, { replies, parseMode }) {
  for (const text of replies) {
    const opts = parseMode ? { parse_mode: parseMode } : {};
    await bot.sendMessage(chatId, text, opts);
  }
}

// ============ Command handlers ============

bot.onText(/^\/(new|reset)$/, async msg => {
  const pro = await core.isProMode();
  const result = await core.handleCommand(String(msg.from.id), { cmd: "new" }, pro);
  await sendReplies(msg.chat.id, result);
});

bot.onText(/^\/status$/, async msg => {
  const pro = await core.isProMode();
  const result = await core.handleCommand(String(msg.from.id), { cmd: "status" }, pro);
  await sendReplies(msg.chat.id, result);
});

bot.onText(/^\/sessions$/, async msg => {
  const pro = await core.isProMode();
  const result = await core.handleCommand(String(msg.from.id), { cmd: "sessions" }, pro);
  await sendReplies(msg.chat.id, result);
});

bot.onText(/^\/resume$/, async msg => {
  const pro = await core.isProMode();
  const result = await core.handleCommand(String(msg.from.id), { cmd: "resume_help" }, pro);
  await sendReplies(msg.chat.id, result);
});

bot.onText(/^\/resume\s+(.+)$/, async (msg, match) => {
  const pro = await core.isProMode();
  const result = await core.handleCommand(String(msg.from.id), { cmd: "resume", id: match[1].trim() }, pro);
  await sendReplies(msg.chat.id, result);
});

bot.onText(/^\/activate(?:\s+(.+))?$/, async (msg, match) => {
  const pro = await core.isProMode();
  const result = await core.handleCommand(String(msg.from.id), { cmd: "activate", key: match?.[1]?.trim() }, pro);
  await sendReplies(msg.chat.id, result);
});

bot.onText(/^\/cron(?:\s+(.*))?$/s, async (msg, match) => {
  const chatId = msg.chat.id;
  const userId = String(msg.from.id);
  core.trackChatId(userId, chatId);

  const pro = await core.isProMode();
  const result = await core.handleCommand(userId, { cmd: "cron", args: (match?.[1] || "").trim() }, pro);
  await sendReplies(chatId, result);
});

bot.onText(/^\/start$/, async msg => {
  const pro = await core.isProMode();
  const result = await core.handleCommand(String(msg.from.id), { cmd: "help" }, pro);
  await sendReplies(msg.chat.id, result);
});

bot.onText(/^\/help$/, async msg => {
  const pro = await core.isProMode();
  const result = await core.handleCommand(String(msg.from.id), { cmd: "help" }, pro);
  await sendReplies(msg.chat.id, result);
});

// ============ Photo handler ============

bot.on("photo", async msg => {
  const chatId = msg.chat.id;
  const userId = String(msg.from.id);
  const msgId  = String(msg.message_id);

  if (core.isProcessing(msgId)) return;

  try {
    const pro = await core.isProMode();
    if (!pro) {
      await bot.sendMessage(chatId, core.T.imgProOnly);
      return;
    }

    const photo = msg.photo[msg.photo.length - 1];
    const file = await bot.getFile(photo.file_id);
    const fileUrl = `https://api.telegram.org/file/bot${BOT_TOKEN}/${file.file_path}`;
    const ext = file.file_path.split(".").pop() || "jpg";
    const localPath = join(TMP_DIR, `${randomUUID()}.${ext}`);

    const buf = Buffer.from(await (await fetch(fileUrl)).arrayBuffer());
    writeFileSync(localPath, buf);
    core.logger.info(`Photo saved: [${userId}] ${localPath}`);

    const caption = msg.caption || "请描述这张图片";
    await bot.sendMessage(chatId, "🤔 Analyzing image...");

    const result = await core.runClaude(caption, core.getSessionId(userId), [localPath]);
    if (result.sessionId) core.updateSession(userId, result.sessionId, caption.slice(0, 30));
    setTimeout(() => { try { unlinkSync(localPath); } catch {} }, 60_000);

    for (const chunk of core.splitText(result.text)) await bot.sendMessage(chatId, chunk);
  } catch (err) {
    core.logger.error("Photo error:", err.message);
    await bot.sendMessage(chatId, "Image processing error: " + err.message);
  } finally {
    core.doneProcessing(msgId);
  }
});

// ============ Document handler ============

bot.on("document", async msg => {
  const chatId = msg.chat.id;
  const userId = String(msg.from.id);
  const msgId  = String(msg.message_id);

  if (core.isProcessing(msgId)) return;

  try {
    const pro = await core.isProMode();
    if (!pro) {
      await bot.sendMessage(chatId, core.T.fileProOnly);
      return;
    }

    const doc = msg.document;
    const fileName = doc.file_name || "unknown";
    const file = await bot.getFile(doc.file_id);
    const fileUrl = `https://api.telegram.org/file/bot${BOT_TOKEN}/${file.file_path}`;
    const localPath = join(TMP_DIR, `${randomUUID()}_${fileName}`);

    const buf = Buffer.from(await (await fetch(fileUrl)).arrayBuffer());
    writeFileSync(localPath, buf);
    core.logger.info(`File saved: [${userId}] ${fileName} -> ${localPath}`);

    const caption = msg.caption || `请分析这个文件: ${fileName}`;
    const ext = fileName.split(".").pop()?.toLowerCase() || "";

    if (ClaudeAnywhere.UNSUPPORTED_EXTS.includes(ext)) {
      await bot.sendMessage(chatId,
        `❌ .${ext} files are not supported.\n\nSupported: images (jpg/png/gif/webp), PDF, txt, md, csv, json, code files, xlsx/xls/csv`
      );
      try { unlinkSync(localPath); } catch {}
      return;
    }

    const isImage = ClaudeAnywhere.IMAGE_EXTS.includes(ext);
    await bot.sendMessage(chatId, isImage ? "🤔 Analyzing image..." : `📄 Analyzing file: ${fileName}...`);

    const sessionId = core.getSessionId(userId);
    let result;
    if (isImage) {
      result = await core.runClaude(caption, sessionId, [localPath]);
    } else {
      result = await core.runClaude(
        `文件已保存到: ${localPath}\n文件名: ${fileName}\n\n${caption}\n\n（请用 Read 工具读取该文件来分析内容）`,
        sessionId
      );
    }

    if (result.sessionId) core.updateSession(userId, result.sessionId, `📄 ${fileName}`);
    setTimeout(() => { try { unlinkSync(localPath); } catch {} }, 120_000);

    for (const chunk of core.splitText(result.text)) await bot.sendMessage(chatId, chunk);
  } catch (err) {
    core.logger.error("File error:", err.message);
    await bot.sendMessage(chatId, "File processing error: " + err.message);
  } finally {
    core.doneProcessing(msgId);
  }
});

// ============ Text message handler ============

bot.on("text", async msg => {
  const chatId = msg.chat.id;
  const userId = String(msg.from.id);
  const text   = msg.text?.trim();
  const msgId  = String(msg.message_id);

  core.trackChatId(userId, chatId);

  if (!text || text.startsWith("/")) return;
  if (core.isProcessing(msgId)) return;

  core.logger.info(`Text: [${userId}] ${text.slice(0, 100)}`);

  // Check for pending cron confirmation
  if (core.hasPendingCron(userId)) {
    const cronResult = core.handleCronConfirmation(userId, text);
    if (cronResult.handled) {
      core.doneProcessing(msgId);
      if (cronResult.reply) await bot.sendMessage(chatId, cronResult.reply);
      return;
    }
  }

  try {
    const pro = await core.isProMode();

    if (pro) {
      await bot.sendMessage(chatId, "🤔 Thinking...");
      const result = await core.runClaude(text, core.getSessionId(userId));
      if (result.sessionId) core.updateSession(userId, result.sessionId, text.slice(0, 30));
      if (!result.text) { await bot.sendMessage(chatId, "No response from Claude. Please try again."); return; }
      for (const chunk of core.splitText(result.text)) await bot.sendMessage(chatId, chunk);
      core.logger.info(`Reply: ${result.text.length} chars`);
    } else {
      if (core.isTrialExpired(userId)) {
        const { getMachineId } = await import('./license-client.mjs');
        const buyUrl = `https://claudeanywhere.com/buy.html?mid=${getMachineId()}`;
        await bot.sendMessage(chatId, `⚠️ Free trial expired (7 days).\n\n🛒 Upgrade to Pro — pay and it activates instantly:\n${buyUrl}\n\n• Monthly ¥39.99 | Yearly ¥399.9 (save 2 months)`);
        return;
      }

      const quota = await core.checkQuotaRemote(userId);
      if (!quota.allowed) {
        const { getMachineId } = await import('./license-client.mjs');
        const buyUrl = `https://claudeanywhere.com/buy.html?mid=${getMachineId()}`;
        await bot.sendMessage(chatId, `⚠️ Daily limit reached (5/5).\n\n🛒 Upgrade to Pro for unlimited — pay and it activates instantly:\n${buyUrl}\n\n• Monthly ¥39.99 | Yearly ¥399.9 (save 2 months)`);
        return;
      }

      await bot.sendMessage(chatId, "🤔 Thinking...");
      const result = await core.runClaude(text);
      if (!result.text) { await bot.sendMessage(chatId, "No response from Claude. Please try again."); return; }

      const fullReply = result.text + core.T.upgradeAd;
      for (const chunk of core.splitText(fullReply)) await bot.sendMessage(chatId, chunk);
      core.logger.info(`Reply (free): ${result.text.length} chars`);
    }
  } catch (err) {
    core.logger.error("Text error:", err.message);
    if (String(err).includes("session") || String(err).includes("resume")) {
      core.deleteSession(userId);
    }
    await bot.sendMessage(chatId, "Error: " + err.message);
  } finally {
    core.doneProcessing(msgId);
  }
});

// ============ Error handling ============

bot.on("polling_error", err => core.logger.error("Polling error:", err.message));

process.on("SIGINT",  () => { bot.stopPolling(); process.exit(0); });
process.on("SIGTERM", () => { bot.stopPolling(); process.exit(0); });

core.logger.info("Bot started. Waiting for messages...");
