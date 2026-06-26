/**
 * core.mjs — Shared core logic for all Claude Anywhere bridges
 *
 * Provides: Claude invocation, session management, license checking,
 * free-tier quota, cron management, command parsing, text splitting.
 *
 * Each bridge creates a ClaudeAnywhere instance with platform-specific options.
 */

import { spawn } from "child_process";
import { randomUUID } from "crypto";
import {
  writeFileSync, readFileSync, existsSync, mkdirSync,
  readdirSync, statSync,
} from "fs";
import { join, basename } from "path";
import { homedir } from "os";
import { getLicenseTier, activateLicense } from "./license-client.mjs";
import { CronManager, describeCron } from "./cron-manager.mjs";

// ============ Constants ============

const FREE_DAILY_LIMIT = 5;
const TRIAL_DAYS       = 7;
const MAX_STDERR_LEN   = 1000;

const CONFIRM_WORDS = new Set(["y", "yes", "ok", "确认", "是", "好", "好的"]);
const CANCEL_WORDS  = new Set(["n", "no", "取消", "否", "算了"]);

// Platform-specific text
const TEXTS = {
  telegram: {
    upgradeUrl:  "claudeanywhere.gumroad.com/l/claude-anywhere",
    upgradeAd:   "\n\n💡 Upgrade to Pro: unlimited chat, multi-turn, image, file → claudeanywhere.gumroad.com/l/claude-anywhere ($5.99/mo)",
    limitMsg:    "⚠️ Free limit reached (5/5 today). Upgrade to Pro for unlimited → claudeanywhere.gumroad.com/l/claude-anywhere ($5.99/mo)",
    trialExpired:"⚠️ Free trial expired (7 days). Upgrade to Pro → claudeanywhere.gumroad.com/l/claude-anywhere ($5.99/mo)",
    thinking:    "🤔 Thinking...",
    noResponse:  "No response from Claude. Please try again.",
    newSession:  "✅ New conversation started.",
    newFree:     "✅ Each message is already a fresh conversation in the free tier.\n💡 Want multi-turn sessions? Upgrade to Pro → claudeanywhere.gumroad.com/l/claude-anywhere",
    noHistory:   "No session history.",
    resumeUsage: "Usage: /resume <session id prefix>\nUse /sessions to list available sessions.",
    cronParsing: "⏰ Parsing your request...",
    cronConfirmY:"Y",
    cronConfirmN:"N",
    cronCancelled:"❌ Cancelled.",
    cronNoPush:  null, // telegram supports push
    imgProOnly:  "📷 Image analysis is a Pro feature.\n💡 Upgrade → claudeanywhere.gumroad.com/l/claude-anywhere ($5.99/mo)",
    fileProOnly: "📄 File analysis is a Pro feature.\n💡 Upgrade → claudeanywhere.gumroad.com/l/claude-anywhere ($5.99/mo)",
    cronProOnly: "⏰ Scheduled tasks (/cron) is a Pro feature.\n💡 Upgrade → claudeanywhere.gumroad.com/l/claude-anywhere ($5.99/mo)",
    sessionsProOnly: "📋 Session history is a Pro feature.\n💡 Upgrade → claudeanywhere.gumroad.com/l/claude-anywhere ($5.99/mo)",
    resumeProOnly: "🔄 /resume is a Pro feature.\n💡 Upgrade → claudeanywhere.gumroad.com/l/claude-anywhere ($5.99/mo)",
    helpPro:
      "🤖 *Claude Anywhere Pro* — Telegram\n\n" +
      "*🚀 Quick Start — just send a message:*\n" +
      "• `What is quantum computing?` — ask anything\n" +
      "• Send a photo → `What's in this image?`\n" +
      "• Attach a PDF/Excel/CSV → auto analysis\n" +
      "• `Write a Python script to rename files`\n" +
      "• `Help me debug this code` (paste code)\n\n" +
      "*📋 Commands:*\n" +
      "/new — Start a new conversation (clears context)\n" +
      "/sessions — List your recent sessions\n" +
      "/resume `<id>` — Continue a previous session\n" +
      "　　e.g. `/resume abc` (first few chars of session id)\n" +
      "/status — Show current session info\n" +
      "/cron `<task>` — Schedule a recurring task\n" +
      "　　e.g. `/cron every day at 9am check server`\n" +
      "　　e.g. `/cron every Monday summarize my tasks`\n" +
      "/cron list — View all scheduled tasks\n" +
      "/cron remove `<id>` — Delete a task\n" +
      "/activate `<key>` — Activate license key\n" +
      "/help — Show this message\n\n" +
      "📎 *Supported files:* PDF, Excel, CSV, Word, images, code files",
    helpFree:
      "🤖 *Claude Anywhere* — Free Tier\n\n" +
      "*🚀 Quick Start — just send a message:*\n" +
      "• `What is machine learning?`\n" +
      "• `Write an email for me`\n" +
      "• `Translate this to English: [text]`\n\n" +
      "*📋 Commands:*\n" +
      "/new — Start a fresh conversation\n" +
      "/status — Check daily usage & trial days left\n" +
      "/activate `<key>` — Activate Pro license\n" +
      "/help — Show this message\n\n" +
      "*⚠️ Free limits:*\n" +
      "```\n" +
      "Feature          Free    Pro\n" +
      "─────────────────────────────\n" +
      "Messages/day     5       ∞\n" +
      "Multi-turn       ✗       ✓\n" +
      "Image analysis   ✗       ✓\n" +
      "File analysis    ✗       ✓\n" +
      "Scheduled tasks  ✗       ✓\n" +
      "```\n\n" +
      "💡 *Upgrade Pro* → unlimited messages, multi-turn, images & files\n" +
      "claudeanywhere.gumroad.com/l/claude-anywhere ($5.99/mo)",
    cronHelp:
      "⏰ *Scheduled Tasks — /cron*\n\n" +
      "*How to create a task (natural language):*\n" +
      "`/cron every day at 9am check server status`\n" +
      "`/cron every weekday at 8pm sync data`\n" +
      "`/cron every Monday at 10am send me a summary`\n" +
      "`/cron in 30 minutes remind me about the meeting`\n\n" +
      "*Manage tasks:*\n" +
      "`/cron list` — List all scheduled tasks\n" +
      "`/cron remove <id>` — Delete a task (use id from list)\n" +
      "`/cron help` — Show this help\n\n" +
      "Max 10 tasks per user.",
    cronNoJobs:  "📋 You have no scheduled tasks yet.\n\nExample: `/cron every day at 9am check server status`\nSend `/cron help` for more examples.",
    cronRemoveUsage: "Usage: `/cron remove <job id>`\nRun `/cron list` first to see your task IDs.",
    activateUsage: "Usage: `/activate <license-key>`\n\nBuy Pro → claudeanywhere.gumroad.com/l/claude-anywhere ($5.99/mo)",
  },
  wecom: {
    upgradeUrl:  "support@claudeanywhere.com",
    upgradeAd:   "\n\n💡 升级Pro版：无限对话、多轮会话、图片文件分析 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    limitMsg:    "⚠️ 今日免费额度已用完（5/5）。升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    trialExpired:"⚠️ 免费试用已到期（7天）。升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    thinking:    "<think>正在思考...</think>",
    noResponse:  "Claude 没有返回结果，请重试。",
    newSession:  "✅ 已开始新对话。",
    newFree:     "✅ 每条消息默认就是独立对话（免费版）。\n💡 升级Pro版可获得多轮会话 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    noHistory:   "没有历史会话。",
    resumeUsage: "用法: /resume <会话ID前几位>\n先用 /sessions 查看可用会话。",
    cronParsing: "⏰ 正在解析你的需求...",
    cronConfirmY:"Y",
    cronConfirmN:"N",
    cronCancelled:"❌ 已取消。",
    cronNoPush:  null, // wecom supports push
    imgProOnly:  "📷 图片分析是Pro版功能。\n💡 升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    fileProOnly: "📄 文件分析是Pro版功能。\n💡 升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    cronProOnly: "⏰ 定时任务（/cron）是Pro版功能。\n💡 升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    sessionsProOnly: "⚠️ /sessions 是Pro版功能。\n💡 升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    resumeProOnly: "⚠️ /resume 是Pro版功能。\n💡 升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    helpPro:
      "🤖 Claude Anywhere Pro — 企业微信\n\n" +
      "🚀 快速开始 — 直接发消息即可：\n" +
      "• 「量子计算是什么？」— 问任何问题\n" +
      "• 发送图片 → 「这张图里有什么？」\n" +
      "• 发送 PDF/Excel/CSV → 自动分析\n" +
      "• 「帮我写一个重命名文件的Python脚本」\n" +
      "• 「帮我 debug 这段代码」（粘贴代码）\n\n" +
      "📋 命令列表：\n" +
      "/new — 开始新对话（清除上下文）\n" +
      "/sessions — 查看最近的历史会话\n" +
      "/resume <id> — 继续某个历史会话\n" +
      "　　例：/resume abc（会话ID前几位）\n" +
      "/status — 显示当前会话信息\n" +
      "/cron <任务> — 创建定时任务（自然语言）\n" +
      "　　例：/cron 每天早上9点检查服务器\n" +
      "　　例：/cron 每周一总结本周任务\n" +
      "/cron list — 查看所有定时任务\n" +
      "/cron remove <id> — 删除定时任务\n" +
      "/activate <激活码> — 激活授权码\n" +
      "/help — 显示此帮助\n\n" +
      "📎 支持的文件：PDF、Excel、CSV、Word、图片、代码文件",
    helpFree:
      "🤖 Claude Anywhere 免费版 — 企业微信\n\n" +
      "🚀 快速开始 — 直接发消息即可：\n" +
      "• 「帮我解释一下这段代码」\n" +
      "• 「用中文总结一下：...」\n" +
      "• 「给我写一封邮件，主题是...」\n\n" +
      "📋 命令：\n" +
      "/new — 新建对话\n" +
      "/status — 查看今日用量和试用剩余天数\n" +
      "/activate <激活码> — 激活Pro授权码\n" +
      "/help — 显示帮助\n\n" +
      "免费版 vs Pro版：\n" +
      "┌──────────┬──────┬──────┐\n" +
      "│ 功能     │ 免费 │ Pro  │\n" +
      "├──────────┼──────┼──────┤\n" +
      "│ 每日条数 │  5   │ 无限 │\n" +
      "│ 多轮对话 │  ✗   │  ✓   │\n" +
      "│ 图片分析 │  ✗   │  ✓   │\n" +
      "│ 文件分析 │  ✗   │  ✓   │\n" +
      "│ 定时任务 │  ✗   │  ✓   │\n" +
      "└──────────┴──────┴──────┘\n\n" +
      "💡 升级Pro版 → support@claudeanywhere.com\n" +
      "¥39.99/月，年付¥399.9（省2个月）",
    cronHelp:
      "⏰ 定时任务 /cron\n\n" +
      "创建方法（用自然语言描述）：\n" +
      "/cron 每天早上9点检查服务器状态\n" +
      "/cron 每周一到周五晚8点同步数据\n" +
      "/cron 每周一上午10点发送本周总结\n" +
      "/cron 30分钟后提醒我开会\n\n" +
      "管理命令：\n" +
      "/cron list — 查看所有定时任务\n" +
      "/cron remove <id> — 删除任务（id从 list 获取）\n" +
      "/cron help — 显示此帮助\n\n" +
      "每用户最多10个任务。",
    cronNoJobs:  "📋 您还没有定时任务。\n\n示例：/cron 每天早上9点检查服务器状态\n发送 /cron help 查看更多示例。",
    cronRemoveUsage: "用法：/cron remove <任务ID>\n先用 /cron list 查看任务列表及ID。",
    activateUsage: "用法：/activate <激活码>\n\n购买Pro版 → support@claudeanywhere.com\n¥39.99/月，年付¥399.9（省2个月）",
  },
  qq: {
    upgradeUrl:  "support@claudeanywhere.com",
    upgradeAd:   "\n\n💡 升级Pro版：无限对话、多轮会话、图片文件分析 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    limitMsg:    "⚠️ 今日免费额度已用完（5/5）。升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    trialExpired:"⚠️ 免费试用已到期（7天）。升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    thinking:    "🤔 正在思考...",
    noResponse:  "Claude 没有返回结果，请重试。",
    newSession:  "✅ 已开始新对话。",
    newFree:     "✅ 每条消息默认就是独立对话（免费版）。\n💡 升级Pro版可获得多轮会话 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    noHistory:   "没有历史会话。",
    resumeUsage: "用法: /resume <会话ID前几位>\n先用 /sessions 查看可用会话。",
    cronParsing: "⏰ 正在解析你的需求...",
    cronConfirmY:"Y",
    cronConfirmN:"N",
    cronCancelled:"❌ 已取消。",
    cronNoPush:  "⚠️ 注意：QQ不支持定时推送结果，建议使用Telegram或企业微信。",
    imgProOnly:  "📷 图片分析是Pro版功能。\n💡 升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    fileProOnly: "📄 文件分析是Pro版功能。\n💡 升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    cronProOnly: "⏰ 定时任务（/cron）是Pro版功能。\n💡 升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    sessionsProOnly: "⚠️ /sessions 是Pro版功能。\n💡 升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    resumeProOnly: "⚠️ /resume 是Pro版功能。\n💡 升级Pro版 → 联系 support@claudeanywhere.com（¥39.99/月，年付¥399.9省2个月）",
    helpPro:
      "🤖 Claude Anywhere Pro — QQ\n\n" +
      "🚀 快速开始 — 直接发消息即可：\n" +
      "• 「量子计算是什么？」— 问任何问题\n" +
      "• 发送图片 → 「这张图里有什么？」\n" +
      "• 发送 PDF/Excel/CSV → 自动分析\n" +
      "• 「帮我写一个重命名文件的Python脚本」\n" +
      "• 「帮我 debug 这段代码」（粘贴代码）\n\n" +
      "📋 命令列表：\n" +
      "/new — 开始新对话（清除上下文）\n" +
      "/sessions — 查看最近的历史会话\n" +
      "/resume <id> — 继续某个历史会话\n" +
      "　　例：/resume abc（会话ID前几位）\n" +
      "/status — 显示当前会话信息\n" +
      "/cron <任务> — 创建定时任务（自然语言）\n" +
      "　　例：/cron 每天早上9点检查服务器\n" +
      "　　例：/cron 每周一总结本周任务\n" +
      "/cron list — 查看所有定时任务\n" +
      "/cron remove <id> — 删除定时任务\n" +
      "/activate <激活码> — 激活授权码\n" +
      "/help — 显示此帮助\n\n" +
      "⚠️ 注意：QQ不支持定时任务推送结果，建议用企业微信。\n" +
      "📎 支持的文件：PDF、Excel、CSV、Word、图片、代码文件",
    helpFree:
      "🤖 Claude Anywhere 免费版 — QQ\n\n" +
      "🚀 快速开始 — 直接发消息即可：\n" +
      "• 「帮我解释一下这段代码」\n" +
      "• 「用中文总结一下：...」\n" +
      "• 「给我写一封邮件，主题是...」\n\n" +
      "📋 命令：\n" +
      "/new — 新建对话\n" +
      "/status — 查看今日用量和试用剩余天数\n" +
      "/activate <激活码> — 激活Pro授权码\n" +
      "/help — 显示帮助\n\n" +
      "免费版 vs Pro版：\n" +
      "┌──────────┬──────┬──────┐\n" +
      "│ 功能     │ 免费 │ Pro  │\n" +
      "├──────────┼──────┼──────┤\n" +
      "│ 每日条数 │  5   │ 无限 │\n" +
      "│ 多轮对话 │  ✗   │  ✓   │\n" +
      "│ 图片分析 │  ✗   │  ✓   │\n" +
      "│ 文件分析 │  ✗   │  ✓   │\n" +
      "│ 定时任务 │  ✗   │  ✓   │\n" +
      "└──────────┴──────┴──────┘\n\n" +
      "💡 升级Pro版 → support@claudeanywhere.com\n" +
      "¥39.99/月，年付¥399.9（省2个月）",
    cronHelp:
      "⏰ 定时任务 /cron\n\n" +
      "创建方法（用自然语言描述）：\n" +
      "/cron 每天早上9点检查服务器状态\n" +
      "/cron 每周一到周五晚8点同步数据\n" +
      "/cron 每周一上午10点发送本周总结\n" +
      "/cron 30分钟后提醒我开会\n\n" +
      "管理命令：\n" +
      "/cron list — 查看所有定时任务\n" +
      "/cron remove <id> — 删除任务（id从 list 获取）\n" +
      "/cron help — 显示此帮助\n\n" +
      "⚠️ 注意：QQ不支持定时推送结果，建议用企业微信。\n" +
      "每用户最多10个任务。",
    cronNoJobs:  "📋 您还没有定时任务。\n\n示例：/cron 每天早上9点检查服务器状态\n发送 /cron help 查看更多示例。",
    cronRemoveUsage: "用法：/cron remove <任务ID>\n先用 /cron list 查看任务列表及ID。",
    activateUsage: "用法：/activate <激活码>\n\n购买Pro版 → support@claudeanywhere.com\n¥39.99/月，年付¥399.9（省2个月）",
  },
};

