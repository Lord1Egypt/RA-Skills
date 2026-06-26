import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { spawn, spawnSync } from "node:child_process";
import { createWriteStream, existsSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, extname, join } from "node:path";
import { pipeline } from "node:stream/promises";
import { fileURLToPath } from "node:url";

// ─── stdio 保护：拦截所有 stdout 写入，强制走 stderr ───
const _origStdoutWrite = process.stdout.write.bind(process.stdout);
process.stdout.write = function (chunk, encoding, callback) {
  const str = typeof chunk === 'string' ? chunk : chunk.toString();
  if (str.trimStart().startsWith('{')) {
    return _origStdoutWrite(chunk, encoding, callback);
  }
  return process.stderr.write(chunk, encoding, callback);
};
console.log = console.error;
console.warn = console.error;
console.info = console.error;
console.debug = console.error;

import { createDouyinSession, disconnect } from './index.js';
import config from './config.js';
import { startBackgroundNodeJob } from '../scripts/background-job.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || ".";
const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(HOME, ".openclaw", "workspace", "douyin-ops");
const MCP_CACHE_DIR = join(STATE_DIR, "upstream");
const PUBLISH_JOB_DIR = join(STATE_DIR, "publish-jobs");
const MARKETING_STATE_PATH = process.env.DOUYIN_MARKETING_STATE_PATH || join(STATE_DIR, "automation-marketing-state.json");
const OPENCLAW_SESSION_DIR = process.env.OPENCLAW_SESSION_DIR
  || join(HOME, ".openclaw", "agents", "main", "sessions");
const FEISHU_SOURCE_MAX_AGE_MS = Number(process.env.DOUYIN_FEISHU_SOURCE_MAX_AGE_MS || 5 * 60 * 1000);
const FEISHU_ROUTE_TIMEOUT_MS = Number(process.env.DOUYIN_FEISHU_ROUTE_TIMEOUT_MS || 1_500_000);
const DIGITAL_HUMAN_ROUTE_TIMEOUT_MS = Number(process.env.DIGITAL_HUMAN_ROUTE_TIMEOUT_MS || 1_500_000);
const IN_FLIGHT_VIDEO_STALE_MS = Number(process.env.DOUYIN_IN_FLIGHT_VIDEO_STALE_MS || 60 * 60 * 1000);

function extFromUrl(url, fallback = ".bin") {
  try {
    const ext = extname(new URL(url).pathname);
    return ext || fallback;
  } catch {
    return fallback;
  }
}

async function downloadToMcpCache(url, kind = "resource", fallbackExt = ".bin") {
  const cleanUrl = String(url || "").trim();
  if (!cleanUrl) return null;
  mkdirSync(MCP_CACHE_DIR, { recursive: true });
  const hash = createHash("sha256").update(cleanUrl).digest("hex").slice(0, 16);
  const outputPath = join(MCP_CACHE_DIR, `${hash}${extFromUrl(cleanUrl, fallbackExt)}`);
  if (existsSync(outputPath)) return outputPath;
  const response = await fetch(cleanUrl);
  if (!response.ok || !response.body) {
    throw new Error(`${kind}_download_failed:${response.status}`);
  }
  await pipeline(response.body, createWriteStream(outputPath));
  return outputPath;
}