// ============ Helpers ============

function todayStr() {
  return new Date().toISOString().slice(0, 10);
}

function makeLogger(platform) {
  const tag = `[${platform.toUpperCase()}]`;
  return {
    info:  (...a) => console.log( new Date().toISOString(), tag, "[INFO]",  ...a),
    warn:  (...a) => console.warn( new Date().toISOString(), tag, "[WARN]",  ...a),
    error: (...a) => console.error(new Date().toISOString(), tag, "[ERROR]", ...a),
  };
}

function isValidUserText(text) {
  if (!text || typeof text !== "string") return false;
  const t = text.trimStart();
  if (t.startsWith("<") || t.startsWith("[{") || t.startsWith("{")) return false;
  if (t.startsWith("图片文件:") || t.startsWith("/tmp/") || t.startsWith("文件已保存到:")) return false;
  if (t.startsWith("最近") && t.includes("个会话")) return false;
  if (t.startsWith("Unknown skill:") || t.startsWith("conversations")) return false;
  if (t.length < 2) return false;
  return true;
}

// ============ Main Class ============

export class ClaudeAnywhere {
  /**
   * @param {object} options
   * @param {string} options.platform      - "telegram" | "wecom" | "qq"
   * @param {string} [options.claudePath]  - Path to claude binary
   * @param {string} [options.claudeCwd]   - Working directory for claude
   * @param {string[]} [options.knowledgeDirs] - Knowledge base directories
   * @param {number} [options.claudeTimeoutMs] - Timeout for claude process
   * @param {number} [options.maxReplyLength]  - Max reply length per chunk
   */
  constructor(options) {
    this.platform       = options.platform || "telegram";
    this.claudePath     = options.claudePath || process.env.CLAUDE_PATH?.trim() || "claude";
    this.claudeCwd      = options.claudeCwd  || process.env.CLAUDE_CWD?.trim()  || process.cwd();
    this.knowledgeDirs  = options.knowledgeDirs || (process.env.KNOWLEDGE_DIR || "").split(",").map(d => d.trim()).filter(Boolean);
    this.claudeTimeoutMs = options.claudeTimeoutMs || parseInt(process.env.CLAUDE_TIMEOUT_MS || "600000", 10);
    this.maxReplyLength = options.maxReplyLength || parseInt(process.env.MAX_REPLY_LENGTH || "4000", 10);

    this.logger = makeLogger(this.platform);
    this.T = TEXTS[this.platform] || TEXTS.telegram;

    // Session file per platform
    const dir = join(homedir(), ".claude-anywhere");
    mkdirSync(dir, { recursive: true });
    this._sessionsFile = join(dir, `${this.platform}-sessions.json`);
    this._chatIdsFile  = join(dir, `${this.platform}-chat-ids.json`);

    // Free tier state
    const stateDir = join(homedir(), ".claude-anywhere-free");
    mkdirSync(stateDir, { recursive: true });
    this._stateFile = join(stateDir, `${this.platform}-state.json`);
    this._trialFile = join(stateDir, `${this.platform}-trial.json`);

    // In-memory state
    this._proMode      = null;
    this._userSessions = this._loadSessions();
    this._appState     = this._loadState();
    this._trialState   = this._loadTrialState();
    this._dailyCount   = new Map();
    this._chatIds      = this._loadChatIds();
    this._processing   = new Set();
    this._pendingCron  = new Map();

    // Cron manager — onResult callback set by bridge via setCronResultHandler()
    this._cronOnResult = null;
    this.cronManager = new CronManager({
      claudePath: this.claudePath,
      claudeCwd:  this.claudeCwd,
      onResult: async (jobId, jobName, userId, result) => {
        if (this._cronOnResult) {
          await this._cronOnResult(jobId, jobName, userId, result);
        }
      },
    });
    this.cronManager.start();
  }

  /**
   * Set the cron result delivery callback (bridge-specific).
   * @param {function} handler - async (jobId, jobName, userId, resultText) => void
   */
  setCronResultHandler(handler) {
    this._cronOnResult = handler;
  }

  // ============ License ============

  async isProMode() {
    this._proMode = null;
    const tier = await getLicenseTier();
    this._proMode = (tier === "pro");
    return this._proMode;
  }

  async activateLicense(key) {
    return activateLicense(key);
  }

  // ============ Session persistence ============

  _loadSessions() {
    try {
      if (existsSync(this._sessionsFile)) {
        return new Map(Object.entries(JSON.parse(readFileSync(this._sessionsFile, "utf-8"))));
      }
    } catch {}
    return new Map();
  }

  _saveSessions() {
    try {
      writeFileSync(this._sessionsFile, JSON.stringify(Object.fromEntries(this._userSessions), null, 2));
    } catch {}
  }

  getSession(userId) {
    return this._userSessions.get(userId) || null;
  }

  getSessionId(userId) {
    return this._userSessions.get(userId)?.sessionId || null;
  }

  updateSession(userId, sessionId, label) {
    if (sessionId) {
      this._userSessions.set(userId, { sessionId, lastUsed: Date.now(), label: label || "" });
      this._saveSessions();
      this.logger.info(`Session updated: [${userId}] -> ${sessionId.slice(0, 8)}...`);
    }
  }