function makeJobId(prefix = "publish") {
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`;
}

function readJsonFile(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function readJsonFileSafe(path, fallback = null) {
  try {
    if (!existsSync(path)) return fallback;
    return readJsonFile(path);
  } catch {
    return fallback;
  }
}

function freshRunning(record, staleMs) {
  if (record?.status !== "running") return false;
  const started = Date.parse(record.startedAt || "");
  if (!Number.isFinite(started)) return true;
  return Date.now() - started < staleMs;
}

function existingMarketingVideoGuard() {
  const state = readJsonFileSafe(MARKETING_STATE_PATH, null);
  if (!state) return null;
  if (state.pendingReview?.publishText || state.pendingReview?.videoUrl) {
    return {
      reason: "pending_review_exists",
      pendingReview: state.pendingReview,
    };
  }
  if (freshRunning(state.inFlightVideo, IN_FLIGHT_VIDEO_STALE_MS)) {
    return {
      reason: "in_flight_video_exists",
      inFlightVideo: state.inFlightVideo,
    };
  }
  return null;
}

function marketingLastGeneratedTaskId() {
  const state = readJsonFileSafe(MARKETING_STATE_PATH, null);
  return String(state?.lastGenerated?.video?.taskId || '').trim();
}

function parseLastJsonObject(text) {
  const raw = String(text || '').trim();
  const candidates = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  for (let i = 0; i < raw.length; i += 1) {
    const ch = raw[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') inString = true;
    else if (ch === '{') {
      if (depth === 0) start = i;
      depth += 1;
    } else if (ch === '}') {
      depth -= 1;
      if (depth === 0 && start >= 0) {
        candidates.push(raw.slice(start, i + 1));
        start = -1;
      }
    }
  }
  for (let i = candidates.length - 1; i >= 0; i -= 1) {
    try {
      return JSON.parse(candidates[i]);
    } catch {
      // keep scanning older candidates
    }
  }
  return null;
}

function routeInstruction(output) {
  const payload = parseLastJsonObject(output);
  const action = payload?.result?.action || '';
  const flowStep = payload?.flow?.step || '';
  const customerMessage = payload?.result?.customerMessage || '';
  const nextVideoJobStarted = action === "next_video_plan_job_started";
  const personaJobStarted = action === "persona_generation_job_started";
  const marketingVideoJobStarted = action === "marketing_video_generation_started" || action === "marketing_video_generation_already_running";
  const onboardingJobStarted = action === "persona_confirmed_onboarding_job_started" || action === "persona_confirmed_onboarding_already_running" || action === "onboarding_already_running";
  const marketingLongRunning = /^marketing_|^xiaoice_|^publish_pending_review|^confirmation_mode_|^bind_model_id|^digital_human_/.test(action);
  let agentInstruction;
  if (nextVideoJobStarted) {
    agentInstruction = "A background next-video-plan job has started and will send exactly one final Feishu message. Do not call douyin_next_video_plan_from_feishu_bitable, do not format a plan yourself, do not ask follow-up questions, do not send a visible Feishu reply, and never output NO_REPLY. If your runtime requires a response, output exactly HEARTBEAT_OK.";
  } else if (personaJobStarted) {
    agentInstruction = "A background persona-generation job has started and will send the exact Feishu review message when ready. Do not call douyin_persona_flow again for the same user message, do not send a visible Feishu reply, and never output NO_REPLY. If your runtime requires a response, output exactly HEARTBEAT_OK.";
  } else if (onboardingJobStarted) {
    agentInstruction = "A background onboarding job has started. It will train/check the digital human, generate the first video, and send the exact Feishu review message when ready. Do not call douyin_marketing_controller, douyin_xiaoice_video_produce, douyin_digital_human_training, or douyin_persona_flow for the same user message. Do not send a visible Feishu reply and never output NO_REPLY. If your runtime requires a response, output exactly HEARTBEAT_OK.";
  } else if (marketingVideoJobStarted) {
    agentInstruction = "A background marketing-video job has started and will send the exact video-review Feishu message when the video is ready. Do not call douyin_marketing_controller, douyin_xiaoice_video_produce, douyin_digital_human_training, or douyin_persona_flow for the same user message. Do not send a visible Feishu reply and never output NO_REPLY. If your runtime requires a response, output exactly HEARTBEAT_OK.";
  } else if (marketingLongRunning) {
    agentInstruction = "The automation-marketing route tool has handled this Feishu event. Do not call lower-level tools such as douyin_marketing_controller, douyin_xiaoice_video_produce, douyin_digital_human_training, or douyin_persona_flow for the same user message. If this call appears slow or timed out in the runtime, query status only through douyin_feishu_route_text({text:\"自动化营销状态\"}) or wait for the tool's Feishu notification; never start another plan/video/training task.";
  } else if (customerMessage) {
    agentInstruction = "The route tool already attempted the customer notification itself. Do not send a visible Feishu reply, do not repeat the message, and never output NO_REPLY. If your runtime requires a response, output exactly HEARTBEAT_OK.";
  } else {
    agentInstruction = "The route tool already handled this event. Do not send a visible Feishu reply and never output NO_REPLY. If your runtime requires a response, output exactly HEARTBEAT_OK.";
  }
  const lines = [
    JSON.stringify({
      ok: Boolean(payload?.ok),
      routed: true,
      action,
      flowStep,
      jobId: payload?.result?.jobId || payload?.result?.job?.jobId || null,
      statusPath: payload?.result?.statusPath || payload?.result?.job?.statusPath || null,
      customerAlreadyNotifiedByTool: true,
      customerMessageSent: Boolean(customerMessage),
      agentShouldReplyToFeishu: false,
      silentFallback: "HEARTBEAT_OK",
      bannedVisibleReplies: ["NO_REPLY", "contact admin", "restart Gateway", "Not connected", "route timed out", "路由超时"],
      bannedFallbackTools: nextVideoJobStarted
        ? ["douyin_next_video_plan_from_feishu_bitable"]
        : (marketingLongRunning || marketingVideoJobStarted || onboardingJobStarted || personaJobStarted ? ["douyin_marketing_controller", "douyin_xiaoice_video_produce", "douyin_digital_human_training", "douyin_persona_flow"] : []),
      agentInstruction,
    }, null, 2),
  ];
  if (!payload) lines.push(String(output || '').slice(-2000));
  return lines.join('\n');
}

function isUpstreamPublishText(text) {
  const raw = String(text || '').trim();
  if (hasMarketingVideoRejectIntent(raw)) return false;
  return Boolean(
    raw
    && /视频地址|videoUrl/.test(raw)
    && /标题|title/.test(raw)
  );
}

function hasMarketingVideoRejectIntent(text) {
  const lines = String(text || '')
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .filter((line) => !/^回复[：:]/.test(line))
    .filter((line) => !/^回复【?确认发布/.test(line))
    .filter((line) => !/^老板，您的视频制作完成/.test(line))
    .filter((line) => !/^视频标题[：:]/.test(line))
    .filter((line) => !/^视频描述[：:]/.test(line))
    .filter((line) => !/^视频标签[：:]/.test(line))
    .filter((line) => !/^视频地址[：:]/.test(line))
    .filter((line) => !/^封面地址[：:]/.test(line))
    .filter((line) => !/^["“]?(tags|标题|视频地址|封面图片|videoUrl|title|coverImageUrl)["”]?\s*[:：]/i.test(line));
  const actionableText = lines.join('\n');
  return /(?:不通过|不满意|需要修改|请修改|修改意见|重新生成|重做|重新成片|不要发布|先别发布)/.test(actionableText);
}

function marketingPendingReviewExists() {
  const state = readJsonFileSafe(MARKETING_STATE_PATH, null);
  return Boolean(state?.pendingReview?.publishText || state?.pendingReview?.videoUrl);
}

function normalizeFeishuTarget(value) {
  if (typeof value !== "string") return "";
  return value.trim();
}

function extractOpenClawFeishuEnvelope(rawText) {
  const raw = String(rawText || "");
  const messageId = raw.match(/"message_id"\s*:\s*"([^"]+)"/)?.[1]
    || raw.match(/\[message_id:\s*([^\]\s]+)\]/)?.[1]
    || "";
  const chatId = raw.match(/"conversation_label"\s*:\s*"([^"]+)"/)?.[1]
    || raw.match(/"chat_id"\s*:\s*"([^"]+)"/)?.[1]
    || raw.match(/"group_subject"\s*:\s*"([^"]+)"/)?.[1]
    || "";
  const payload = raw.match(/\[message_id:\s*[^\]]+\]\s*\n[^\n:]+:\s*([\s\S]*?)(?:\n\n\[System:|$)/)?.[1]?.trim()
    || "";
  return { messageId, chatId, text: payload };
}

function textFromOpenClawMessage(entry) {
  const content = entry?.message?.content;
  if (!Array.isArray(content)) return "";
  return content
    .filter((item) => item?.type === "text" && typeof item.text === "string")
    .map((item) => item.text)
    .join("\n")
    .trim();
}

function messageTimestampMs(entry) {
  const fromMessage = Number(entry?.message?.timestamp || 0);
  if (Number.isFinite(fromMessage) && fromMessage > 0) return fromMessage;
  const fromEntry = Date.parse(entry?.timestamp || "");
  return Number.isFinite(fromEntry) ? fromEntry : 0;
}

function normalizeForLooseMatch(value) {
  return String(value || "")
    .replace(/\s+/g, "")
    .replace(/[，：]/g, (ch) => (ch === "，" ? "," : ":"))
    .trim();
}

function feishuSourceTextMatches(sourceText, routedText) {
  const source = String(sourceText || "").trim();
  const routed = String(routedText || "").trim();
  if (!source || !routed) return false;
  if (source === routed) return true;
  if (isUpstreamPublishText(source) && isUpstreamPublishText(routed)) return true;
  const compactSource = normalizeForLooseMatch(source);
  const compactRouted = normalizeForLooseMatch(routed);
  if (!compactSource || !compactRouted) return false;
  if (compactSource === compactRouted) return true;
  if (compactRouted.length <= 40 && compactSource.includes(compactRouted)) return true;
  return compactSource.length <= 40 && compactRouted.includes(compactSource);
}

function looksLikePersonaFieldText(text) {
  return /姓名\/昵称|本人照片链接|主营业务|核心业务|目标客户|精准受众|IP核心诉求|禁忌与偏好|从业年限|核心优势/.test(String(text || ""));
}

function shouldPreferInferredFeishuText(routedText, inferredText) {
  const routed = String(routedText || "").trim();
  const inferred = String(inferredText || "").trim();
  if (!routed || !inferred || routed === inferred) return false;
  if (isUpstreamPublishText(inferred) && !isUpstreamPublishText(routed)) return true;
  if (looksLikePersonaFieldText(inferred) && !looksLikePersonaFieldText(routed)) return true;
  const compactRouted = normalizeForLooseMatch(routed);
  const compactInferred = normalizeForLooseMatch(inferred);
  if (!compactRouted || !compactInferred) return false;
  if (compactRouted.length <= 60 && compactInferred.length >= compactRouted.length * 2) return true;
  if (/确认人设|人设|资料|信息|总结|概括|已收到/.test(routed) && compactInferred.length > compactRouted.length) return true;
  return false;
}

function recentOpenClawSessionFiles() {
  if (!existsSync(OPENCLAW_SESSION_DIR)) return [];
  return readdirSync(OPENCLAW_SESSION_DIR)
    .filter((name) => name.endsWith(".jsonl"))
    .map((name) => {
      const path = join(OPENCLAW_SESSION_DIR, name);
      let mtimeMs = 0;
      try {
        mtimeMs = statSync(path).mtimeMs;
      } catch {
        // Ignore files that disappear while OpenClaw rotates sessions.
      }
      return { path, mtimeMs };
    })
    .filter((item) => item.mtimeMs > 0)
    .sort((a, b) => b.mtimeMs - a.mtimeMs)
    .slice(0, 8);
}

function inferFeishuSourceFromOpenClawSessions(routedText) {
  const now = Date.now();
  let newestRecent = null;
  let bestMatched = null;
  for (const file of recentOpenClawSessionFiles()) {
    let lines = [];
    try {
      lines = readFileSync(file.path, "utf8").trim().split(/\n+/).slice(-300);
    } catch {
      continue;
    }
    for (let i = lines.length - 1; i >= 0; i -= 1) {
      let entry;
      try {
        entry = JSON.parse(lines[i]);
      } catch {
        continue;
      }
      if (entry?.type !== "message" || entry?.message?.role !== "user") continue;
      const raw = textFromOpenClawMessage(entry);
      if (!raw.includes("Conversation info") && !raw.includes("[message_id:")) continue;
      const envelope = extractOpenClawFeishuEnvelope(raw);
      if (!envelope.messageId && !envelope.chatId) continue;
      const ageMs = now - messageTimestampMs(entry);
      if (!Number.isFinite(ageMs) || ageMs < 0 || ageMs > FEISHU_SOURCE_MAX_AGE_MS) continue;
      const candidate = {
        messageId: envelope.messageId,
        chatId: envelope.chatId,
        text: envelope.text,
        source: "openclaw-session-log",
        ageMs,
      };
      if (!newestRecent || candidate.ageMs < newestRecent.ageMs) newestRecent = candidate;
      if (feishuSourceTextMatches(envelope.text, routedText)
        && (!bestMatched || candidate.ageMs < bestMatched.ageMs)) {
        bestMatched = {
          ...candidate,
          source: "openclaw-session-log-match",
        };
      }
    }
  }
  if (bestMatched) return bestMatched;
  return newestRecent && newestRecent.ageMs <= 60 * 1000 ? newestRecent : null;
}

function resolveFeishuRouteSource(text, { messageId, chatId, receiveId, receiveIdType } = {}) {
  const envelope = extractOpenClawFeishuEnvelope(text);
  const routedText = envelope.text || String(text || "").trim();
  const explicitTarget = normalizeFeishuTarget(receiveId || chatId || envelope.chatId);
  const explicitMessageId = normalizeFeishuTarget(messageId || envelope.messageId);
  const inferred = (!explicitTarget && !explicitMessageId)
    ? inferFeishuSourceFromOpenClawSessions(routedText)
    : null;
  const useInferredText = !envelope.text && shouldPreferInferredFeishuText(routedText, inferred?.text);
  const target = explicitTarget || normalizeFeishuTarget(inferred?.chatId);
  return {
    text: useInferredText ? inferred.text : routedText,
    messageId: explicitMessageId || normalizeFeishuTarget(inferred?.messageId),
    receiveId: target,
    receiveIdType: receiveIdType || (target ? "chat_id" : undefined),
    source: explicitTarget || explicitMessageId
      ? "tool-args-or-envelope"
      : (useInferredText ? `${inferred.source}-restored-text` : inferred?.source || "default"),
  };
}

function startUpstreamPublishJob(text, notify = true, feishuTarget = null, sourceMessageId = null) {
  mkdirSync(PUBLISH_JOB_DIR, { recursive: true });
  const jobId = makeJobId("upstream");
  const inputPath = join(PUBLISH_JOB_DIR, `${jobId}.txt`);
  const taskPath = join(PUBLISH_JOB_DIR, `${jobId}.task.json`);
  const statusPath = join(PUBLISH_JOB_DIR, `${jobId}.status.json`);
  writeFileSync(inputPath, String(text || "").trim());
  writeFileSync(statusPath, `${JSON.stringify({
    ok: true,
    jobId,
    status: "queued",
    stage: "queued",
    inputPath,
    taskPath,
    notify: Boolean(notify),
    feishuTarget: feishuTarget?.receiveId ? {
      receiveId: feishuTarget.receiveId,
      receiveIdType: feishuTarget.receiveIdType || "chat_id",
    } : null,
    sourceMessageId: sourceMessageId || null,
    createdAt: new Date().toISOString(),
  }, null, 2)}\n`);

  const runner = startBackgroundNodeJob({
    scriptPath: join(__dirname, "..", "scripts", "publish-upstream-job-worker.js"),
    args: ["--job", statusPath],
    cwd: join(__dirname, ".."),
    unitName: `douyin-publish-upstream-${jobId}`,
    description: `Douyin upstream publish ${jobId}`,
    runtimeMaxSec: 3600,
  });
  const current = readJsonFile(statusPath);
  writeFileSync(statusPath, `${JSON.stringify({
    ...current,
    runner,
    updatedAt: new Date().toISOString(),
  }, null, 2)}\n`);

  return { jobId, inputPath, taskPath, statusPath };
}

const server = new McpServer({
  name: "douyin-upload-mcp-server",
  version: "0.1.0",
});

// ─── 页面探测 ───

server.registerTool(
  "douyin_feishu_route_text",
  {
    description: "OpenClaw 飞书单入口路由。收到飞书客户原文时必须实际调用这个工具，不能只说明计划；工具返回后按 agentInstruction 行动。不要自己拆分流程，不要用 browser/exec。支持：发布抖音、发送二维码、已登录/已完成、6位验证码、发送验证码/重发验证码、发布视频、更新数据/数据更新、数据报告、生成下一条视频、自动回复、定时任务、字段化发布文本、自动化营销、人设确认、数字人训练、生成视频方案、确认方案、确认发布。生成下一条视频会启动后台 job，由工具最终只给飞书发一次方案；自动化营销的长耗时步骤已有本地防重状态，超时后只能再次通过本工具查询“自动化营销状态”，不得改调 douyin_marketing_controller、douyin_xiaoice_video_produce、douyin_digital_human_training 或 douyin_persona_flow。工具会复用同一套登录/二维码/短信/发布/通知状态机；未命中时会给客户发送简短使用说明。若返回 customerAlreadyNotifiedByTool=true，不要额外发可见 Feishu 消息，尤其不要输出 NO_REPLY。",
    inputSchema: {
      text: z.string().describe("飞书客户消息原文。6位验证码也直接传原文"),
      reset: z.boolean().default(false).describe("仅测试时使用：清除当前技能会话状态"),
      dryRun: z.boolean().default(false).describe("仅测试时使用：不真实发送飞书消息"),
      messageId: z.string().optional().describe("可选：真实飞书 message_id，便于日志关联"),
      chatId: z.string().optional().describe("可选：当前飞书 chat_id。群聊/私聊自适应通知时传入；通常取消息元数据 conversation_label"),
      receiveId: z.string().optional().describe("可选：显式飞书接收目标，优先级同 chatId"),
      receiveIdType: z.string().optional().describe("可选：receive_id_type，默认 chat_id"),
    },
  },
  async ({ text, reset, dryRun, messageId, chatId, receiveId, receiveIdType }) => {
    const routeSource = resolveFeishuRouteSource(text, { messageId, chatId, receiveId, receiveIdType });
    if (!reset && !dryRun && isUpstreamPublishText(routeSource.text) && !marketingPendingReviewExists()) {
      try {
        const job = startUpstreamPublishJob(routeSource.text, true, routeSource.receiveId ? {
          receiveId: routeSource.receiveId,
          receiveIdType: routeSource.receiveIdType || "chat_id",
        } : null, routeSource.messageId || null);
        return {
          content: [{
            type: "text",
            text: JSON.stringify({
              ok: true,
              routed: true,
              action: "publish_from_upstream_text_job_started",
              ...job,
              customerAlreadyNotifiedByTool: true,
              agentInstruction: "后台发布 job 已启动，结束后会通知飞书。不要重复发起发布，不要发送可见 Feishu 回复，不要输出 NO_REPLY；如果运行时必须输出，输出 HEARTBEAT_OK。需要状态时调用 douyin_publish_job_status。",
            }, null, 2),
          }],
        };
      } catch (err) {
        return { content: [{ type: "text", text: `启动发布 job 失败: ${err.message}` }], isError: true };
      }
    }
    const script = join(__dirname, '..', 'scripts', 'feishu-reply-watcher.js');
    const args = [script, 'route-text', '--text', routeSource.text];
    if (reset) args.push('--reset');
    if (dryRun) args.push('--dry-run');
    if (routeSource.messageId) args.push('--message-id', routeSource.messageId);
    if (routeSource.receiveId) args.push('--receive-id', routeSource.receiveId);
    if (routeSource.receiveIdType) args.push('--receive-id-type', routeSource.receiveIdType);
    const result = spawnSync(process.execPath, args, {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: FEISHU_ROUTE_TIMEOUT_MS,
    });
    const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
    return {
      content: [{ type: "text", text: routeInstruction(output || `feishu route exited with status ${result.status}`) }],
      isError: result.status !== 0,
    };
  }
);

server.registerTool(
  "douyin_probe",
  {
    description: "探测抖音创作者平台页面各元素状态，用于调试和排查问题",
    inputSchema: {},
  },
  async () => {
    try {
      const { ops } = await createDouyinSession();
      const result = await ops.probe();
      disconnect();

      return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `执行崩溃: ${err.message}` }], isError: true };
    }
  }
);

server.registerTool(
  "douyin_persona_flow",
  {
    description: "人设定位兼容入口。飞书用户原文应优先走 douyin_feishu_route_text；若模型误调本工具，默认也会转交飞书单入口并异步生成人设，避免 MCP 超时。只有本地调试才传 direct=true。",
    inputSchema: {
      text: z.string().default("人设状态").describe("用户原文，例如 生成人设、确认人设，或包含姓名/主营业务/目标客户等字段的文本"),
      reset: z.boolean().default(false).describe("仅测试使用：清除人设状态"),
      dryRun: z.boolean().default(false).describe("仅测试使用：转交飞书单入口但不真实发送飞书消息"),
      direct: z.boolean().default(false).describe("仅本地调试使用：true 时绕过飞书单入口，直接同步运行 persona-flow.js；真实飞书流程不要使用"),
    },
  },
  async ({ text, reset, dryRun, direct }) => {
    if (!direct) {
      const routeSource = resolveFeishuRouteSource(text);
      const script = join(__dirname, '..', 'scripts', 'feishu-reply-watcher.js');
      const args = [script, 'route-text', '--text', routeSource.text || text || '人设状态'];
      if (reset) args.push('--reset');
      if (dryRun) args.push('--dry-run');
      if (routeSource.messageId) args.push('--message-id', routeSource.messageId);
      if (routeSource.receiveId) args.push('--receive-id', routeSource.receiveId);
      if (routeSource.receiveIdType) args.push('--receive-id-type', routeSource.receiveIdType);
      const result = spawnSync(process.execPath, args, {
        cwd: join(__dirname, '..'),
        encoding: 'utf8',
        stdio: ['ignore', 'pipe', 'pipe'],
        timeout: 180000,
      });
      const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
      return {
        content: [{ type: "text", text: routeInstruction(output || `feishu route exited with status ${result.status}`) }],
        isError: result.status !== 0,
      };
    }
    const script = join(__dirname, '..', 'scripts', 'persona-flow.js');
    const args = [script, 'route-text', '--text', text || '人设状态'];
    if (reset) args.push('--reset');
    const result = spawnSync(process.execPath, args, {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: 120000,
    });
    const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
    return {
      content: [{ type: "text", text: output || `persona-flow exited with status ${result.status}` }],
      isError: result.status !== 0,
    };
  }
);

server.registerTool(
  "douyin_marketing_controller",
  {
    description: "数字人自动化营销总控。支持自动化营销状态、开启/关闭、训练或绑定数字人ID、生成数字人视频、确认发布、不满意重做、生成并发布、每日自动化营销。飞书用户原文仍优先走 douyin_feishu_route_text。",
    inputSchema: {
      text: z.string().default("自动化营销状态").describe("用户原文，例如 开启自动化营销、绑定数字人ID xxx、生成数字人视频、确认发布、不满意、生成并发布"),
      dryRun: z.boolean().default(false).describe("测试模式：不真实发布，只验证编排"),
    },
  },
  async ({ text, dryRun }) => {
    const script = join(__dirname, '..', 'scripts', 'marketing-controller.js');
    const args = [script, 'route-text', '--text', text || '自动化营销状态'];
    if (dryRun) args.push('--dry-run');
    const result = spawnSync(process.execPath, args, {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: dryRun ? 240000 : 1200000,
    });
    const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
    return {
      content: [{ type: "text", text: output || `marketing-controller exited with status ${result.status}` }],
      isError: result.status !== 0,
    };
  }
);

server.registerTool(
  "douyin_digital_human_training",
  {
    description: "数字人形象训练/形象定制低层入口。接入小冰极速定制形象四接口：创建任务、查询质检、启动训练、查询训练结果；成功后绑定数字人ID。飞书用户原文仍优先走 douyin_feishu_route_text 或 douyin_marketing_controller。",
    inputSchema: {
      text: z.string().default("形象状态").describe("用户原文，例如 形象状态、训练数字人、形象定制"),
      dryRun: z.boolean().default(false).describe("测试模式：只验证配置和状态"),
    },
  },
  async ({ text, dryRun }) => {
    const script = join(__dirname, '..', 'scripts', 'digital-human-training.js');
    const args = [script, 'route-text', '--text', text || '形象状态'];
    if (dryRun) args.push('--dry-run');
    const result = spawnSync(process.execPath, args, {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: dryRun ? 240000 : DIGITAL_HUMAN_ROUTE_TIMEOUT_MS,
    });
    const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
    return {
      content: [{ type: "text", text: output || `digital-human-training exited with status ${result.status}` }],
      isError: result.status !== 0,
    };
  }
);

server.registerTool(
  "douyin_xiaoice_video_produce",
  {
    description: "一键成片桥接。调用本机 XiaoIce video-task-service 创建/查询数字人视频任务，并输出可交给抖音发布的字段化文本。禁止在飞书自动营销用户消息中直接调用；即使 douyin_feishu_route_text 或 douyin_marketing_controller 超时，也只能通过 douyin_feishu_route_text({text:\"自动化营销状态\"}) 查询状态，不能用本工具补跑，否则会重复生成视频。",
    inputSchema: {
      action: z.enum(["health", "create", "get", "wait", "create-and-wait"]).default("health"),
      title: z.string().optional().describe("视频标题"),
      scriptText: z.string().optional().describe("口播脚本"),
      tags: z.string().optional().describe("话题标签，例如 #宠物险#保险"),
      taskId: z.string().optional().describe("查询/等待任务 ID"),
      dryRun: z.boolean().default(false).describe("测试模式：不真实调用一键成片创建"),
      timeoutSec: z.number().default(900).describe("等待生成超时秒数"),
      allowDuplicate: z.boolean().default(false).describe("仅低层调试使用：允许在自动营销已有生成中/待确认视频时继续创建新成片任务"),
    },
  },
  async ({ action, title, scriptText, tags, taskId, dryRun, timeoutSec, allowDuplicate }) => {
    const normalizedAction = action || "health";
    if (!allowDuplicate && ["create", "create-and-wait"].includes(normalizedAction)) {
      const guard = existingMarketingVideoGuard();
      if (guard) {
        return {
          content: [{
            type: "text",
            text: JSON.stringify({
              ok: true,
              action: "xiaoice_video_blocked_by_marketing_pending",
              statePath: MARKETING_STATE_PATH,
              customerMessage: "自动化营销已有视频生成中或待确认视频，不再重复创建成片任务。请通过 douyin_feishu_route_text({text:\"自动化营销状态\"}) 查看进度。",
              ...guard,
            }, null, 2),
          }],
        };
      }
    }
    if (!allowDuplicate && ["get", "wait"].includes(normalizedAction)) {
      const guard = existingMarketingVideoGuard();
      const allowedTaskId = marketingLastGeneratedTaskId();
      if (guard && taskId && allowedTaskId && String(taskId).trim() !== allowedTaskId) {
        return {
          content: [{
            type: "text",
            text: JSON.stringify({
              ok: true,
              action: "xiaoice_video_stale_task_blocked_by_marketing_pending",
              statePath: MARKETING_STATE_PATH,
              customerMessage: "这个一键成片任务不是当前自动化营销待确认视频，已拦截，避免把旧视频发给客户。请通过 douyin_feishu_route_text({text:\"自动化营销状态\"}) 查看当前有效视频。",
              requestedTaskId: String(taskId).trim(),
              currentMarketingTaskId: allowedTaskId,
              ...guard,
            }, null, 2),
          }],
        };
      }
    }
    const script = join(__dirname, '..', 'scripts', 'xiaoice-video-produce.js');
    const args = [script, action || 'health'];
    if (title) args.push('--title', title);
    if (scriptText) args.push('--script-text', scriptText);
    if (tags) args.push('--tags', tags);
    if (taskId) args.push('--task-id', taskId);
    if (dryRun) args.push('--dry-run');
    if (timeoutSec) args.push('--timeout-sec', String(timeoutSec));
    const result = spawnSync(process.execPath, args, {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: Math.max(120000, Number(timeoutSec || 900) * 1000 + 60000),
    });
    const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
    return {
      content: [{ type: "text", text: output || `xiaoice-video-produce exited with status ${result.status}` }],
      isError: result.status !== 0,
    };
  }
);

// ─── 登录检查 ───

server.registerTool(
  "douyin_check_login",
  {
    description: "检查当前抖音创作者平台是否已登录，并推进登录流程。支持多次调用：qrcode（需扫码）→ sms_verification（自动点击接收短信）→ sms_code_input（需传入验证码）→ 带 smsCode 调用完成验证 → logged_in。飞书用户说“已登录/已完成”不能直接相信，必须以本工具或 douyin_feishu_route_text 的结果为准；若仍是 qrcode，只能告诉客户仍未登录并继续扫码/重新取码。",
    inputSchema: {
      smsCode: z.string().optional().describe("短信验证码（6位数字）。在 phase 为 sms_code_input 时传入"),
    },
  },
  async ({ smsCode }) => {
    try {
      const { ops } = await createDouyinSession();
      const result = await ops.checkLogin({ smsCode });
      disconnect();

      if (!result.ok) {
        const msg = result.message || result.error || '未知错误';
        return { content: [{ type: "text", text: `检测失败: ${msg}` }], isError: true };
      }

      const lines = [];

      switch (result.phase) {
        case 'logged_in':
          lines.push('✅ 已登录');
          break;
        case 'qrcode':
          lines.push('❌ 未登录 — 需要扫码');
          if (result.qrcodePath) lines.push(`状态检查截图路径: ${result.qrcodePath}`);
          lines.push('不要直接发送此路径给客户；客户准备扫码后必须调用 douyin_fresh_qr 获取刷新后的二维码');
          lines.push('AGENT_INSTRUCTION: 如果这是客户回复“已登录/已完成”后触发的检查，不要判断为登录成功；请只回复客户：仍未登录，请用手机抖音 App 扫码并确认。二维码过期请回复：发送二维码。');
          break;
        case 'sms_verification':
          lines.push('⏳ 身份验证中');
          lines.push(result.message);
          break;
        case 'sms_code_input':
          lines.push('📱 等待输入验证码');
          lines.push(result.message);
          break;
        case 'sms_code_submitted':
          lines.push('⏳ 验证码已提交，等待验证结果');
          lines.push(result.message);
          break;
        default:
          lines.push(result.message || JSON.stringify(result));
      }

      return {
        content: [{ type: "text", text: lines.join('\n') }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `执行崩溃: ${err.message}` }], isError: true };
    }
  }
);

// ─── 最新二维码 ───

server.registerTool(
  "douyin_fresh_qr",
  {
    description: "刷新抖音创作者中心登录页并获取最新可扫码二维码。飞书 DM 完整流程不要直接调用本工具，必须调用 douyin_feishu_route_text({text:\"发送二维码\"}) 让状态机统一处理。只有非飞书调试，或客户明确已在电脑端打开飞书并准备用手机抖音扫码时，才允许 customerReady=true 且 send=true 发送二维码；否则只发送准备提示。",
    inputSchema: {
      send: z.boolean().default(false).describe("是否发送到已配置的飞书客户会话"),
      customerReady: z.boolean().default(false).describe("客户是否已明确回复准备好：电脑端打开飞书，手机抖音 App 准备扫码。未确认时必须为 false"),
      maxQrAttempts: z.number().default(3).describe("刷新取码最大尝试次数，默认 3"),
    },
  },
  async ({ send, customerReady, maxQrAttempts }) => {
    const script = join(__dirname, '..', 'scripts', 'douyin-login-monitor.js');
    const args = [script, 'fresh-qr', '--max-qr-attempts', String(maxQrAttempts || 3)];
    if (send) args.push('--send');
    if (customerReady) args.push('--customer-ready');
    const result = spawnSync(process.execPath, args, {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
    if (result.status !== 0) {
      return { content: [{ type: "text", text: output || `fresh-qr failed with status ${result.status}` }], isError: true };
    }
    return { content: [{ type: "text", text: output }] };
  }
);

// ─── 页面导航 ───

server.registerTool(
  "douyin_navigate_to",
  {
    description: "打开指定的抖音页面 URL。仅允许 douyin.com 域名",
    inputSchema: {
      url: z.string().url().describe("目标抖音 URL"),
      timeout: z.number().default(30000).describe("等待页面加载完成的超时（毫秒），默认 30000"),
    },
  },
  async ({ url, timeout }) => {
    try {
      const { ops } = await createDouyinSession();
      const result = await ops.navigateTo(url, { timeout });
      disconnect();

      if (!result.ok) {
        let msg = `页面导航失败: ${result.error}`;
        if (result.detail) msg += `\n${result.detail}`;
        return { content: [{ type: "text", text: msg }], isError: true };
      }
      return {
        content: [{ type: "text", text: `已导航至: ${result.url}（耗时 ${result.elapsed}ms）` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `执行崩溃: ${err.message}` }], isError: true };
    }
  }
);

// ─── 页面刷新 ───

server.registerTool(
  "douyin_reload_page",
  {
    description: "刷新抖音页面（页面卡住或状态异常时使用）",
    inputSchema: {
      timeout: z.number().default(30000).describe("等待页面重新加载完成的超时（毫秒），默认 30000"),
    },
  },
  async ({ timeout }) => {
    try {
      const { ops } = await createDouyinSession();
      const result = await ops.reloadPage({ timeout });
      disconnect();

      if (!result.ok) {
        return { content: [{ type: "text", text: `页面刷新失败: ${result.error}` }], isError: true };
      }
      return { content: [{ type: "text", text: `页面刷新完成，耗时 ${result.elapsed}ms` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `执行崩溃: ${err.message}` }], isError: true };
    }
  }
);

// ─── 截图 ───

server.registerTool(
  "douyin_screenshot",
  {
    description: "对当前抖音页面进行截图，保存到本地文件。用于调试或查看页面当前状态",
    inputSchema: {},
  },
  async () => {
    try {
      const { writeFileSync, mkdirSync } = await import('node:fs');
      const { join } = await import('node:path');

      const { ops } = await createDouyinSession();

      mkdirSync(config.outputDir, { recursive: true });
      const filename = `douyin_screenshot_${Date.now()}.png`;
      const filePath = join(config.outputDir, filename);

      const buffer = await ops.screenshot({ fullPage: true });
      writeFileSync(filePath, buffer);

      disconnect();

      return {
        content: [{ type: "text", text: `截图已保存至: ${filePath}` }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `执行崩溃: ${err.message}` }], isError: true };
    }
  }
);

// ─── 浏览器信息 ───

server.registerTool(
  "douyin_browser_info",
  {
    description: "获取抖音浏览器会话的连接信息（CDP 端口、WebSocket 地址、Daemon 状态等）",
    inputSchema: {},
  },
  async () => {
    const daemonUrl = `http://127.0.0.1:${config.daemonPort}`;

    try {
      const healthRes = await fetch(`${daemonUrl}/health`, { signal: AbortSignal.timeout(3000) });
      const health = await healthRes.json();

      if (!health.ok) {
        return {
          content: [{ type: "text", text: "Daemon 未就绪，浏览器可能未启动。请先调用其他工具触发自动启动。" }],
          isError: true,
        };
      }

      const acquireRes = await fetch(`${daemonUrl}/browser/acquire`, { signal: AbortSignal.timeout(5000) });
      const acquire = await acquireRes.json();

      const info = {
        daemon: {
          url: daemonUrl,
          port: config.daemonPort,
          status: "running",
        },
        browser: {
          cdpPort: config.browserDebugPort,
          wsEndpoint: acquire.wsEndpoint || null,
          pid: acquire.pid || null,
          headless: config.browserHeadless,
        },
        config: {
          protocolTimeout: config.browserProtocolTimeout,
          outputDir: config.outputDir,
          daemonTTL: config.daemonTTL,
          douyinUrl: config.douyinUrl,
        },
      };

      return {
        content: [{ type: "text", text: JSON.stringify(info, null, 2) }],
      };
    } catch (err) {
      return {
        content: [{
          type: "text",
          text: `无法连接 Daemon (${daemonUrl})，浏览器可能未启动。\n错误: ${err.message}\n\n提示: 请先调用其他工具触发自动启动，或手动运行 npm run daemon`,
        }],
        isError: true,
      };
    }
  }
);