  deleteSession(userId) {
    this._userSessions.delete(userId);
    this._saveSessions();
  }

  // ============ Chat ID tracking (for cron result delivery) ============

  _loadChatIds() {
    try {
      if (existsSync(this._chatIdsFile)) {
        return new Map(Object.entries(JSON.parse(readFileSync(this._chatIdsFile, "utf-8"))));
      }
    } catch {}
    return new Map();
  }

  _saveChatIds() {
    try {
      writeFileSync(this._chatIdsFile, JSON.stringify(Object.fromEntries(this._chatIds), null, 2));
    } catch {}
  }

  trackChatId(userId, chatId) {
    if (this._chatIds.get(userId) !== chatId) {
      this._chatIds.set(userId, chatId);
      this._saveChatIds();
    }
  }

  getChatId(userId) {
    return this._chatIds.get(userId);
  }

  // ============ Free tier state ============

  _loadState() {
    try {
      if (existsSync(this._stateFile)) return JSON.parse(readFileSync(this._stateFile, "utf-8"));
    } catch {}
    return { users: {} };
  }

  _saveState() {
    try { writeFileSync(this._stateFile, JSON.stringify(this._appState, null, 2)); } catch {}
  }

  _loadTrialState() {
    try {
      if (existsSync(this._trialFile)) return JSON.parse(readFileSync(this._trialFile, "utf-8"));
    } catch {}
    return {};
  }