// ─── 发布视频 ───

server.registerTool(
  "douyin_publish_video",
  {
    description: "低层同步发布视频到抖音创作者平台。仅用于非飞书调试或本地绝对路径视频；飞书 DM 流程必须用 douyin_feishu_route_text，字段化文本优先用 douyin_publish_from_upstream_text 异步 job，避免 MCP 超时误报。自动完成：登录检查 → 切换到上传页 → fresh 上传视频文件 → 等待上传完成 → 优先上传自定义封面（coverImagePath/coverImageUrl），无封面才使用 AI 推荐封面 → 填写标题和简介 → 点击发布。",
    inputSchema: {
      filePath: z.string().describe("视频文件的绝对路径"),
      title: z.string().optional().describe("作品标题（可选）"),
      description: z.string().optional().describe("作品简介（可选）"),
      topics: z.union([z.string(), z.array(z.string())]).optional().describe("话题/tag 列表。会通过编辑页“#添加话题”生成真实话题节点"),
      coverImagePath: z.string().optional().describe("自定义封面图片绝对路径（可选）。字段“封面图片”应先下载到这里"),
      coverImageUrl: z.string().optional().describe("自定义封面图片 URL（可选）。传入后工具会先下载再上传为封面"),
      timeout: z.number().optional().default(300000).describe("视频上传超时（毫秒），默认 300000（5分钟）"),
    },
  },
  async ({ filePath, title, description, topics, coverImagePath, coverImageUrl, timeout }) => {
    try {
      const { ops } = await createDouyinSession();

      // 先检查登录状态
      const login = await ops.checkLogin();
      if (!login.loggedIn) {
        disconnect();
        const script = join(__dirname, '..', 'scripts', 'douyin-login-monitor.js');
        const notify = spawnSync(process.execPath, [script, 'check', '--notify', '--send-qr', 'ask'], {
          cwd: join(__dirname, '..'),
          encoding: 'utf8',
          stdio: ['ignore', 'pipe', 'pipe'],
        });
        const detail = `${notify.stderr || ''}${notify.stdout || ''}`.trim();
        return {
          content: [{
            type: "text",
            text: `未登录（phase: ${login.phase}），已尝试通过飞书提醒客户。客户回复准备扫码后调用 douyin_fresh_qr(send=true)。\n${detail}`,
          }],
          isError: true,
        };
      }

      const resolvedCoverImagePath = coverImagePath || (coverImageUrl
        ? await downloadToMcpCache(coverImageUrl, "cover", ".png")
        : null);
      const result = await ops.publishVideo(filePath, {
        title,
        description,
        topics,
        coverImagePath: resolvedCoverImagePath,
        freshUpload: true,
        timeout,
      });
      disconnect();

      if (!result.ok) {
        let msg = `视频发布失败: ${result.error}`;
        if (result.detail) msg += `\n详情: ${result.detail}`;
        return { content: [{ type: "text", text: msg }], isError: true };
      }

      const lines = [
        '✅ 视频发布成功',
        `文件: ${result.file}`,
        resolvedCoverImagePath ? `封面: ${resolvedCoverImagePath}` : '封面: AI 推荐封面',
        `上传耗时: ${result.elapsed}ms`,
      ];
      return { content: [{ type: "text", text: lines.join('\n') }] };
    } catch (err) {
      return { content: [{ type: "text", text: `执行崩溃: ${err.message}` }], isError: true };
    }
  }
);

server.registerTool(
  "douyin_publish_from_upstream_text",
  {
    description: "从字段化文本异步发布抖音视频。会解析“视频地址/封面图片/标题/tags”，下载视频和封面，优先使用自定义封面，并在后台持续发布和验证，避免 MCP 长请求超时。飞书 DM 正常流程仍必须优先用 douyin_feishu_route_text。",
    inputSchema: {
      text: z.string().describe("字段化文本，包含 视频地址、封面图片、标题、tags"),
      notify: z.boolean().default(false).describe("是否在后台 job 结束后主动通知飞书。OpenClaw 飞书模式若误用此低层工具，也必须传 true 兜底发布完成通知。"),
    },
  },
  async ({ text, notify }) => {
    try {
      const job = startUpstreamPublishJob(text, notify);

      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            ok: true,
            jobId: job.jobId,
            status: "started",
            statusPath: job.statusPath,
            next: notify
              ? "后台 job 会在发布结束后通知飞书；也可调用 douyin_publish_job_status 查询。不要重复发起发布。"
              : "调用 douyin_publish_job_status 查询，直到 status=succeeded 或 failed。不要重复发起发布。",
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: "text", text: `启动发布 job 失败: ${err.message}` }], isError: true };
    }
  }
);

server.registerTool(
  "douyin_publish_job_status",
  {
    description: "查询 douyin_publish_from_upstream_text 启动的异步发布 job 状态。",
    inputSchema: {
      jobId: z.string().describe("发布 job id"),
    },
  },
  async ({ jobId }) => {
    try {
      const statusPath = join(PUBLISH_JOB_DIR, `${jobId}.status.json`);
      if (!existsSync(statusPath)) {
        return { content: [{ type: "text", text: `未找到发布 job: ${jobId}` }], isError: true };
      }
      const status = readJsonFile(statusPath);
      return { content: [{ type: "text", text: JSON.stringify(status, null, 2) }], isError: status.status === "failed" };
    } catch (err) {
      return { content: [{ type: "text", text: `查询发布 job 失败: ${err.message}` }], isError: true };
    }
  }
);