  _saveTrialState() {
    try { writeFileSync(this._trialFile, JSON.stringify(this._trialState, null, 2)); } catch {}
  }

  /**
   * Check trial expiration (telegram-style: separate trial file).
   */
  isTrialExpired(userId) {
    const today = todayStr();
    if (!this._trialState[userId]) {
      this._trialState[userId] = today;
      this._saveTrialState();
      return false;
    }
    const daysDiff = Math.floor((new Date(today) - new Date(this._trialState[userId])) / 86400000);
    return daysDiff >= TRIAL_DAYS;
  }

  /**
   * Check and increment quota (wecom-style: unified state file).
   * Returns { allowed, reason: null | "daily_limit" | "trial_expired" }
   */
  checkQuota(userId) {
    const today = todayStr();
    const users = this._appState.users;

    if (!users[userId]) {
      users[userId] = { firstUsed: today, daily: {} };
      this._saveState();
    }

    const user = users[userId];
    const daysDiff = Math.floor((new Date(today) - new Date(user.firstUsed)) / 86400000);
    if (daysDiff >= TRIAL_DAYS) return { allowed: false, reason: "trial_expired" };

    const used = user.daily[today] || 0;
    if (used >= FREE_DAILY_LIMIT) return { allowed: false, reason: "daily_limit" };

    user.daily[today] = used + 1;
    this._saveState();
    return { allowed: true, reason: null };
  }

  /**
   * Check and increment quota via server (telegram-style, with local fallback).
   */
  async checkQuotaRemote(userId) {
    const serverUrl = process.env.LICENSE_SERVER_URL?.trim() || "https://license.claudeanywhere.com";
    const key = process.env.LICENSE_KEY?.trim();

    try {
      const res = await fetch(`${serverUrl}/v1/daily_count`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, license_key: key || null }),
        signal: AbortSignal.timeout(4000),
      });
      if (res.ok) {
        const data = await res.json();
        return { allowed: !!data.allowed, used: data.used, limit: data.limit };
      }
    } catch {}

    // Local fallback
    const today = todayStr();
    const entry = this._dailyCount.get(userId);
    const used = (entry && entry.date === today) ? entry.count : 0;
    if (used >= FREE_DAILY_LIMIT) return { allowed: false, used, limit: FREE_DAILY_LIMIT };
    this._dailyCount.set(userId, { date: today, count: used + 1 });
    return { allowed: true, used: used + 1, limit: FREE_DAILY_LIMIT };
  }

  getDailyUsage(userId) {
    const today = todayStr();
    const entry = this._dailyCount.get(userId);
    if (!entry || entry.date !== today) return 0;
    return entry.count;
  }

  getStatusText(userId) {
    const today = todayStr();
    const user  = this._appState.users[userId];
    const T = this.T;
    if (this.platform === "telegram") {
      const used = this.getDailyUsage(userId);
      const remaining = Math.max(0, FREE_DAILY_LIMIT - used);
      return `📊 Free tier\nToday: ${used}/${FREE_DAILY_LIMIT} messages used, ${remaining} remaining\n\n💡 Upgrade to Pro → ${T.upgradeUrl} ($5.99/mo)`;
    }
    // wecom / qq
    if (!user) {
      return `📊 免费试用版\n今日：0/${FREE_DAILY_LIMIT} 条\n剩余试用：${TRIAL_DAYS} 天\n\n${T.upgradeAd.trim()}`;
    }
    const used      = user.daily[today] || 0;
    const remaining = Math.max(0, FREE_DAILY_LIMIT - used);
    const daysDiff  = Math.floor((new Date(today) - new Date(user.firstUsed)) / 86400000);
    const trialLeft = Math.max(0, TRIAL_DAYS - daysDiff);
    return `📊 免费试用版\n今日：${used}/${FREE_DAILY_LIMIT} 条，剩余 ${remaining} 条\n剩余试用天数：${trialLeft} 天\n\n${T.upgradeAd.trim()}`;
  }

  // ============ Claude session list (auto-discover) ============

  listClaudeSessions(limit = 10) {
    const base = join(homedir(), ".claude", "projects");
    if (!existsSync(base)) return [];

    let dirs;
    try {
      dirs = readdirSync(base)
        .map(d => join(base, d))
        .filter(d => { try { return statSync(d).isDirectory(); } catch { return false; } });
    } catch { return []; }

    const all = [];
    for (const dir of dirs) {
      try {
        const files = readdirSync(dir).filter(f => f.endsWith(".jsonl"));
        for (const f of files) {
          const fullPath = join(dir, f);
          const id = basename(f, ".jsonl");
          let mtime = 0;
          try { mtime = statSync(fullPath).mtimeMs; } catch {}
          let lastUserMsg = "";
          let lastAssistantMsg = "";
          try {
            const lines = readFileSync(fullPath, "utf-8").split("\n");
            for (let i = lines.length - 1; i >= 0; i--) {
              if (!lines[i].trim()) continue;
              try {
                const j = JSON.parse(lines[i]);
                if (!lastUserMsg && j.type === "user" && isValidUserText(j.message?.content)) {
                  lastUserMsg = j.message.content.slice(0, 50).replace(/\n/g, " ");
                }
                if (!lastAssistantMsg && j.type === "assistant" && j.message?.content) {
                  const c = j.message.content;
                  if (typeof c === "string") {
                    lastAssistantMsg = c.slice(0, 50).replace(/\n/g, " ");
                  } else if (Array.isArray(c)) {
                    const tb = c.find(b => b.type === "text" && b.text);
                    if (tb) lastAssistantMsg = tb.text.slice(0, 50).replace(/\n/g, " ");
                  }
                }
                if (lastUserMsg && lastAssistantMsg) break;
              } catch {}
            }
          } catch {}
          all.push({ id, mtime, lastUserMsg, lastAssistantMsg });
        }
      } catch {}
    }

    return all.sort((a, b) => b.mtime - a.mtime).slice(0, limit);
  }

  // ============ Claude invocation ============

  runClaude(message, sessionId = null, imagePaths = []) {
    return new Promise((resolve, reject) => {
      let fullMessage = message;
      if (imagePaths.length > 0) {
        const imgList = imagePaths.map(p => `图片文件: ${p}`).join("\n");
        fullMessage = `${imgList}\n\n${message}\n\n（请用 Read 工具读取上述图片文件来查看图片内容）`;
      }

      const args = [
        "-p", fullMessage,
        "--max-turns", "100",
        "--output-format", "json",
        "--dangerously-skip-permissions",
      ];

      if (sessionId) args.push("--resume", sessionId);
      for (const dir of this.knowledgeDirs) args.push("--add-dir", dir);

      this.logger.info(`Claude: ${sessionId ? "resume " + sessionId.slice(0, 8) : "new"} | ${message.slice(0, 80)}`);

      const proc = spawn(this.claudePath, args, {
        cwd: this.claudeCwd,
        env: { ...process.env },
        timeout: this.claudeTimeoutMs,
        stdio: ["pipe", "pipe", "pipe"],
      });

      let stdout = "";
      let stderr = "";

      proc.stdout.on("data", c => { stdout += c.toString(); });
      proc.stderr.on("data", c => { if (stderr.length < MAX_STDERR_LEN) stderr += c.toString(); });

      proc.on("close", code => {
        proc.stdout.removeAllListeners();
        proc.stderr.removeAllListeners();
        proc.removeAllListeners();

        if (code === 0 || stdout.trim()) {
          try {
            const json = JSON.parse(stdout.trim());
            resolve({ text: json.result || json.text || stdout.trim(), sessionId: json.session_id || null });
          } catch {
            resolve({ text: stdout.trim(), sessionId: null });
          }
          stdout = "";
        } else {
          this.logger.error(`Claude exit ${code}: ${stderr.slice(0, 300)}`);
          const errMsg = this.platform === "telegram"
            ? `Claude error (code=${code})`
            : `Claude 执行出错 (code=${code})`;
          resolve({ text: errMsg, sessionId: null });
        }
      });

      proc.on("error", err => {
        proc.stdout.removeAllListeners();
        proc.stderr.removeAllListeners();
        proc.removeAllListeners();
        const errMsg = this.platform === "telegram"
          ? `Failed to start Claude: ${err.message}`
          : `Claude 启动失败: ${err.message}`;
        reject(new Error(errMsg));
      });

      proc.stdin.end();
    });
  }

  // ============ Text splitting ============

  splitText(text, limit) {
    limit = limit || this.maxReplyLength;
    if (text.length <= limit) return [text];
    const chunks = [];
    let rem = text;
    while (rem.length > 0) {
      let end = limit;
      if (rem.length > limit) {
        const nl = rem.lastIndexOf("\n", limit);
        if (nl > limit * 0.5) end = nl;
      }
      chunks.push(rem.slice(0, end));
      rem = rem.slice(end);
    }
    return chunks;
  }

  // ============ Command parsing ============

  parseCommand(text) {
    if (!text) return null;
    if (text === "/new" || text === "/reset" || text === "新对话") return { cmd: "new" };
    if (text === "/status")   return { cmd: "status" };
    if (text === "/sessions") return { cmd: "sessions" };
    if (text === "/resume")   return { cmd: "resume_help" };
    if (text === "/help" || text === "/start") return { cmd: "help" };
    const resumeM = text.match(/^\/resume\s+(.+)$/);
    if (resumeM) return { cmd: "resume", id: resumeM[1].trim() };
    const activateM = text.match(/^\/activate(?:\s+(.+))?$/);
    if (activateM) return { cmd: "activate", key: activateM[1]?.trim() };
    const cronM = text.match(/^\/cron(?:\s+([\s\S]*))?$/);
    if (cronM) return { cmd: "cron", args: (cronM[1] || "").trim() };
    return null;
  }

  // ============ Dedup ============

  isProcessing(msgId) {
    if (this._processing.has(msgId)) return true;
    this._processing.add(msgId);
    return false;
  }

  doneProcessing(msgId) {
    this._processing.delete(msgId);
  }

  // ============ Pending cron confirmation ============

  hasPendingCron(userId) {
    return this._pendingCron.has(userId);
  }

  /**
   * Handle a pending cron confirmation.
   * Returns { handled: boolean, reply?: string }
   */
  handleCronConfirmation(userId, text) {
    if (!this._pendingCron.has(userId)) return { handled: false };

    const lower = text.trim().toLowerCase();

    if (CONFIRM_WORDS.has(lower)) {
      const pending = this._pendingCron.get(userId);
      clearTimeout(pending.timer);
      this._pendingCron.delete(userId);

      const { type, schedule, prompt, name } = pending;
      let r;
      if (type === "once") {
        r = this.cronManager.addOnce({ name, runAt: schedule, prompt, userId });
      } else {
        r = this.cronManager.add({ name, schedule, prompt, userId });
      }

      if (!r.ok) return { handled: true, reply: `❌ ${r.error}` };

      const id8 = r.job.id.slice(0, 8);
      let doneText;
      if (this.platform === "telegram") {
        if (type === "once") {
          const at = new Date(r.job.runAt).toLocaleString();
          doneText = `✅ Scheduled: "${name}"\nSchedule: once at ${at}\nTask: ${prompt}\nID: ${id8}\n\n/cron list — view all | /cron remove ${id8} — delete`;
        } else {
          doneText = `✅ Scheduled: "${name}"\nSchedule: ${schedule} (${describeCron(schedule)})\nTask: ${prompt}\nID: ${id8}\n\n/cron list — view all | /cron remove ${id8} — delete`;
        }
      } else {
        if (type === "once") {
          const at = new Date(r.job.runAt).toLocaleString("zh-CN");
          doneText = `✅ 定时任务已创建："${name}"\n调度：一次性，${at}\n任务：${prompt}\nID：${id8}\n\n/cron list 查看所有 | /cron remove ${id8} 删除`;
        } else {
          doneText = `✅ 定时任务已创建："${name}"\n调度：${schedule}（${describeCron(schedule)}）\n任务：${prompt}\nID：${id8}\n\n/cron list 查看所有 | /cron remove ${id8} 删除`;
        }
      }
      return { handled: true, reply: doneText };
    }

    if (CANCEL_WORDS.has(lower)) {
      const pending = this._pendingCron.get(userId);
      clearTimeout(pending.timer);
      this._pendingCron.delete(userId);
      return { handled: true, reply: this.T.cronCancelled };
    }

    // Not a confirm/cancel — clear pending and fall through
    clearTimeout(this._pendingCron.get(userId).timer);
    this._pendingCron.delete(userId);
    return { handled: false };
  }

  // ============ Command handling ============

  /**
   * Handle a parsed command. Returns an array of reply strings.
   * @param {string} userId
   * @param {object} command - from parseCommand()
   * @param {boolean} pro
   * @returns {Promise<{ replies: string[], parseMode?: string }>}
   */
  async handleCommand(userId, command, pro) {
    const T = this.T;

    switch (command.cmd) {
      case "new":
        if (pro) {
          this.deleteSession(userId);
          return { replies: [T.newSession] };
        }
        return { replies: [T.newFree] };

      case "status": {
        if (pro) {
          const s = this.getSession(userId);
          const locale = this.platform === "telegram" ? undefined : "zh-CN";
          const text = s
            ? (this.platform === "telegram"
              ? `✅ Pro mode active\n\nCurrent session: ${s.sessionId.slice(0, 8)}...\nLast used: ${new Date(s.lastUsed).toLocaleString(locale)}`
              : `✅ Pro版已激活\n\n当前会话: ${s.sessionId.slice(0, 8)}...\n上次使用: ${new Date(s.lastUsed).toLocaleString(locale)}`)
            : (this.platform === "telegram"
              ? "✅ Pro mode active\n\nNo active session — next message starts a new one."
              : "✅ Pro版已激活\n\n无活跃会话，下条消息将开始新对话。");
          return { replies: [text] };
        }
        return { replies: [this.getStatusText(userId)] };
      }

      case "sessions":
        if (!pro) return { replies: [T.sessionsProOnly] };
        {
          const sessions = this.listClaudeSessions(10);
          if (!sessions.length) return { replies: [T.noHistory] };
          const locale = this.platform === "telegram" ? undefined : "zh-CN";
          let text = this.platform === "telegram" ? "Recent 10 sessions:\n\n" : "最近10个会话:\n\n";
          for (const s of sessions) {
            const date = new Date(s.mtime).toLocaleString(locale);
            const user = s.lastUserMsg || (this.platform === "telegram" ? "(no content)" : "无内容");
            const asst = s.lastAssistantMsg ? `\n  🤖 ${s.lastAssistantMsg}` : "";
            text += `${s.id.slice(0, 8)} | ${date}\n  👤 ${user}${asst}\n\n`;
          }
          text += this.platform === "telegram"
            ? "Use /resume <first 8 chars of id> to resume"
            : "用 /resume <id前8位> 恢复会话";
          return { replies: [text] };
        }

      case "resume_help":
        if (!pro) return { replies: [T.resumeProOnly] };
        return { replies: [T.resumeUsage] };

      case "resume": {
        if (!pro) return { replies: [T.resumeProOnly] };
        const sessions = this.listClaudeSessions(50);
        const found = sessions.find(s => s.id.startsWith(command.id));
        if (found) {
          this._userSessions.set(userId, { sessionId: found.id, lastUsed: Date.now(), label: found.lastUserMsg || "" });
          this._saveSessions();
          const msg = this.platform === "telegram"
            ? `✅ Session resumed: ${found.id.slice(0, 8)}...\n👤 ${found.lastUserMsg || "(no content)"}`
            : `✅ 已恢复会话: ${found.id.slice(0, 8)}...\n👤 ${found.lastUserMsg || "无内容"}`;
          return { replies: [msg] };
        }
        const notFound = this.platform === "telegram"
          ? `❌ No session starting with "${command.id}".\nUse /sessions to list available sessions.`
          : `❌ 未找到以 "${command.id}" 开头的会话。\n用 /sessions 查看可用会话。`;
        return { replies: [notFound] };
      }

      case "activate": {
        if (!command.key) return { replies: [T.activateUsage] };
        const validating = this.platform === "telegram" ? "🔑 Validating license..." : "🔑 正在验证激活码...";
        const result = await this.activateLicense(command.key);
        let msg;
        if (result.success) {
          msg = this.platform === "telegram"
            ? `✅ ${result.message}\n\nSet LICENSE_KEY=${command.key} in your .env file and restart the bot.`
            : `✅ ${result.message}\n\n请在 .env 中设置 LICENSE_KEY=${command.key} 并重启服务。`;
        } else {
          msg = this.platform === "telegram"
            ? `❌ ${result.message}\n\nGet a valid key → ${T.upgradeUrl}`
            : `❌ ${result.message}\n\n购买Pro版 → 联系 ${T.upgradeUrl}（¥39.99/月，年付¥399.9省2个月）`;
        }
        return { replies: [validating, msg] };
      }

      case "help":
        return { replies: [pro ? T.helpPro : T.helpFree], parseMode: "Markdown" };

      case "cron":
        return this._handleCronCommand(userId, command.args, pro);

      default:
        return { replies: [] };
    }
  }

  // ============ Cron sub-command handling ============

  async _handleCronCommand(userId, args, pro) {
    const T = this.T;

    if (!pro) return { replies: [T.cronProOnly] };

    const sub = (args || "").split(/\s+/)[0]?.toLowerCase();

    if (!sub || sub === "help") {
      return { replies: [T.cronHelp], parseMode: "Markdown" };
    }

    if (sub === "list") {
      const jobs = this.cronManager.list(userId);
      if (!jobs.length) return { replies: [T.cronNoJobs] };

      const locale = this.platform === "telegram" ? undefined : "zh-CN";
      let text = this.platform === "telegram"
        ? `📋 Your scheduled jobs (${jobs.length}/10):\n\n`
        : `📋 您的定时任务（${jobs.length}/10）：\n\n`;

      for (const j of jobs) {
        const id8 = j.id.slice(0, 8);
        if (j.type === "cron") {
          text += this.platform === "telegram"
            ? `[${id8}] "${j.name}"\n  ⏱ ${j.schedule} (${describeCron(j.schedule)})\n\n`
            : `[${id8}] "${j.name}"\n  ⏱ ${j.schedule}（${describeCron(j.schedule)}）\n\n`;
        } else {
          const at = new Date(j.runAt).toLocaleString(locale);
          text += this.platform === "telegram"
            ? `[${id8}] "${j.name}"\n  📅 Once at ${at}\n\n`
            : `[${id8}] "${j.name}"\n  📅 一次性，执行时间：${at}\n\n`;
        }
      }
      text += this.platform === "telegram" ? "/cron remove <id> to delete" : "/cron remove <id> 删除任务";
      return { replies: [text] };
    }

    if (sub === "remove") {
      const rest = args.slice("remove".length).trim();
      if (!rest) return { replies: [T.cronRemoveUsage] };

      const jobs  = this.cronManager.list(userId);
      const found = jobs.find(j => j.id.startsWith(rest) || j.id.slice(0, 8) === rest);
      if (!found) {
        const msg = this.platform === "telegram"
          ? `❌ No job found with id starting with "${rest}".\nUse /cron list to see your jobs.`
          : `❌ 未找到ID以"${rest}"开头的任务。\n用 /cron list 查看任务列表。`;
        return { replies: [msg] };
      }
      this.cronManager.remove(found.id);
      const msg = this.platform === "telegram"
        ? `✅ Job removed: "${found.name}" [${found.id.slice(0, 8)}]`
        : `✅ 已删除任务："${found.name}"（${found.id.slice(0, 8)}）`;
      return { replies: [msg] };
    }

    // Natural language — parse, preview, wait for confirmation
    const parseResult = await this.cronManager.parseNaturalLanguage(args);
    if (!parseResult.ok) return { replies: [T.cronParsing, `❌ ${parseResult.error}`] };

    const { type, schedule, prompt, name } = parseResult.parsed;
    const locale = this.platform === "telegram" ? undefined : "zh-CN";

    let previewText;
    if (this.platform === "telegram") {
      if (type === "once") {
        const atStr = new Date(schedule).toLocaleString();
        previewText = `⏰ I'll create this scheduled task:\n\n📌 Name: ${name}\n🕐 Schedule: once at ${atStr}\n📋 Task: ${prompt}\n\nReply Y to confirm, N to cancel.`;
      } else {
        previewText = `⏰ I'll create this scheduled task:\n\n📌 Name: ${name}\n🕐 Schedule: ${describeCron(schedule)} (${schedule})\n📋 Task: ${prompt}\n\nReply Y to confirm, N to cancel.`;
      }
    } else {
      if (type === "once") {
        const atStr = new Date(schedule).toLocaleString(locale);
        previewText = `⏰ 即将创建以下定时任务：\n\n📌 名称：${name}\n🕐 调度：一次性，${atStr}\n📋 任务：${prompt}\n\n回复 Y 确认创建，N 取消。`;
      } else {
        previewText = `⏰ 即将创建以下定时任务：\n\n📌 名称：${name}\n🕐 调度：${describeCron(schedule)}（${schedule}）\n📋 任务：${prompt}\n\n回复 Y 确认创建，N 取消。`;
      }
    }

    // QQ platform: warn about no push support
    if (this.T.cronNoPush) {
      previewText += `\n\n${this.T.cronNoPush}`;
    }

    // Store pending confirmation with 60-second timeout
    if (this._pendingCron.has(userId)) clearTimeout(this._pendingCron.get(userId).timer);
    const timer = setTimeout(() => this._pendingCron.delete(userId), 60_000);
    this._pendingCron.set(userId, { type, schedule, prompt, name, timer });

    return { replies: [T.cronParsing, previewText] };
  }

  // ============ Unsupported file extensions ============

  static get UNSUPPORTED_EXTS() {
    return ["mp4","avi","mov","mkv","wmv","flv","webm","mp3","wav","ogg","aac","flac","m4a","zip","rar","7z","tar","gz","exe","dll","so","bin"];
  }

  static get IMAGE_EXTS() {
    return ["jpg","jpeg","png","gif","webp","bmp"];
  }
}