// ─── 发布图文 ───

server.registerTool(
  "douyin_publish_imagetext",
  {
    description: "发布图文到抖音创作者平台。自动完成：登录检查 → 切换到上传页 → 上传图片 → 填写标题和简介 → 选择音乐 → 点击发布。",
    inputSchema: {
      filePaths: z.array(z.string()).describe("图片文件绝对路径数组（支持多张）"),
      title: z.string().optional().describe("作品标题（可选）"),
      description: z.string().optional().describe("作品简介（可选）"),
    },
  },
  async ({ filePaths, title, description }) => {
    try {
      const { ops } = await createDouyinSession();

      // 先检查登录状态
      const login = await ops.checkLogin();
      if (!login.loggedIn) {
        disconnect();
        const script = join(__dirname, '..', 'scripts', 'douyin-login-monitor.js');
        const notify = spawnSync(process.execPath, [script, 'check', '--notify', '--send-qr', 'ask'], {
          cwd: join(__dirname, '..'),
          encoding: 'utf8',
          stdio: ['ignore', 'pipe', 'pipe'],
        });
        const detail = `${notify.stderr || ''}${notify.stdout || ''}`.trim();
        return {
          content: [{
            type: "text",
            text: `未登录（phase: ${login.phase}），已尝试通过飞书提醒客户。客户回复准备扫码后调用 douyin_fresh_qr(send=true)。\n${detail}`,
          }],
          isError: true,
        };
      }

      const result = await ops.publishImageText(filePaths, { title, description });
      disconnect();

      if (!result.ok) {
        let msg = `图文发布失败: ${result.error}`;
        if (result.detail) msg += `\n详情: ${result.detail}`;
        return { content: [{ type: "text", text: msg }], isError: true };
      }

      const lines = [
        '✅ 图文发布成功',
        `图片数: ${result.count}`,
      ];
      return { content: [{ type: "text", text: lines.join('\n') }] };
    } catch (err) {
      return { content: [{ type: "text", text: `执行崩溃: ${err.message}` }], isError: true };
    }
  }
);

// ─── 数据分析 ───

server.registerTool(
  "douyin_data_analysis",
  {
    description: "兼容工具：先同步近 N 天数据到飞书多维表，再从多维表生成报告。飞书 DM 的“数据分析/数据报告”仍应优先调用 douyin_feishu_route_text；不要把本工具当成直连页面的采集入口。",
    inputSchema: {
      output: z.string().optional().describe("可选：报告 JSON 输出路径，必须是绝对路径"),
      days: z.number().optional().default(90).describe("统计最近 N 天作品明细，默认 90 天"),
    },
  },
  async ({ output, days }) => {
    const syncScript = join(__dirname, '..', 'scripts', 'sync-douyin-data-to-feishu-bitable.js');
    const reportScript = join(__dirname, '..', 'scripts', 'douyin-data-report-from-bitable.js');
    const syncResult = spawnSync(process.execPath, [syncScript, '--days', String(days || 90)], {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: 240000,
    });
    const syncText = `${syncResult.stderr || ''}${syncResult.stdout || ''}`.trim();
    const syncPayload = parseLastJsonObject(syncText);
    if (syncResult.status !== 0 || !syncPayload?.ok) {
      return {
        content: [{
          type: "text",
          text: syncText || `douyin_sync_data_to_feishu_bitable exited with status ${syncResult.status}`,
        }],
        isError: true,
      };
    }

    const reportResult = spawnSync(process.execPath, [reportScript, '--days', String(days || 90)], {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: 120000,
    });
    const reportText = `${reportResult.stderr || ''}${reportResult.stdout || ''}`.trim();
    const reportPayload = parseLastJsonObject(reportText);
    if (reportResult.status !== 0 || !reportPayload?.ok) {
      return {
        content: [{
          type: "text",
          text: reportText || `douyin_data_report_from_feishu_bitable exited with status ${reportResult.status}`,
        }],
        isError: true,
      };
    }

    const payload = {
      ok: true,
      source: 'feishu_bitable',
      days: Number(days || 90),
      sync: syncPayload,
      report: reportPayload,
    };
    if (output) {
      writeFileSync(output, `${JSON.stringify(payload, null, 2)}\n`);
      payload.output = output;
    }

    return {
      content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
    };
  }
);

server.registerTool(
  "douyin_sync_data_to_feishu_bitable",
  {
    description: "低层同步组件：采集抖音近期数据并同步到飞书多维表。默认近 90 天；会创建/复用“抖音作品明细、抖音账号日报、抖音数据同步日志”三张表。飞书 DM 的数据命令必须优先用 douyin_feishu_route_text。",
    inputSchema: {
      days: z.number().optional().default(90).describe("同步最近 N 天，建议 7/30/90/180，默认 90"),
      output: z.string().optional().describe("可选：数据分析 JSON 输出路径，必须是绝对路径"),
    },
  },
  async ({ days, output }) => {
    const script = join(__dirname, '..', 'scripts', 'sync-douyin-data-to-feishu-bitable.js');
    const args = [script, '--days', String(days || 90)];
    if (output) args.push('--output', output);
    const result = spawnSync(process.execPath, args, {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: 240000,
    });
    const text = `${result.stderr || ''}${result.stdout || ''}`.trim();
    return {
      content: [{ type: "text", text: text || `sync-douyin-data-to-feishu-bitable exited with status ${result.status}` }],
      isError: result.status !== 0,
    };
  }
);

server.registerTool(
  "douyin_data_report_from_feishu_bitable",
  {
    description: "低层报告组件：从已同步的飞书多维表读取抖音作品明细和账号日报，生成数据报告。飞书 DM 的“数据分析/数据报告”必须优先用 douyin_feishu_route_text，由入口先同步再报告。",
    inputSchema: {
      days: z.number().optional().default(90).describe("报告口径最近 N 天，默认 90"),
      notify: z.boolean().optional().default(false).describe("是否发送报告到已配置的飞书会话"),
    },
  },
  async ({ days, notify }) => {
    const script = join(__dirname, '..', 'scripts', 'douyin-data-report-from-bitable.js');
    const args = [script, '--days', String(days || 90)];
    if (notify) args.push('--notify');
    const result = spawnSync(process.execPath, args, {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: 120000,
    });
    const text = `${result.stderr || ''}${result.stdout || ''}`.trim();
    return {
      content: [{ type: "text", text: text || `douyin-data-report-from-bitable exited with status ${result.status}` }],
      isError: result.status !== 0,
    };
  }
);

server.registerTool(
  "douyin_next_video_plan_from_feishu_bitable",
  {
    description: "低层创作方案组件，仅用于非飞书调试或后台 job worker。从已同步的飞书多维表读取抖音数据，生成下一条视频的标题、封面文案、tags、口播脚本、画面建议和 digitalHumanInput。飞书 DM 的“生成下一条视频/内容方案”必须调用 douyin_feishu_route_text；即使路由等待或超时，agent 也不得改调本工具、不得把本工具 JSON 手动改写后发给飞书。",
    inputSchema: {
      days: z.number().optional().default(90).describe("参考最近 N 天数据，默认 90"),
      notify: z.boolean().optional().default(false).describe("是否发送方案到已配置的飞书会话"),
      output: z.string().optional().describe("可选：方案 JSON 输出路径，必须是绝对路径"),
    },
  },
  async ({ days, notify, output }) => {
    const script = join(__dirname, '..', 'scripts', 'douyin-next-video-plan-from-bitable.js');
    const args = [script, '--days', String(days || 90)];
    if (notify) args.push('--notify');
    if (output) args.push('--output', output);
    const result = spawnSync(process.execPath, args, {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: 180000,
    });
    const text = `${result.stderr || ''}${result.stdout || ''}`.trim();
    return {
      content: [{ type: "text", text: text || `douyin-next-video-plan-from-bitable exited with status ${result.status}` }],
      isError: result.status !== 0,
    };
  }
);

// ─── 评论管理 ───

server.registerTool(
  "douyin_comment_list",
  {
    description: "读取抖音创作者中心评论管理页面，列出可见评论。只读操作。",
    inputSchema: {},
  },
  async () => {
    const script = join(__dirname, '..', 'scripts', 'douyin-comment-reply.js');
    const result = spawnSync(process.execPath, [script, 'list'], {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    const text = `${result.stderr || ''}${result.stdout || ''}`.trim();
    return {
      content: [{ type: "text", text: text || `douyin-comment-reply list exited with status ${result.status}` }],
      isError: result.status !== 0,
    };
  }
);

server.registerTool(
  "douyin_comment_reply",
  {
    description: "对第一条可见评论准备回复。默认 dry-run：填入后清空，不发送。只有明确允许真实回复时才 execute=true。",
    inputSchema: {
      text: z.string().describe("评论回复内容"),
      index: z.number().default(0).describe("目标评论序号，来自 douyin_comment_list，默认 0"),
      execute: z.boolean().default(false).describe("是否真实点击发送。默认 false，只做 dry-run"),
    },
  },
  async ({ text, index, execute }) => {
    const script = join(__dirname, '..', 'scripts', 'douyin-comment-reply.js');
    const args = [script, 'reply', '--text', text, '--index', String(index || 0)];
    if (execute) args.push('--execute');
    const result = spawnSync(process.execPath, args, {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    const out = `${result.stderr || ''}${result.stdout || ''}`.trim();
    return {
      content: [{ type: "text", text: out || `douyin-comment-reply reply exited with status ${result.status}` }],
      isError: result.status !== 0,
    };
  }
);

// ─── 私信管理 ───

server.registerTool(
  "douyin_dm_list",
  {
    description: "读取抖音创作者中心私信/会话页面，列出可见会话。只读操作。",
    inputSchema: {},
  },
  async () => {
    const script = join(__dirname, '..', 'scripts', 'douyin-dm-reply.js');
    const result = spawnSync(process.execPath, [script, 'list'], {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    const text = `${result.stderr || ''}${result.stdout || ''}`.trim();
    return {
      content: [{ type: "text", text: text || `douyin-dm-reply list exited with status ${result.status}` }],
      isError: result.status !== 0,
    };
  }
);

server.registerTool(
  "douyin_dm_reply",
  {
    description: "对第一条可见私信会话准备回复。默认 dry-run：填入后清空，不发送。只有明确允许真实回复时才 execute=true。",
    inputSchema: {
      text: z.string().describe("私信回复内容"),
      index: z.number().default(0).describe("目标会话序号，来自 douyin_dm_list，默认 0"),
      execute: z.boolean().default(false).describe("是否真实点击发送。默认 false，只做 dry-run"),
    },
  },
  async ({ text, index, execute }) => {
    const script = join(__dirname, '..', 'scripts', 'douyin-dm-reply.js');
    const args = [script, 'reply', '--text', text, '--index', String(index || 0)];
    if (execute) args.push('--execute');
    const result = spawnSync(process.execPath, args, {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    const textOut = `${result.stderr || ''}${result.stdout || ''}`.trim();
    return {
      content: [{ type: "text", text: textOut || `douyin-dm-reply reply exited with status ${result.status}` }],
      isError: result.status !== 0,
    };
  }
);

server.registerTool(
  "douyin_auto_reply",
  {
    description: "按评论/私信内容自动生成回复。默认 dry-run，只生成建议不发送；execute=true 才真实发送，并会验证回复可见。",
    inputSchema: {
      kind: z.enum(["comment", "dm", "both"]).default("both").describe("自动回复范围：comment 评论、dm 私信、both 两者"),
      limit: z.number().default(50).describe("本次每类最多处理多少条，默认 50，用于尽量处理所有未回复项"),
      maxScan: z.number().default(200).describe("本次每类最多扫描多少条可见记录，默认 200"),
      execute: z.boolean().default(false).describe("是否真实发送。默认 false，只生成建议"),
      force: z.boolean().default(false).describe("是否忽略已回复记录强制再次处理，默认 false"),
    },
  },
  async ({ kind, limit, maxScan, execute, force }) => {
    const script = join(__dirname, '..', 'scripts', 'douyin-auto-reply.js');
    const args = [script, kind || 'both', '--limit', String(limit || 50), '--max-scan', String(maxScan || 200)];
    if (execute) args.push('--execute');
    if (force) args.push('--force');
    const result = spawnSync(process.execPath, args, {
      cwd: join(__dirname, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: 240000,
    });
    const text = `${result.stderr || ''}${result.stdout || ''}`.trim();
    return {
      content: [{ type: "text", text: text || `douyin-auto-reply exited with status ${result.status}` }],
      isError: result.status !== 0,
    };
  }
);

// 启动
async function run() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Douyin MCP Server running on stdio");
}

run().catch(console.error);
