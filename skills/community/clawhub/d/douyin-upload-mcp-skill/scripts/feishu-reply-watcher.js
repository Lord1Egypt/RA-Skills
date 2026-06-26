#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, renameSync, statSync, writeFileSync } from 'node:fs';
import { basename, dirname, extname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import {
  downloadFeishuMessageResource,
  getFeishuMessage,
  listFeishuMessages,
  resolveFeishuConfig,
  sendFeishuImage,
  sendFeishuText,
  sendFeishuTextChunks,
} from './feishu-client.js';
import { startBackgroundNodeJob } from './background-job.js';

const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops');
const STATE_PATH = process.env.DOUYIN_FEISHU_WATCH_STATE || join(STATE_DIR, 'feishu-reply-watcher-state.json');
const UPLOAD_DIR = process.env.DOUYIN_FEISHU_UPLOAD_DIR || join(STATE_DIR, 'uploads');
const UPSTREAM_DIR = process.env.DOUYIN_FEISHU_UPSTREAM_DIR || join(STATE_DIR, 'upstream-tasks');
const PUBLISH_JOB_DIR = process.env.DOUYIN_PUBLISH_JOB_DIR || join(STATE_DIR, 'publish-jobs');
const NEXT_VIDEO_PLAN_JOB_DIR = process.env.DOUYIN_NEXT_VIDEO_PLAN_JOB_DIR || join(STATE_DIR, 'next-video-plan-jobs');
const MARKETING_VIDEO_JOB_DIR = process.env.DOUYIN_MARKETING_VIDEO_JOB_DIR || join(STATE_DIR, 'marketing-video-jobs');
const PERSONA_JOB_DIR = process.env.DOUYIN_PERSONA_JOB_DIR || join(STATE_DIR, 'persona-jobs');
const ONBOARDING_JOB_DIR = process.env.DOUYIN_ONBOARDING_JOB_DIR || join(STATE_DIR, 'onboarding-jobs');
const PERSONA_STATE_PATH = process.env.DOUYIN_PERSONA_STATE_PATH || join(STATE_DIR, 'persona-state.json');
const BOUND_FEISHU_TARGET_PATH = process.env.DOUYIN_FEISHU_BOUND_TARGET_PATH || join(STATE_DIR, 'feishu-bound-target.json');
const __dirname = dirname(fileURLToPath(import.meta.url));
const VIDEO_EXTENSIONS = new Set(['.mp4', '.mov', '.m4v', '.avi', '.webm', '.mkv']);
const SESSION_TTL_MS = 30 * 60 * 1000;
const LOGIN_QR_PREPARE_MESSAGE = '抖音需要重新登录。\n请在电脑端打开飞书，用手机抖音 App 准备扫码。\n准备好后回复：发送二维码';

function statePathEnv() {
  return {
    DOUYIN_MONITOR_STATE_DIR: STATE_DIR,
    DOUYIN_FEISHU_WATCH_STATE: STATE_PATH,
    DOUYIN_FEISHU_UPLOAD_DIR: UPLOAD_DIR,
    DOUYIN_FEISHU_UPSTREAM_DIR: UPSTREAM_DIR,
    DOUYIN_FEISHU_UPSTREAM_CACHE_DIR: join(STATE_DIR, 'upstream'),
    DOUYIN_PUBLISH_JOB_DIR: PUBLISH_JOB_DIR,
    DOUYIN_NEXT_VIDEO_PLAN_JOB_DIR: NEXT_VIDEO_PLAN_JOB_DIR,
    DOUYIN_MARKETING_VIDEO_JOB_DIR: MARKETING_VIDEO_JOB_DIR,
    DOUYIN_PERSONA_JOB_DIR: PERSONA_JOB_DIR,
    DOUYIN_ONBOARDING_JOB_DIR: ONBOARDING_JOB_DIR,
    DOUYIN_PERSONA_STATE_PATH: PERSONA_STATE_PATH,
    DOUYIN_MARKETING_STATE_PATH: process.env.DOUYIN_MARKETING_STATE_PATH || join(STATE_DIR, 'automation-marketing-state.json'),
    DOUYIN_DIGITAL_HUMAN_STATE_PATH: process.env.DOUYIN_DIGITAL_HUMAN_STATE_PATH || join(STATE_DIR, 'digital-human-state.json'),
  };
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) continue;
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
    } else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function loadState() {
  if (!existsSync(STATE_PATH)) return { seen: {}, lastCreateTime: 0, pendingVideo: null, flow: null };
  try {
    return { seen: {}, lastCreateTime: 0, pendingVideo: null, flow: null, ...JSON.parse(readFileSync(STATE_PATH, 'utf8')) };
  } catch {
    return { seen: {}, lastCreateTime: 0, pendingVideo: null, flow: null };
  }
}

function loadPersonaState() {
  try {
    if (!existsSync(PERSONA_STATE_PATH)) return null;
    return JSON.parse(readFileSync(PERSONA_STATE_PATH, 'utf8'));
  } catch {
    return null;
  }
}

function personaGeneralReply(text) {
  const persona = loadPersonaState();
  const confirmed = persona?.confirmed;
  if (!confirmed) return null;
  const fields = confirmed.fields || {};
  const summary = confirmed.summary || {};
  const identity = summary.coreIdentity || fields.bissiness || '当前人设';
  const audience = summary.audience || fields.segment || '目标客户';
  const tone = summary.tone || fields.trials || '专业、清晰、自然';
  const value = summary.value || fields.advantage || '提供可落地的建议';
  const raw = String(text || '').trim();
  if (!raw) return null;
  const answer = [
    `以“${identity}”的人设来回复：`,
    `这个问题可以围绕${audience}最关心的实际场景来讲，重点突出“${value}”。`,
    `建议表达保持${tone}，先给明确判断，再给1-2个具体行动建议。`,
  ].join('\n');
  return {
    action: 'persona_general_reply',
    customerMessage: answer,
  };
}

function personaCollectingActive() {
  const persona = loadPersonaState();
  return persona?.status === 'collecting';
}

function personaDraftPending() {
  const persona = loadPersonaState();
  return Boolean(persona?.draft && !persona?.confirmed);
}

function personaGenerationActive() {
  const persona = loadPersonaState();
  return persona?.status === 'generating';
}

function currentMarketingState() {
  try {
    const path = process.env.DOUYIN_MARKETING_STATE_PATH || join(STATE_DIR, 'automation-marketing-state.json');
    if (!existsSync(path)) return {};
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return {};
  }
}

function normalizePendingUpstreamTask(task) {
  if (!task || typeof task !== 'object') return null;
  const taskPath = String(task.taskPath || '').trim();
  if (!taskPath || !existsSync(taskPath)) return null;
  return {
    taskPath,
    inputPath: task.inputPath || null,
    title: task.title || '',
    videoPath: task.videoPath || null,
    coverImagePath: task.coverImagePath || null,
  };
}

function recoverPendingUpstreamTaskFromMarketingState(state) {
  const marketing = currentMarketingState();
  const lastRunStatus = String(marketing?.lastRun?.status || '').toLowerCase();
  const lastRunStage = String(marketing?.lastRun?.stage || '').toLowerCase();
  if (lastRunStatus === 'published' || lastRunStage === 'published_verified') return null;
  const candidates = [
    marketing?.lastRun?.publishPayload?.result?.pendingUpstreamTask,
    marketing?.lastRun?.publishPayload?.result?.task,
    marketing?.lastRun?.publishPayload?.pendingUpstreamTask,
    marketing?.lastRun?.pendingUpstreamTask,
  ];
  const task = candidates.map(normalizePendingUpstreamTask).find(Boolean);
  if (!task) return null;
  if (state) {
    state.pendingUpstreamTask = task;
    state.pendingPublish = {
      ...(state.pendingPublish || {}),
      title: task.title,
      taskPath: task.taskPath,
    };
  }
  return task;
}

function pendingUpstreamTask(state) {
  const existing = normalizePendingUpstreamTask(state?.pendingUpstreamTask);
  if (existing) return existing;
  return recoverPendingUpstreamTaskFromMarketingState(state);
}

function mergeExternalWatcherFlowState(state) {
  if (!state || !existsSync(STATE_PATH)) return null;
  let external;
  try {
    external = JSON.parse(readFileSync(STATE_PATH, 'utf8'));
  } catch {
    return null;
  }
  const hasExternalFlowState = Boolean(
    external?.flow?.active
    || external?.pendingUpstreamTask
    || external?.pendingPublish
    || external?.pendingVideo
    || external?.pendingCommand
  );
  if (!hasExternalFlowState) return null;
  if (external.flow?.active) state.flow = external.flow;
  if (external.pendingUpstreamTask) state.pendingUpstreamTask = external.pendingUpstreamTask;
  if (external.pendingPublish) state.pendingPublish = external.pendingPublish;
  if (external.pendingVideo) state.pendingVideo = external.pendingVideo;
  if (external.pendingCommand) state.pendingCommand = external.pendingCommand;
  if ('lastSmsCode' in external) state.lastSmsCode = external.lastSmsCode;
  if (external.notified && typeof external.notified === 'object') {
    state.notified = { ...(state.notified || {}), ...external.notified };
  }
  return external;
}

function personaFingerprintFromState(persona = loadPersonaState()) {
  const confirmed = persona?.confirmed || null;
  const fields = confirmed?.fields || persona?.fields || {};
  return {
    confirmed: Boolean(confirmed),
    confirmedAt: String(confirmed?.confirmedAt || '').trim(),
    name: String(fields.name || '').trim(),
    photo: String(fields.photo || fields.photoUrl || '').trim(),
  };
}

function resetGeneratedMarketingStateForPersona() {
  return saveMarketingStatePatch({
    digitalHuman: {},
    pendingPlan: null,
    pendingReview: null,
    inFlightPlan: null,
    inFlightVideo: null,
    lastGenerated: null,
    videoRevisionFeedback: '',
    lastVideoRevisionRequestedAt: '',
  });
}

function saveMarketingStatePatch(patch) {
  const path = process.env.DOUYIN_MARKETING_STATE_PATH || join(STATE_DIR, 'automation-marketing-state.json');
  const current = currentMarketingState();
  const next = { ...current, ...patch, updatedAt: new Date().toISOString() };
  mkdirSync(dirname(path), { recursive: true });
  const tempPath = `${path}.tmp-${process.pid}-${Date.now()}`;
  writeFileSync(tempPath, `${JSON.stringify(next, null, 2)}\n`);
  renameSync(tempPath, path);
  return next;
}

function marketingPendingPlan() {
  return Boolean(currentMarketingState()?.pendingPlan?.plan);
}

function marketingPendingVideoReview() {
  const state = currentMarketingState();
  return Boolean(state?.pendingReview?.publishText || state?.pendingReview?.videoUrl);
}

function automationMarketingStartText(text) {
  return /^(开启自动化营销|启动自动化营销|我要做自动化营销)$/.test(String(text || '').trim());
}

function shouldRouteAutomationStartToPersona(text) {
  if (!automationMarketingStartText(text)) return false;
  const persona = loadPersonaState();
  if (!persona?.confirmed) return true;
  return persona.status === 'collecting' || Boolean(persona.draft && !persona.confirmed);
}

function internalConfirmedMarketingPublish() {
  return process.env.DOUYIN_INTERNAL_CONFIRMED_MARKETING_PUBLISH === 'true';
}

function firstMeaningfulLine(text) {
  return String(text || '')
    .split(/\r?\n/)
    .map((line) => line.trim())
    .find(Boolean) || '';
}

function textBeforePublishFields(text) {
  return String(text || '')
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .filter((line) => !/^回复[：:]/.test(line))
    .filter((line) => !/^回复【?确认发布/.test(line))
    .filter((line) => !/^请按格式发送[：:]?/.test(line))
    .filter((line) => !/^老板，您的视频制作完成/.test(line))
    .filter((line) => !/^视频标题[：:]/.test(line))
    .filter((line) => !/^视频描述[：:]/.test(line))
    .filter((line) => !/^视频标签[：:]/.test(line))
    .filter((line) => !/^视频地址[：:]/.test(line))
    .filter((line) => !/^封面地址[：:]/.test(line))
    .filter((line) => !/^["“]?(tags|标题|视频地址|封面图片|videoUrl|title|coverImageUrl)["”]?\s*[:：]/i.test(line))
    .join('\n');
}

function isMarketingPublishConfirmText(text) {
  const raw = String(text || '').trim();
  const firstLine = firstMeaningfulLine(raw);
  if (isMarketingVideoRejectText(raw)) return false;
  return /^(确认发布|发布这个视频|确认发布视频|发布生成的视频)$/.test(firstLine)
    || /^(确认发布|发布这个视频|确认发布视频|发布生成的视频)(?:\s|$)/.test(raw)
    || /^回复\s*[:：]\s*【?确认发布】?$/.test(raw);
}

function isMarketingVideoRejectText(text) {
  const firstLine = firstMeaningfulLine(text);
  if (/^(不通过|不满意|重新生成视频|重做视频|重新成片)(?:[\s\S]*)$/.test(firstLine)) return true;
  return /(?:不通过|不满意|需要修改|请修改|修改意见|重新生成|重做|重新成片|不要发布|先别发布)/.test(textBeforePublishFields(text));
}

function isScheduleCommandText(text) {
  return /^(定时任务|查看定时任务|任务计划|查看任务|开启定时任务|启动定时任务|安装定时任务|创建定时任务|关闭定时任务|暂停定时任务|停用定时任务|恢复默认定时任务|重置定时任务|默认定时任务)$/.test(String(text || '').trim())
    || /^修改定时任务/.test(String(text || '').trim());
}

function marketingVideoRevisionFeedback(text) {
  return String(text || '')
    .trim()
    .replace(/^(不通过|不满意|重新生成视频|重做视频|重新成片)\s*[，,。:：-]?\s*/u, '')
    .trim();
}

function looksLikePersonaInfo(text) {
  const raw = String(text || '').trim();
  if (!raw) return false;
  if (/视频地址|视频链接|视频url|videoUrl|封面图片|封面链接|coverImageUrl|tags\s*[:：]|发布抖音|发送二维码|验证码|数据报告|数据报表|同步数据|自动回复|定时任务/.test(raw)) return false;
  let score = 0;
  if (/(?:我叫|我是|本人|昵称|名字)\s*[\u4e00-\u9fa5A-Za-z0-9_-]{1,12}/.test(raw)) score += 1;
  if (/(?:性别|男士|女士|从业|深耕|做了|经验|年限|入行)\s*[:：]?\s*\d{0,2}/.test(raw)) score += 1;
  if (/(?:主营业务|核心业务|业务|主要做|从事|经营|做)[^。！？!?；;]{1,40}/.test(raw)) score += 1;
  if (/(?:目标客户|精准受众|受众|客户|人群|养猫|养狗|家庭|用户)/.test(raw)) score += 1;
  if (/(?:核心优势|优势|擅长|比较会|最会|强项|讲清楚|理赔坑|条款)/.test(raw)) score += 1;
  if (/(?:抖音|视频号|小红书|IP|账号|人设|获客|咨询|转化|建立信任)/i.test(raw)) score += 1;
  if (/(?:禁忌|偏好|不要|不能|避免|不夸大|不承诺|合规)/.test(raw)) score += 1;
  return score >= 2;
}

function normalizeIncomingText(text) {
  const raw = String(text || '').trim();
  if (!raw) return raw;
  const exact = new Map([
    ['发布', '发布抖音'],
    ['我要发布', '发布抖音'],
    ['开始发布', '发布抖音'],
    ['发抖音', '发布抖音'],
    ['上传抖音', '发布抖音'],
    ['同步数据', '更新数据'],
    ['刷新数据', '更新数据'],
    ['拉取数据', '更新数据'],
    ['获取数据', '更新数据'],
    ['数据报表', '数据报告'],
    ['查看报表', '数据报告'],
    ['分析报告', '数据报告'],
    ['内容分析', '数据报告'],
    ['生成选题', '生成下一条视频'],
    ['下一条选题', '生成下一条视频'],
    ['生成下一条', '生成下一条视频'],
    ['下一条内容方案', '生成下一条视频'],
    ['回复互动', '自动回复'],
    ['处理消息', '自动回复'],
    ['回复消息', '自动回复'],
    ['查看任务计划', '定时任务'],
    ['任务状态', '定时任务'],
    ['定时设置', '定时任务'],
    ['账号定位', '生成人设'],
    ['做人设', '生成人设'],
    ['生成定位', '生成人设'],
    ['开始营销', '开启自动化营销'],
    ['开启营销', '开启自动化营销'],
    ['启动营销', '开启自动化营销'],
    ['开通自动化营销', '开启自动化营销'],
    ['开启自动营销', '开启自动化营销'],
    ['启动自动营销', '开启自动化营销'],
    ['我要做自动化营销', '开启自动化营销'],
    ['停止营销', '关闭自动化营销'],
    ['关闭营销', '关闭自动化营销'],
    ['停止自动化营销', '关闭自动化营销'],
    ['开启自动发布', '开启自动确认'],
    ['自动发布模式', '开启自动确认'],
    ['关闭自动发布', '关闭自动确认'],
    ['人工审核', '关闭自动确认'],
    ['查看数字人', '查看形象'],
  ]);
  if (exact.has(raw)) return exact.get(raw);
  return raw
    .replace(/^(同步|刷新|拉取|获取)(近\s*\d{1,3}\s*天)?数据$/u, (_, verb, days = '') => `更新数据${days}`)
    .replace(/^数据(报表|分析报告|复盘报告)(\s*\d{1,3}\s*天)?$/u, (_, _kind, days = '') => `数据报告${days}`)
    .replace(/^自动(回复|处理)(留言|互动|消息)$/u, '自动回复')
    .replace(/^回复(留言|消息)$/u, '自动回复')
    .replace(/^生成(选题|内容方案|视频文案|口播文案)$/u, '生成下一条视频')
    .replace(/^下一条(选题|内容方案|视频文案|口播文案)$/u, '生成下一条视频');
}

function maybeIncompletePublishTaskText(text) {
  const raw = String(text || '').trim();
  if (!raw) return null;
  if (marketingPendingVideoReview()) return null;
  if (isMarketingVideoRejectText(raw)) return null;
  if (/训练视频|授权视频|授权文件|trainingVideoUrl|authVideoUrl|authFileUrl|形象定制|训练数字人|本人照片|形象照片|头像照片|照片\s*[:：]|photoUrl|photo\s*[:：]/i.test(raw)) return null;
  const hasPublishField = /视频地址|视频链接|视频url|videoUrl|封面图片|封面链接|coverImageUrl|标题|title|tags\s*[:：]/i.test(raw);
  if (!hasPublishField) return null;
  const missing = [];
  if (!/(视频地址|视频链接|视频url|videoUrl)\s*[:：]\s*\S+/i.test(raw)) missing.push('视频地址');
  if (!/(标题|title)\s*[:：]\s*\S+/i.test(raw)) missing.push('标题');
  if (!missing.length) return null;
  return `发布任务信息不完整，还缺：${missing.join('、')}。\n请按格式发送：\n视频地址：https://...\n标题：作品标题\n封面图片：https://...（可选）\ntags:#标签1#标签2`;
}

function saveState(state) {
  mkdirSync(STATE_DIR, { recursive: true });
  const entries = Object.entries(state.seen || {}).sort((a, b) => Number(b[1]) - Number(a[1])).slice(0, 500);
  writeFileSync(STATE_PATH, JSON.stringify({
    ...state,
    seen: Object.fromEntries(entries),
    updatedAt: new Date().toISOString(),
  }, null, 2));
}

function patchJsonFile(path, patch) {
  if (!path || !existsSync(path)) return null;
  try {
    const current = JSON.parse(readFileSync(path, 'utf8'));
    const next = {
      ...current,
      ...patch,
      updatedAt: new Date().toISOString(),
    };
    writeFileSync(path, `${JSON.stringify(next, null, 2)}\n`);
    return next;
  } catch {
    return null;
  }
}

function markMessageSeen(state, messageId, createTime = nowMs()) {
  if (!state || !messageId) return;
  if (!state.seen || typeof state.seen !== 'object') state.seen = {};
  state.seen[messageId] = Number(createTime || Date.now());
}

function nowMs() {
  return Date.now();
}

function extractText(message) {
  if (!message?.body?.content) return '';
  try {
    const content = JSON.parse(message.body.content);
    return String(content.text || '').trim();
  } catch {
    return String(message.body.content || '').trim();
  }
}

function buildSyntheticMessage(text, opts = {}) {
  const now = Date.now();
  return {
    message_id: opts.messageId || `manual_${now}`,
    chat_id: opts.chatId,
    create_time: String(opts.createTime || now),
    msg_type: opts.msgType || 'text',
    sender: { sender_type: 'user' },
    body: {
      content: JSON.stringify({ text: String(text || '').trim() }),
    },
  };
}

function parseContent(message) {
  if (!message?.body?.content) return {};
  try {
    return JSON.parse(message.body.content);
  } catch {
    return {};
  }
}

function sanitizeFileName(name) {
  const safe = String(name || 'feishu-video')
    .replace(/[\\/:*?"<>|\r\n\t]/g, '_')
    .replace(/\s+/g, '_')
    .slice(0, 120);
  return safe || 'feishu-video';
}

function firstAvailable(...values) {
  return values.find((value) => typeof value === 'string' && value.trim());
}

function parseJsonObjects(text) {
  const objects = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  for (let i = 0; i < String(text || '').length; i += 1) {
    const ch = text[i];
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
        try {
          objects.push(JSON.parse(text.slice(start, i + 1)));
        } catch {
          // Ignore non-JSON spans from command logs.
        }
        start = -1;
      }
    }
  }
  return objects;
}

function parseLastJsonObject(text) {
  const objects = parseJsonObjects(text);
  return objects[objects.length - 1] || null;
}

function extractAttachment(message) {
  const msgType = message?.msg_type || message?.message_type;
  const content = parseContent(message);
  const fileKey = firstAvailable(
    content.file_key,
    content.fileKey,
    content.file_token,
    content.fileToken,
    content.media_id,
    content.mediaId,
    content.video_key,
    content.videoKey,
  );
  const fileName = firstAvailable(content.file_name, content.fileName, content.name, content.title);
  const extension = extname(fileName || '').toLowerCase();
  const looksLikeVideo = msgType === 'video' || VIDEO_EXTENSIONS.has(extension);
  if (!fileKey || !looksLikeVideo) return null;
  return {
    messageId: message.message_id,
    msgType,
    fileKey,
    fileName: fileName || `feishu-video-${message.message_id || Date.now()}.mp4`,
    resourceType: 'file',
    content,
  };
}

async function downloadAttachment(message) {
  const attachment = extractAttachment(message);
  if (!attachment) return null;
  mkdirSync(UPLOAD_DIR, { recursive: true });
  const ext = extname(attachment.fileName) || '.mp4';
  const stem = basename(attachment.fileName, ext);
  const outputPath = join(UPLOAD_DIR, `${Date.now()}_${sanitizeFileName(stem)}${ext}`);
  const downloaded = await downloadFeishuMessageResource(
    attachment.messageId,
    attachment.fileKey,
    { outputPath, type: attachment.resourceType },
  );
  const size = statSync(outputPath).size;
  return {
    ...attachment,
    outputPath,
    bytes: size || downloaded.bytes,
  };
}

function runNode(args, opts = {}) {
  const result = spawnSync(process.execPath, args, {
    cwd: join(__dirname, '..'),
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: Number(opts.timeout || 120000),
    env: { ...process.env, ...(opts.env || {}) },
  });
  const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
  return {
    ok: result.status === 0,
    status: result.status,
    signal: result.signal,
    error: result.error?.message,
    timedOut: result.error?.code === 'ETIMEDOUT' || result.signal === 'SIGTERM',
    output,
    stdout: result.stdout || '',
    stderr: result.stderr || '',
  };
}

function routeDryRun() {
  return process.env.FEISHU_DRY_RUN === 'true';
}

function routeLightMode() {
  return process.env.DOUYIN_ROUTE_LIGHT_TEST === 'true';
}

function safeCustomerMessage(result) {
  return result?.payload?.customerMessage || result?.customerMessage || '';
}

function isDigitalHumanReadyAction(action) {
  return /^digital_human_training_succeeded|^digital_human_training_already_succeeded|^bind_model_id|^digital_human_default_model_confirmed/.test(String(action || ''));
}

function isMarketingVideoGeneratedAction(action) {
  return /^marketing_video_generated$|^marketing_video_already_pending$|^marketing_generate_and_publish/.test(String(action || ''));
}

function normalizeChatId(value) {
  if (typeof value !== 'string') return '';
  return value.trim();
}

function feishuTargetFromMessage(message) {
  const chatId = normalizeChatId(message?.chat_id || message?.chatId);
  if (!chatId) return null;
  return {
    receiveId: chatId,
    receiveIdType: 'chat_id',
  };
}

function saveBoundFeishuTarget(target, source = 'bind_current_chat') {
  if (!target?.receiveId) return null;
  const payload = {
    receiveId: target.receiveId,
    receiveIdType: target.receiveIdType || 'chat_id',
    source,
    updatedAt: new Date().toISOString(),
  };
  mkdirSync(dirname(BOUND_FEISHU_TARGET_PATH), { recursive: true });
  writeFileSync(BOUND_FEISHU_TARGET_PATH, `${JSON.stringify(payload, null, 2)}\n`);
  return payload;
}

async function bindCurrentFeishuTarget(state, message) {
  const target = feishuTargetFromMessage(message) || state?.feishuTarget;
  if (!target?.receiveId) {
    const customerMessage = '绑定失败：没有识别到当前飞书会话。请在飞书里重新发送：绑定当前会话';
    await notifyOnce(state, 'bind_current_chat_missing_target', customerMessage, { force: true });
    return { action: 'bind_current_chat_failed', customerMessage };
  }
  const bound = saveBoundFeishuTarget(target);
  setActiveFeishuTarget(state, target, 'bind_current_chat');
  const customerMessage = '已绑定当前飞书会话。后续二维码、验证码提醒和发布结果都会发到这里。';
  await notifyOnce(state, 'bind_current_chat_ok', customerMessage, { force: true });
  return { action: 'bind_current_chat_ok', target: bound, customerMessage };
}

function applyFeishuTargetToEnv(target) {
  if (!target?.receiveId) return;
  process.env.DOUYIN_FEISHU_RECEIVE_ID = target.receiveId;
  process.env.DOUYIN_FEISHU_RECEIVE_ID_TYPE = target.receiveIdType || 'chat_id';
}

function setActiveFeishuTarget(state, target, source = 'message') {
  if (!state || !target?.receiveId) return null;
  const next = {
    receiveId: target.receiveId,
    receiveIdType: target.receiveIdType || 'chat_id',
    source,
    updatedAt: new Date().toISOString(),
  };
  state.feishuTarget = next;
  applyFeishuTargetToEnv(next);
  return next;
}

function activeFeishuConfig(state) {
  const target = state?.feishuTarget;
  if (target?.receiveId) {
    return resolveFeishuConfig({
      receiveId: target.receiveId,
      receiveIdType: target.receiveIdType || 'chat_id',
    });
  }
  return resolveFeishuConfig();
}

function clearActiveFeishuTarget(state) {
  if (!state) return;
  state.feishuTarget = null;
}

function clearStaleFeishuTargetForSourceLessRoute(state, explicitTarget, sourceMessage) {
  if (!state || explicitTarget || sourceMessage) return;
  if (!flowActive(state)) clearActiveFeishuTarget(state);
}

function withFeishuTargetEnv(state, fn) {
  const previousReceiveId = process.env.DOUYIN_FEISHU_RECEIVE_ID;
  const previousReceiveIdType = process.env.DOUYIN_FEISHU_RECEIVE_ID_TYPE;
  const target = state?.feishuTarget;
  if (target?.receiveId) applyFeishuTargetToEnv(target);
  try {
    return fn();
  } finally {
    if (previousReceiveId === undefined) delete process.env.DOUYIN_FEISHU_RECEIVE_ID;
    else process.env.DOUYIN_FEISHU_RECEIVE_ID = previousReceiveId;
    if (previousReceiveIdType === undefined) delete process.env.DOUYIN_FEISHU_RECEIVE_ID_TYPE;
    else process.env.DOUYIN_FEISHU_RECEIVE_ID_TYPE = previousReceiveIdType;
  }
}

async function trySendFeishuText(text, opts = {}) {
  const attempts = Number(opts.attempts || 3);
  let lastError = null;
  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    try {
      return await sendFeishuTextChunks(text, opts.feishuConfig || resolveFeishuConfig(), {
        maxLength: opts.maxLength || process.env.FEISHU_TEXT_CHUNK_MAX_CHARS || 7000,
      });
    } catch (err) {
      lastError = err;
      console.warn(`[feishu] text notify failed (${attempt}/${attempts}): ${err.message}`);
      if (attempt < attempts) {
        await new Promise((resolve) => setTimeout(resolve, attempt * 800));
      }
    }
  }
  return { ok: false, error: lastError?.message || 'send_failed' };
}

async function notifyOnce(state, key, text, opts = {}) {
  const sendOpts = { ...opts, feishuConfig: opts.feishuConfig || activeFeishuConfig(state) };
  if (!state) return trySendFeishuText(text, sendOpts);
  if (!state.notified || typeof state.notified !== 'object') state.notified = {};
  const now = Date.now();
  const ttlMs = Number(opts.ttlMs || 10 * 60 * 1000);
  const previous = state.notified[key];
  if (!opts.force && previous?.text === text && now - Number(previous.at || 0) < ttlMs) {
    return { ok: true, skipped: true, key };
  }
  const result = await trySendFeishuText(text, sendOpts);
  if (result.ok) {
    state.notified[key] = { text, at: now };
  }
  return result;
}

function usageText(state = null) {
  const step = state?.flow?.step || '';
  const lines = ['未识别这条指令。请直接发送以下任一关键词：'];
  if (step === 'waiting_login_sms' || step === 'waiting_publish_sms') {
    lines.push('发送验证码', '6 位短信验证码');
  } else if (step === 'waiting_scan_confirm' || step === 'waiting_qr_ready') {
    lines.push('发送二维码', '已登录');
  } else if (step === 'waiting_video' || step === 'waiting_publish_confirm') {
    lines.push('发送视频', '发布视频');
  }
  lines.push('发布抖音', '更新数据', '数据报告', '生成下一条视频', '具体文案', '自动回复', '定时任务', '截图');
  return [...new Set(lines)].join('\n');
}

async function notifyUsage(state, action, text) {
  const message = usageText(state);
  await notifyOnce(state, `usage_help_${action}`, message, { force: true, ttlMs: 60 * 1000 });
  return { action, text, customerMessage: message };
}

function parseLastJson(text) {
  const trimmed = String(text || '').trim();
  const candidates = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  for (let i = 0; i < trimmed.length; i += 1) {
    const ch = trimmed[i];
    if (inString) {
      if (escaped) {
        escaped = false;
      } else if (ch === '\\') {
        escaped = true;
      } else if (ch === '"') {
        inString = false;
      }
      continue;
    }
    if (ch === '"') {
      inString = true;
    } else if (ch === '{') {
      if (depth === 0) start = i;
      depth += 1;
    } else if (ch === '}') {
      depth -= 1;
      if (depth === 0 && start !== -1) {
        candidates.push(trimmed.slice(start, i + 1));
        start = -1;
      }
    }
  }
  for (let i = candidates.length - 1; i >= 0; i -= 1) {
    try {
      return JSON.parse(candidates[i]);
    } catch {
      continue;
    }
  }
  return null;
}

function parseUpstreamPublishText(text) {
  const raw = String(text || '').trim();
  if (/训练视频|授权视频|授权文件|trainingVideoUrl|authVideoUrl|authFileUrl|形象定制|训练数字人|本人照片|形象照片|头像照片|照片\s*[:：]|photoUrl|photo\s*[:：]/i.test(raw)) return null;
  if (!raw || !/视频地址|视频链接|视频url|videoUrl|封面图片|封面链接|coverImageUrl|标题|title/i.test(raw)) return null;
  if (!/视频地址|视频链接|视频url|videoUrl/i.test(raw) || !/标题|title/i.test(raw)) return null;
  try {
    if (raw.startsWith('{')) return JSON.parse(raw);
  } catch {
    // Continue with line parser.
  }
  const result = {};
  for (const line of raw.split(/\r?\n/)) {
    const cleaned = line.trim().replace(/,$/, '');
    if (!cleaned) continue;
    const match = cleaned.match(/^"?([^":：]+)"?\s*[:：]\s*(.+)$/);
    if (!match) continue;
    const key = match[1].trim();
    const value = match[2].trim().replace(/^["“”]|["“”]$/g, '').trim();
    result[key] = value;
  }
  if (!result['视频地址']) result['视频地址'] = result['视频链接'] || result['视频url'] || result.videoUrl;
  if (!result['封面图片']) result['封面图片'] = result['封面链接'] || result.coverImageUrl;
  if (!result['标题']) result['标题'] = result.title;
  return result['视频地址'] || result.videoUrl ? result : null;
}

function writeUpstreamInput(input) {
  mkdirSync(UPSTREAM_DIR, { recursive: true });
  const inputPath = join(UPSTREAM_DIR, `upstream-${Date.now()}.json`);
  const taskPath = join(UPSTREAM_DIR, `publish-task-${Date.now()}.json`);
  writeFileSync(inputPath, `${JSON.stringify(input, null, 2)}\n`);
  return { inputPath, taskPath };
}

function makeJobId(prefix) {
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`;
}

function targetFromState(state) {
  return state?.feishuTarget?.receiveId ? {
    receiveId: state.feishuTarget.receiveId,
    receiveIdType: state.feishuTarget.receiveIdType || 'chat_id',
  } : null;
}

function startPreparedPublishJob(state, task, opts = {}) {
  mkdirSync(PUBLISH_JOB_DIR, { recursive: true });
  const jobId = makeJobId('upstream');
  const statusPath = join(PUBLISH_JOB_DIR, `${jobId}.status.json`);
  const target = targetFromState(state);
  writeFileSync(statusPath, `${JSON.stringify({
    ok: true,
    jobId,
    status: 'queued',
    stage: 'prepared_task_queued',
    taskPath: task.taskPath,
    inputPath: task.inputPath,
    title: task.title || '',
    notify: true,
    feishuTarget: target,
    sourceMessageId: opts.messageId || state?.lastRouteMessageId || null,
    createdAt: new Date().toISOString(),
  }, null, 2)}\n`);

  const runner = startBackgroundNodeJob({
    scriptPath: join(__dirname, 'publish-upstream-job-worker.js'),
    args: ['--job', statusPath, '--skip-prepare'],
    cwd: join(__dirname, '..'),
    unitName: `douyin-publish-upstream-${jobId}`,
    description: `Douyin upstream publish ${jobId}`,
    runtimeMaxSec: 7200,
    env: {
      ...statePathEnv(),
      DOUYIN_FEISHU_RECEIVE_ID: target?.receiveId || process.env.DOUYIN_FEISHU_RECEIVE_ID || '',
      DOUYIN_FEISHU_RECEIVE_ID_TYPE: target?.receiveIdType || process.env.DOUYIN_FEISHU_RECEIVE_ID_TYPE || 'chat_id',
    },
  });
  const current = JSON.parse(readFileSync(statusPath, 'utf8'));
  writeFileSync(statusPath, `${JSON.stringify({
    ...current,
    runner,
    updatedAt: new Date().toISOString(),
  }, null, 2)}\n`);

  return { jobId, statusPath, runner };
}

function startNextVideoPlanJob(state, text, opts = {}) {
  mkdirSync(NEXT_VIDEO_PLAN_JOB_DIR, { recursive: true });
  const days = parseDataDays(text, opts.days || 90);
  const jobId = makeJobId('next-video-plan');
  const statusPath = join(NEXT_VIDEO_PLAN_JOB_DIR, `${jobId}.status.json`);
  const target = state?.feishuTarget?.receiveId ? {
    receiveId: state.feishuTarget.receiveId,
    receiveIdType: state.feishuTarget.receiveIdType || 'chat_id',
  } : null;
  writeFileSync(statusPath, `${JSON.stringify({
    ok: true,
    jobId,
    status: 'queued',
    stage: 'queued',
    text,
    days,
    notify: true,
    feishuTarget: target,
    sourceMessageId: opts.messageId || state?.lastRouteMessageId || null,
    createdAt: new Date().toISOString(),
  }, null, 2)}\n`);

  const runner = startBackgroundNodeJob({
    scriptPath: join(__dirname, 'next-video-plan-job-worker.js'),
    args: ['--job', statusPath],
    cwd: join(__dirname, '..'),
    unitName: `douyin-next-video-plan-${jobId}`,
    description: `Douyin next video plan ${jobId}`,
    runtimeMaxSec: 1800,
    env: statePathEnv(),
  });
  const current = JSON.parse(readFileSync(statusPath, 'utf8'));
  writeFileSync(statusPath, `${JSON.stringify({
    ...current,
    runner,
    updatedAt: new Date().toISOString(),
  }, null, 2)}\n`);

  return { jobId, statusPath, days };
}

function startMarketingVideoJob(state, text = '确认方案', opts = {}) {
  mkdirSync(MARKETING_VIDEO_JOB_DIR, { recursive: true });
  const jobId = makeJobId('marketing-video');
  const statusPath = join(MARKETING_VIDEO_JOB_DIR, `${jobId}.status.json`);
  const marketingState = currentMarketingState();
  const target = state?.feishuTarget?.receiveId ? {
    receiveId: state.feishuTarget.receiveId,
    receiveIdType: state.feishuTarget.receiveIdType || 'chat_id',
  } : null;
  writeFileSync(statusPath, `${JSON.stringify({
    ok: true,
    jobId,
    status: 'queued',
    stage: 'queued',
    routeText: text,
    notify: true,
    feishuTarget: target,
    sourceMessageId: opts.messageId || state?.lastRouteMessageId || null,
    createdAt: new Date().toISOString(),
  }, null, 2)}\n`);
  saveMarketingStatePatch({
    inFlightVideo: {
      ...(marketingState?.inFlightVideo || {}),
      runId: jobId,
      status: 'running',
      source: 'background_job',
      statusPath,
      startedAt: new Date().toISOString(),
      title: marketingState?.pendingPlan?.plan?.plan?.title || marketingState?.pendingPlan?.plan?.title || '',
    },
  });

  const runner = startBackgroundNodeJob({
    scriptPath: join(__dirname, 'marketing-video-job-worker.js'),
    args: ['--job', statusPath],
    cwd: join(__dirname, '..'),
    unitName: `douyin-marketing-video-${jobId}`,
    description: `Douyin marketing video ${jobId}`,
    runtimeMaxSec: 1800,
    env: {
      ...statePathEnv(),
      DOUYIN_FEISHU_RECEIVE_ID: target?.receiveId || process.env.DOUYIN_FEISHU_RECEIVE_ID || '',
      DOUYIN_FEISHU_RECEIVE_ID_TYPE: target?.receiveIdType || process.env.DOUYIN_FEISHU_RECEIVE_ID_TYPE || 'chat_id',
    },
  });
  const current = JSON.parse(readFileSync(statusPath, 'utf8'));
  writeFileSync(statusPath, `${JSON.stringify({
    ...current,
    runner,
    updatedAt: new Date().toISOString(),
  }, null, 2)}\n`);

  return { jobId, statusPath };
}

function startPersonaGenerationJob(state, text, opts = {}) {
  mkdirSync(PERSONA_JOB_DIR, { recursive: true });
  const jobId = makeJobId('persona');
  const statusPath = join(PERSONA_JOB_DIR, `${jobId}.status.json`);
  const target = state?.feishuTarget?.receiveId ? {
    receiveId: state.feishuTarget.receiveId,
    receiveIdType: state.feishuTarget.receiveIdType || 'chat_id',
  } : null;
  writeFileSync(statusPath, `${JSON.stringify({
    ok: true,
    jobId,
    status: 'queued',
    stage: 'queued',
    text,
    notify: true,
    dryRun: routeDryRun(),
    feishuTarget: target,
    sourceMessageId: opts.messageId || state?.lastRouteMessageId || null,
    createdAt: new Date().toISOString(),
  }, null, 2)}\n`);

  const runner = startBackgroundNodeJob({
    scriptPath: join(__dirname, 'persona-generation-job-worker.js'),
    args: ['--job', statusPath],
    cwd: join(__dirname, '..'),
    unitName: `douyin-persona-${jobId}`,
    description: `Douyin persona generation ${jobId}`,
    runtimeMaxSec: 900,
    env: {
      ...statePathEnv(),
      DOUYIN_FEISHU_RECEIVE_ID: target?.receiveId || process.env.DOUYIN_FEISHU_RECEIVE_ID || '',
      DOUYIN_FEISHU_RECEIVE_ID_TYPE: target?.receiveIdType || process.env.DOUYIN_FEISHU_RECEIVE_ID_TYPE || 'chat_id',
    },
  });
  const current = JSON.parse(readFileSync(statusPath, 'utf8'));
  writeFileSync(statusPath, `${JSON.stringify({
    ...current,
    runner,
    updatedAt: new Date().toISOString(),
  }, null, 2)}\n`);

  return { jobId, statusPath };
}

function currentOnboardingJob(state = null) {
  const job = state?.onboardingJob;
  if (!job?.statusPath || !existsSync(job.statusPath)) return null;
  try {
    return JSON.parse(readFileSync(job.statusPath, 'utf8'));
  } catch {
    return null;
  }
}

function onboardingJobRunning(state = null) {
  const job = currentOnboardingJob(state);
  return ['queued', 'running'].includes(String(job?.status || ''));
}

function startOnboardingAfterPersonaJob(state, opts = {}) {
  mkdirSync(ONBOARDING_JOB_DIR, { recursive: true });
  const jobId = makeJobId('onboarding');
  const statusPath = join(ONBOARDING_JOB_DIR, `${jobId}.status.json`);
  const target = state?.feishuTarget?.receiveId ? {
    receiveId: state.feishuTarget.receiveId,
    receiveIdType: state.feishuTarget.receiveIdType || 'chat_id',
  } : null;
  writeFileSync(statusPath, `${JSON.stringify({
    ok: true,
    jobId,
	    status: 'queued',
	    stage: 'queued',
	    notify: true,
	    notifyProgress: false,
	    dryRun: routeDryRun(),
    feishuTarget: target,
    sourceMessageId: opts.messageId || state?.lastRouteMessageId || null,
    createdAt: new Date().toISOString(),
  }, null, 2)}\n`);

  state.onboardingJob = {
    jobId,
    status: 'running',
    statusPath,
    startedAt: new Date().toISOString(),
  };

  const runner = startBackgroundNodeJob({
    scriptPath: join(__dirname, 'onboarding-after-persona-worker.js'),
    args: ['--job', statusPath],
    cwd: join(__dirname, '..'),
    unitName: `douyin-onboarding-${jobId}`,
    description: `Douyin onboarding after persona ${jobId}`,
    runtimeMaxSec: 2400,
    env: {
      ...statePathEnv(),
      DOUYIN_FEISHU_RECEIVE_ID: target?.receiveId || process.env.DOUYIN_FEISHU_RECEIVE_ID || '',
      DOUYIN_FEISHU_RECEIVE_ID_TYPE: target?.receiveIdType || process.env.DOUYIN_FEISHU_RECEIVE_ID_TYPE || 'chat_id',
    },
  });
  const current = JSON.parse(readFileSync(statusPath, 'utf8'));
  writeFileSync(statusPath, `${JSON.stringify({
    ...current,
    runner,
    updatedAt: new Date().toISOString(),
  }, null, 2)}\n`);

  return { jobId, statusPath, runner };
}

function prepareUpstreamPublishTask(input) {
  const paths = writeUpstreamInput(input);
  const result = runNode([
    join(__dirname, 'prepare-upstream-publish-task.js'),
    '--input',
    paths.inputPath,
    '--output',
    paths.taskPath,
  ], { timeout: 180000 });
  return { result, payload: parseLastJson(result.output), ...paths };
}

function runPublishTask(taskPath) {
  const result = runNode([
    join(__dirname, 'publish-task.js'),
    '--task',
    taskPath,
    '--execute',
  ], { timeout: 720000 });
  return { result, payload: parseLastJson(result.output) };
}

function disableSchedulesForReset() {
  return runNode([join(__dirname, 'douyin-schedule-manager.js'), 'disable'], { timeout: 120000 });
}

function getCurrentLoginState() {
  const result = runNode([join(__dirname, 'douyin-login-monitor.js'), 'check']);
  return { result, payload: parseLastJson(result.output) };
}

function isBrowserRecoverableFailure(current) {
  const text = JSON.stringify(current?.payload || {}) + '\n' + String(current?.result?.output || '');
  return /Not connected|Protocol error|Target closed|Session closed|acquire_failed|Missing X server|Daemon 已启动但获取浏览器失败|ECONNREFUSED|WebSocket/i.test(text);
}

function restartSupervisorManagedDaemon() {
  return runNode(['--input-type=module', '-e', `
    import { spawnSync } from 'node:child_process';
    spawnSync('pkill', ['-TERM', '-f', 'src/daemon/server.js'], { stdio: 'ignore' });
    await new Promise((resolve) => setTimeout(resolve, 4000));
    console.log(JSON.stringify({ ok: true, action: 'daemon_restart_requested' }));
  `], { timeout: 15000 });
}

async function waitForSettledLoginState(attempts = 6, delayMs = 1500) {
  if (routeDryRun() && routeLightMode()) {
    return { result: { ok: true }, payload: { kind: 'logged_in', lightTest: true } };
  }
  let current = getCurrentLoginState();
  let recovered = false;
  for (let i = 0; i < attempts && (current.payload?.kind === 'page_loading' || isBrowserRecoverableFailure(current)); i += 1) {
    if (isBrowserRecoverableFailure(current) && !recovered) {
      restartSupervisorManagedDaemon();
      recovered = true;
    }
    await new Promise((resolve) => setTimeout(resolve, delayMs));
    current = getCurrentLoginState();
  }
  if (recovered) current.recoveredBrowser = true;
  return current;
}

function getPublishState(title = '') {
  const args = [join(__dirname, 'douyin-cli.js'), 'publish-state'];
  if (title) args.push('--title', title);
  const result = runNode(args, { timeout: 45000 });
  return { result, payload: parseLastJson(result.output) };
}

function syncDouyinData(days = 90, opts = {}) {
  const args = [
    join(__dirname, 'sync-douyin-data-to-feishu-bitable.js'),
    '--days',
    String(days),
  ];
  if (opts.notify) args.push('--notify');
  return runNode(args, { timeout: 240000 });
}

function scheduleStatusMessage() {
  const result = runNode([join(__dirname, 'douyin-schedule-manager.js'), 'status'], { timeout: 30000 });
  const payload = parseLastJson(result.output);
  return {
    result,
    payload,
    message: payload?.customerMessage || '定时任务已开启。',
  };
}

function enableMarketingScheduleAfterPublish(title, publishPayload = {}) {
  const current = currentMarketingState();
  const dailyTime = current.schedule?.dailyTime || process.env.DOUYIN_DEFAULT_DAILY_TIME || '07:30';
  const scheduleConfigPath = join(STATE_DIR, 'schedule-config.json');
  let scheduleConfig = { version: 1, enabled: true, jobs: {} };
  try {
    if (existsSync(scheduleConfigPath)) scheduleConfig = JSON.parse(readFileSync(scheduleConfigPath, 'utf8'));
  } catch {
    scheduleConfig = { version: 1, enabled: true, jobs: {} };
  }
  const tz = process.env.DOUYIN_SCHEDULE_TZ || 'Asia/Shanghai';
  mkdirSync(dirname(scheduleConfigPath), { recursive: true });
  writeFileSync(scheduleConfigPath, `${JSON.stringify({
    ...scheduleConfig,
    enabled: true,
    jobs: {
      ...(scheduleConfig.jobs || {}),
      autoReply: {
        enabled: true,
        schedule: scheduleConfig.jobs?.autoReply?.schedule || { kind: 'every', every: '30m' },
      },
      dailyReport: {
        enabled: false,
        schedule: scheduleConfig.jobs?.dailyReport?.schedule || { kind: 'daily', time: dailyTime, tz },
      },
      marketingDaily: {
        enabled: true,
        schedule: { kind: 'daily', time: dailyTime, tz },
      },
    },
  }, null, 2)}\n`);
  return saveMarketingStatePatch({
    enabled: true,
    enabledAt: current.enabledAt || new Date().toISOString(),
    schedule: { ...(current.schedule || {}), dailyTime },
    pendingReview: null,
    inFlightVideo: null,
    lastRun: {
      ...(current.lastRun || {}),
      status: 'published',
      finishedAt: new Date().toISOString(),
      stage: 'published_verified',
      title,
      taskPath: publishPayload.taskPath || current.lastRun?.taskPath || '',
      publishPayload,
      checkedAt: new Date().toISOString(),
    },
  });
}

function publishDoneMessage(title) {
  const publishLine = title ? `老板，《${title}》视频投放成功，快去抖音查看吧！` : '老板，视频投放成功，快去抖音查看吧！';
  const schedule = scheduleStatusMessage();
  return {
    schedule,
    message: `${publishLine}\n\n${schedule.message}`,
  };
}

function reportDouyinData(days = 90, opts = {}) {
  const args = [
    join(__dirname, 'douyin-data-report-from-bitable.js'),
    '--days',
    String(days),
  ];
  if (opts.notify) args.push('--notify');
  return runNode(args, { timeout: 90000 });
}

function syncFailureText(payload) {
  if (payload?.actionRequired) {
    return `数据更新失败：需要开通飞书多维表权限。\n请点击授权：${payload.authUrl || '请在开放平台开通 bitable:app 或 base:app:create'}`;
  }
  if (payload?.skipped && /write permission blocked|write.*blocked|permission/i.test(String(payload?.error || ''))) {
    return '数据更新失败：飞书多维表暂无写入权限，请重新授权多维表权限后再试。';
  }
  if (/Feishu HTTP 403|Forbidden|91403/i.test(String(payload?.error || payload?.stack || ''))) {
    return '数据更新失败：飞书多维表暂无写入权限，请重新授权多维表权限后再试。';
  }
  return '数据更新失败，请稍后重试。';
}

function parseDataDays(text, fallback = 90) {
  const match = String(text || '').match(/(\d{1,3})\s*天/);
  if (!match) return fallback;
  return Math.max(1, Math.min(365, Number(match[1])));
}

function bitablePermissionStatePath() {
  return join(STATE_DIR, 'feishu-bitable-permission-state.json');
}

function readBitablePermissionState() {
  try {
    return JSON.parse(readFileSync(bitablePermissionStatePath(), 'utf8'));
  } catch {
    return {};
  }
}

function writeBitablePermissionState(patch) {
  const next = { ...readBitablePermissionState(), ...patch, updatedAt: new Date().toISOString() };
  mkdirSync(STATE_DIR, { recursive: true });
  writeFileSync(bitablePermissionStatePath(), `${JSON.stringify(next, null, 2)}\n`);
  return next;
}

function isBitablePermissionError(payload) {
  return /Feishu HTTP 403|Forbidden|91403/i.test(String(payload?.error || payload?.stack || ''));
}

function markBitablePermissionFailure(payload) {
  if (!isBitablePermissionError(payload)) return null;
  return writeBitablePermissionState({
    writeBlocked: true,
    reason: 'feishu_bitable_write_forbidden',
    lastError: payload?.error || 'Feishu bitable write forbidden',
  });
}

function bitableWriteBlocked() {
  return readBitablePermissionState()?.writeBlocked === true;
}

async function syncDataAndNotify(state, text, opts = {}) {
  const days = parseDataDays(text, opts.days || 90);
  if (routeDryRun() && routeLightMode()) {
    const message = `数据已更新：近 ${days} 天，作品 0 条。`;
    await notifyOnce(state, `data_sync_light_${days}`, message, { force: true });
    return { action: 'sync_douyin_data_light_test', days, customerMessage: message };
  }
  if (bitableWriteBlocked()) {
    const message = '数据更新失败：飞书多维表暂无写入权限，请重新授权多维表权限后再试。';
    await notifyOnce(state, `data_sync_blocked_${Date.now()}`, message, { force: true });
    return { action: 'sync_douyin_data_write_permission_blocked', days, customerMessage: message };
  }
  const result = syncDouyinData(days, { notify: false });
  const payload = parseLastJson(result.output);
  if (result.ok && payload?.ok) {
    const message = payload?.notifyText
      || payload?.feishuText
      || `数据已更新：近 ${days} 天。`;
    await notifyOnce(state, `data_sync_done_${days}`, message, { force: true });
    return { action: 'sync_douyin_data', days, result, payload, customerMessage: message };
  }
  if (!payload?.notified) {
    await notifyOnce(
      state,
      `data_sync_failed_${Date.now()}`,
      syncFailureText(payload),
      { force: true },
    );
  }
  markBitablePermissionFailure(payload);
  return { action: 'sync_douyin_data_failed', days, result, payload, customerMessage: syncFailureText(payload) };
}

async function ensureLoggedInForCommand(state, command, text, meta = {}) {
  if (routeDryRun() && routeLightMode()) {
    clearStaleLoginFlowIfLoggedIn(state);
    return {
      loggedIn: true,
      current: { ok: true, payload: { kind: 'logged_in', lightTest: true } },
    };
  }
  const current = await waitForSettledLoginState();
  const payload = current.payload;
  if (payload?.kind === 'logged_in') {
    clearStaleLoginFlowIfLoggedIn(state);
    return { loggedIn: true, current };
  }

  setPendingCommand(state, command, text, meta);
  if (payload?.kind === 'qrcode') {
    activateFlow(state, 'waiting_qr_ready');
    await notifyOnce(state, 'login_qr_prepare', LOGIN_QR_PREPARE_MESSAGE, { force: true });
    return { loggedIn: false, action: `${command}_waiting_login_qr`, current };
  }
  if (payload?.kind === 'sms_code_input' || payload?.kind === 'sms_verification') {
    activateFlow(state, 'waiting_login_sms');
    await notifyOnce(state, 'login_sms_prompt', '抖音登录需要短信验证。请直接回复 6 位验证码。', { force: true });
    return { loggedIn: false, action: `${command}_waiting_login_sms`, current };
  }
  if (isBrowserRecoverableFailure(current)) {
    activateFlow(state, 'checking_login');
    await notifyOnce(state, 'browser_recovering', '系统正在恢复抖音浏览器连接，请稍后再发送指令。', { force: true });
    return { loggedIn: false, action: `${command}_browser_recovering`, current };
  }
  activateFlow(state, 'waiting_manual');
  await notifyOnce(state, 'manual_required', '抖音需要人工确认，请按页面提示处理。完成后回复：已完成', { force: true });
  return { loggedIn: false, action: `${command}_waiting_manual`, current };
}

async function reportDataAndNotify(state, text, opts = {}) {
  const days = parseDataDays(text, opts.days || 90);
  if (routeDryRun() && routeLightMode()) {
    const message = formatDataReportMessage(`数据报告：已同步近 ${days} 天作品明细 0 条。\n暂无可分析数据。`);
    await notifyOnce(state, `data_report_light_${days}`, message, { force: true });
    return { action: 'report_douyin_data_light_test', days, customerMessage: message };
  }
  const skipSync = bitableWriteBlocked();
  const sync = skipSync
    ? { ok: false, skipped: true, output: JSON.stringify({ ok: false, skipped: true, error: 'Feishu bitable write permission blocked' }) }
    : syncDouyinData(days, { notify: false });
  const syncPayload = parseLastJson(sync.output);
  if (!skipSync) markBitablePermissionFailure(syncPayload);
  const canFallbackToExistingBitable = !sync.ok || !syncPayload?.ok;
  const result = reportDouyinData(days, { notify: false });
  const payload = parseLastJson(result.output);
  if (result.ok && payload?.ok) {
    const message = formatDataReportMessage(payload.reportText || '数据报告已生成。');
    await notifyOnce(state, `data_report_done_${days}`, message, { force: true });
    return {
      action: canFallbackToExistingBitable
        ? 'report_douyin_data_from_existing_bitable'
        : 'sync_and_report_douyin_data_from_bitable',
      days,
      sync,
      syncPayload,
      usedStaleBitableFallback: canFallbackToExistingBitable,
      syncWarning: canFallbackToExistingBitable ? syncFailureText(syncPayload) : null,
      result,
      payload,
      customerMessage: message,
    };
  }
  if (canFallbackToExistingBitable) {
    await notifyOnce(state, `data_sync_failed_${Date.now()}`, syncFailureText(syncPayload), { force: true });
    return { action: 'report_douyin_data_sync_failed', days, sync, syncPayload, result, payload, customerMessage: syncFailureText(syncPayload) };
  }
  if (!payload?.notify?.ok) {
    await notifyOnce(state, `data_report_failed_${Date.now()}`, '数据报告生成失败，数据已尝试更新，请稍后重试。', { force: true });
  }
  return { action: 'report_douyin_data_failed', days, sync, syncPayload, result, payload, customerMessage: '数据报告生成失败，数据已尝试更新，请稍后重试。' };
}

function formatDataReportMessage(reportText) {
  const text = String(reportText || '数据报告已生成。').trim();
  if (text.startsWith('老板，昨日数据报告如下，请您查收～')) return text;
  return `老板，昨日数据报告如下，请您查收～\n${text}`;
}

async function nextVideoPlanAndNotify(state, text, opts = {}) {
  if (routeDryRun() && routeLightMode()) {
    return {
      action: 'next_video_plan_light_test',
      customerAlreadyNotifiedByTool: true,
      agentShouldReplyToFeishu: false,
      customerMessage: '',
    };
  }
  const job = startNextVideoPlanJob(state, text, opts);
  return {
    action: 'next_video_plan_job_started',
    ...job,
    customerAlreadyNotifiedByTool: true,
    agentShouldReplyToFeishu: false,
    customerMessage: '',
  };
}

function autoReplySummaryText(result, fallback = '自动回复失败，请稍后重试。') {
  const payload = parseLastJsonObject(result.output || '');
  if (!result.ok || !payload?.ok) return fallback;
  const deferred = (payload.results || []).some((item) => item?.deferred || item?.reason === 'deferred_to_publish');
  if (deferred) return '正在发布视频，自动回复已让路；发布完成后会继续处理。';
  const commentSent = Number(payload.summary?.commentSent || 0);
  const dmSent = Number(payload.summary?.dmSent || 0);
  return `自动回复完成：评论 ${commentSent} 条，私信 ${dmSent} 条。`;
}

function autoReplyArgs(kind) {
  const args = [
    join(__dirname, 'douyin-auto-reply.js'),
    kind,
    '--limit',
    String(process.env.DOUYIN_AUTO_REPLY_LIMIT || 50),
    '--max-scan',
    String(process.env.DOUYIN_AUTO_REPLY_MAX_SCAN || 200),
  ];
  if (!routeDryRun()) args.push('--execute');
  return args;
}

async function autoReplyAndNotify(state, kind, text) {
  if (routeDryRun() && routeLightMode()) {
    const message = kind === 'comment'
      ? '自动回复完成：评论 0 条，私信 0 条。'
      : (kind === 'dm' ? '自动回复完成：评论 0 条，私信 0 条。' : '自动回复完成：评论 0 条，私信 0 条。');
    await notifyOnce(state, `auto_reply_${kind}_light`, message, { force: true });
    return { action: `auto_reply_${kind}_light_test`, text, customerMessage: message };
  }
  const result = runNode(autoReplyArgs(kind));
  const fallback = kind === 'comment'
    ? '评论自动回复失败，请稍后重试。'
    : (kind === 'dm' ? '私信自动回复失败，请稍后重试。' : '自动回复失败，请稍后重试。');
  const message = autoReplySummaryText(result, fallback);
  await notifyOnce(state, `auto_reply_${kind}_${Date.now()}`, message, { force: true });
  return { action: `auto_reply_${kind}`, text, result, customerMessage: message };
}

async function startOrResumeOnboardingAfterPersona(state, text, baseResponse = {}, opts = {}) {
  if (onboardingJobRunning(state)) {
    return {
      ...baseResponse,
      action: 'persona_confirmed_onboarding_already_running',
      text,
      customerMessage: '',
      customerAlreadyNotifiedByTool: true,
      agentShouldReplyToFeishu: false,
    };
  }
  if (baseResponse?.payload?.action === 'persona_confirmed') {
    resetGeneratedMarketingStateForPersona();
  }
  const job = startOnboardingAfterPersonaJob(state);
  const startMessage = [
    '老板，我将基于原图照片和人设信息为您定制专属数字人形象，请稍等片刻~',
  ].join('\n');
  const alreadyNotified = Boolean(state?.notified?.persona_confirmed_start_digital_human);
  if (opts.notifyStart !== false && !alreadyNotified) {
    await notifyOnce(state, 'persona_confirmed_start_digital_human', startMessage, { force: true });
  }
  return {
    ...baseResponse,
    action: 'persona_confirmed_onboarding_job_started',
    text,
    job,
    customerMessage: alreadyNotified ? '' : startMessage,
    customerAlreadyNotifiedByTool: true,
    agentShouldReplyToFeishu: false,
  };
}

function scheduleArgs(text) {
  const args = [join(__dirname, 'douyin-schedule-manager.js'), 'route-text', '--text', text];
  if (routeDryRun()) args.push('--dry-run');
  return args;
}

async function scheduleAndNotify(state, text) {
  const result = runNode(scheduleArgs(text));
  const payload = parseLastJson(result.output);
  const message = payload?.customerMessage || (result.ok ? '定时任务已处理。' : '定时任务处理失败，请稍后重试。');
  await notifyOnce(state, `schedule_${Date.now()}`, message, { force: true });
  return { action: 'schedule_task', text, result, payload, customerMessage: message };
}

async function personaAndNotify(state, text) {
  const args = [
    join(__dirname, 'persona-flow.js'),
    'route-text',
    '--text',
    text,
  ];
  if (routeDryRun()) args.push('--dry-run');
  args.push('--defer-generate');
  const result = runNode(args);
  const payload = parseLastJson(result.output);
  if (payload?.action === 'persona_generation_deferred') {
    const job = startPersonaGenerationJob(state, text);
    return {
      action: 'persona_generation_job_started',
      text,
      result,
      payload,
      job,
      customerMessage: '',
      customerAlreadyNotifiedByTool: true,
      agentShouldReplyToFeishu: false,
    };
  }
  const message = payload?.customerMessage || (result.ok ? '人设流程已处理。' : '人设处理失败，请稍后重试。');
  const response = { action: 'persona_flow', text, result, payload, customerMessage: message };
  if (payload?.action === 'persona_confirmed' || payload?.action === 'persona_already_confirmed') {
    return startOrResumeOnboardingAfterPersona(state, text, response);
  }
  await notifyOnce(state, `persona_${payload?.action || 'route'}_${Date.now()}`, message, { force: true });
  return response;
}

async function marketingAndNotify(state, text, opts = {}) {
  const args = [
    join(__dirname, 'marketing-controller.js'),
    'route-text',
    '--text',
    text,
  ];
  if (routeDryRun()) args.push('--dry-run');
  if (opts.receiveId) {
    args.push('--receive-id', opts.receiveId, '--receive-id-type', opts.receiveIdType || 'chat_id');
  } else if (state?.feishuTarget?.receiveId) {
    args.push('--receive-id', state.feishuTarget.receiveId, '--receive-id-type', state.feishuTarget.receiveIdType || 'chat_id');
  }
  const result = runNode(args, { timeout: routeDryRun() ? 180000 : 1200000 });
  const payload = parseLastJson(result.output);
  const externalWatcherState = mergeExternalWatcherFlowState(state);
  const hasCustomerMessage = typeof payload?.customerMessage === 'string' && payload.customerMessage.trim() !== '';
  const message = hasCustomerMessage
    ? payload.customerMessage
    : (result.ok ? '' : '自动化营销处理失败，请稍后重试。');
  if (!opts.silent) {
    if (message) await notifyOnce(state, `marketing_${payload?.action || 'route'}_${Date.now()}`, message, { force: true });
  }
  return { action: 'marketing_controller', text, result, payload, externalWatcherStateMerged: Boolean(externalWatcherState), customerMessage: message };
}

async function confirmMarketingPlanAndStartVideoJob(state, text = '确认方案') {
  const marketingState = currentMarketingState();
  if (marketingState?.pendingReview?.publishText || marketingState?.pendingReview?.videoUrl) {
    return marketingAndNotify(state, '确认方案');
  }
  const message = '老板，正在为您制作视频，请耐心等待～';
  if (marketingState?.inFlightVideo?.status === 'running') {
    await notifyOnce(state, 'marketing_video_generating', message, { force: true });
    return {
      action: 'marketing_video_generation_already_running',
      text,
      customerMessage: message,
      customerAlreadyNotifiedByTool: true,
      agentShouldReplyToFeishu: false,
      inFlightVideo: marketingState.inFlightVideo,
    };
  }
  const job = startMarketingVideoJob(state, '确认方案');
  await notifyOnce(state, 'marketing_video_generation_started', message, { force: true });
  return {
    action: 'marketing_video_generation_started',
    text,
    ...job,
    customerMessage: message,
    customerAlreadyNotifiedByTool: true,
    agentShouldReplyToFeishu: false,
  };
}

async function rejectMarketingVideoAndStartRegenerateJob(state, text) {
  const marketingState = currentMarketingState();
  const message = '老板，收到修改意见，正在重新制作视频，请稍等～';
  if (routeDryRun() && routeLightMode()) {
    const feedback = marketingVideoRevisionFeedback(text);
    saveMarketingStatePatch({
      videoRevisionFeedback: feedback,
      lastVideoRevisionRequestedAt: new Date().toISOString(),
    });
    await notifyOnce(state, 'marketing_video_regeneration_started_light', message, { force: true });
    return {
      action: 'marketing_video_regeneration_started_light_test',
      text,
      customerMessage: message,
      customerAlreadyNotifiedByTool: true,
      agentShouldReplyToFeishu: false,
    };
  }
  if (marketingState?.inFlightVideo?.status === 'running') {
    await notifyOnce(state, 'marketing_video_regenerating', message, { force: true });
    return {
      action: 'marketing_video_generation_already_running',
      text,
      customerMessage: message,
      customerAlreadyNotifiedByTool: true,
      agentShouldReplyToFeishu: false,
      inFlightVideo: marketingState.inFlightVideo,
    };
  }
  const job = startMarketingVideoJob(state, text);
  await notifyOnce(state, 'marketing_video_regeneration_started', message, { force: true });
  return {
    action: 'marketing_video_regeneration_started',
    text,
    ...job,
    customerMessage: message,
    customerAlreadyNotifiedByTool: true,
    agentShouldReplyToFeishu: false,
  };
}

function captureCurrentPageScreenshot() {
  const script = `
    import { createDouyinSession, disconnect } from './src/index.js';
    import { mkdirSync, writeFileSync } from 'node:fs';
    import { join } from 'node:path';
    import config from './src/config.js';
    const { ops } = await createDouyinSession();
    try {
      mkdirSync(config.outputDir, { recursive: true });
      const filePath = join(config.outputDir, 'feishu_page_' + Date.now() + '.png');
      const buffer = await ops.screenshot({ fullPage: true });
      writeFileSync(filePath, buffer);
      console.log(JSON.stringify({ ok: true, filePath }, null, 2));
    } finally {
      disconnect();
    }
  `;
  return runNode(['--input-type=module', '-e', script], { timeout: 120000 });
}

async function runPendingCommandAfterLogin(state) {
  const pending = state?.pendingCommand;
  if (!pending?.command) return null;
  clearPendingCommand(state);
  if (pending.command === 'sync_data') {
    return syncDataAndNotify(state, pending.text || '更新数据', pending.meta || {});
  }
  if (pending.command === 'report_data') {
    return reportDataAndNotify(state, pending.text || '数据报告', pending.meta || {});
  }
  if (pending.command === 'next_video_plan') {
    return nextVideoPlanAndNotify(state, pending.text || '生成下一条视频', pending.meta || {});
  }
  if (pending.command === 'auto_reply_comment') {
    return autoReplyAndNotify(state, 'comment', pending.text || '自动回复评论');
  }
  if (pending.command === 'auto_reply_dm') {
    return autoReplyAndNotify(state, 'dm', pending.text || '自动回复私信');
  }
  if (pending.command === 'auto_reply_both') {
    return autoReplyAndNotify(state, 'both', pending.text || '自动回复');
  }
  return null;
}

async function notifyPublishDone(state, title) {
  const marketingState = enableMarketingScheduleAfterPublish(title, {
    title,
    taskPath: state?.pendingPublish?.taskPath || '',
    verifiedAfterSmsAt: new Date().toISOString(),
  });
  const done = publishDoneMessage(title);
  await notifyOnce(state, 'publish_done', done.message, { force: true });
  patchJsonFile(state?.pendingPublish?.publishJobPath, {
    status: 'succeeded',
    stage: 'verified_after_sms',
    customerMessage: done.message,
    verifiedAfterSmsAt: new Date().toISOString(),
  });
  return { schedule: done.schedule, marketingState };
}

function verifyPublishedTitle(title, waitMs = 8000) {
  const args = [join(__dirname, 'douyin-cli.js'), 'verify-published'];
  if (title) args.push('--title', title);
  args.push('--wait-ms', String(waitMs));
  const result = runNode(args, { timeout: 120000 });
  return { result, payload: parseLastJson(result.output) };
}

async function notifyPublishDoneAfterVerified(state, title) {
  const verify = verifyPublishedTitle(title, 8000);
  if (verify.payload?.found) {
    const schedule = await notifyPublishDone(state, title);
    endFlow(state);
    return { ok: true, action: 'publish_verified_and_notified', verify, schedule };
  }
  setFlowStep(state, 'publish_not_verified');
  await notifyOnce(state, 'publish_not_verified', '视频提交后未在作品管理页确认发布成功，请稍后回复：发布视频', { force: true });
  return { ok: false, action: 'publish_not_verified', verify };
}

function flowActive(state) {
  if (!state.flow?.active) return false;
  if (Date.now() - Number(state.flow.startedAt || 0) > SESSION_TTL_MS) {
    state.flow = null;
    state.pendingVideo = null;
    state.pendingCommand = null;
    state.lastSmsCode = null;
    return false;
  }
  return true;
}

function activateFlow(state, step = 'checking_login') {
  state.flow = {
    active: true,
    step,
    startedAt: Date.now(),
    updatedAt: Date.now(),
  };
  state.notified = {};
  state.lastSmsCode = null;
}

function setPendingCommand(state, command, text, meta = {}) {
  if (!state) return;
  state.pendingCommand = {
    command,
    text,
    meta,
    createdAt: Date.now(),
  };
}

function clearPendingCommand(state) {
  if (state) state.pendingCommand = null;
}

function setFlowStep(state, step) {
  if (!state.flow) activateFlow(state, step);
  state.flow.step = step;
  state.flow.updatedAt = Date.now();
}

function endFlow(state) {
  state.flow = null;
  state.pendingVideo = null;
  state.pendingPublish = null;
  state.pendingUpstreamTask = null;
  state.pendingCommand = null;
  state.lastSmsCode = null;
}

function clearStaleLoginFlowIfLoggedIn(state) {
  if (!state?.flow?.active) return;
  const step = state.flow.step;
  if (!['waiting_qr_ready', 'waiting_scan_confirm', 'waiting_login_sms', 'waiting_login_check', 'checking_login'].includes(step)) return;
  state.flow = null;
  state.pendingCommand = null;
  state.lastSmsCode = null;
}

function submitVisibleSmsCode(code) {
  const script = `
    import { createDouyinSession, disconnect } from './src/index.js';
    const { ops } = await createDouyinSession();
    try {
      const result = await ops.submitVisibleSmsCode(${JSON.stringify(code)});
      console.log(JSON.stringify(result, null, 2));
    } finally {
      disconnect();
    }
  `;
  return runNode(['--input-type=module', '-e', script]);
}

async function waitForLoginConfirmed(state, attempts = 20, delayMs = 1000) {
  for (let i = 0; i < attempts; i += 1) {
    const current = getCurrentLoginState();
    if (current.payload?.kind === 'logged_in') {
      return continueAfterLoginConfirmed(state, '验证码已提交');
    }
    if (current.payload?.kind === 'page_loading') {
      if (i + 1 < attempts) {
        await new Promise((resolve) => setTimeout(resolve, delayMs));
        continue;
      }
      break;
    }
    if (i + 1 < attempts) {
      await new Promise((resolve) => setTimeout(resolve, delayMs));
    }
  }
  setFlowStep(state, 'waiting_login_check');
  await notifyOnce(state, 'login_check_pending', '验证码已提交，正在确认登录结果。');
  return { action: 'login_sms_submitted_pending', text: '[6-digit-code]' };
}

async function reconcileActiveFlow(state) {
  if (!flowActive(state)) return null;
  const step = state.flow?.step;
  if (!['waiting_login_sms', 'waiting_login_check', 'confirming_publish'].includes(step)) {
    return null;
  }

  if (step === 'confirming_publish') {
    const publish = getPublishState(state.pendingPublish?.title || '');
    if (publish.payload?.published) {
      const title = state.pendingPublish?.title || publish.payload?.title || '';
      const schedule = await notifyPublishDone(state, title);
      endFlow(state);
      return { action: 'auto_confirm_publish_success', result: publish.result, schedule };
    }
    if (publish.payload?.verification?.found) {
      setFlowStep(state, 'waiting_publish_sms');
      await ensurePublishSmsPrompt(state);
      return { action: 'auto_detect_publish_sms_required', result: publish.result };
    }
    return null;
  }

  const current = await waitForSettledLoginState();
  const payload = current.payload;
  if (payload?.kind === 'logged_in') {
    return continueAfterLoginConfirmed(state, '自动确认登录成功');
  }
  if (payload?.kind === 'page_loading') {
    return null;
  }
  return null;
}

function requestPublishSmsCode() {
  const script = `
    import { createDouyinSession, disconnect } from './src/index.js';
    const { ops } = await createDouyinSession();
    try {
      const result = await ops.requestPublishSmsCode({ allowResend: false });
      console.log(JSON.stringify(result, null, 2));
    } finally {
      disconnect();
    }
  `;
  return runNode(['--input-type=module', '-e', script]);
}

function requestLoginSmsCode() {
  const script = `
    import { createDouyinSession, disconnect } from './src/index.js';
    const { ops } = await createDouyinSession();
    try {
      const result = await ops.requestLoginSmsCode({ allowResend: true });
      console.log(JSON.stringify(result, null, 2));
    } finally {
      disconnect();
    }
  `;
  return runNode(['--input-type=module', '-e', script]);
}

function parseSubmitPayload(result) {
  return parseLastJson(result.output);
}

function smsPromptFor(payload) {
  if (payload?.phase?.startsWith?.('publish_') || payload?.found === true) {
    return '抖音发布需要短信验证。收到短信后，请直接回复 6 位验证码。';
  }
  return '抖音登录需要短信验证。收到短信后，请直接回复 6 位验证码。';
}

async function ensurePublishSmsPrompt(state) {
  const sms = requestPublishSmsCode();
  const smsPayload = parseLastJson(sms.output);
  const sent = sms.ok && smsPayload?.ok;
  await notifyOnce(
    state,
    'publish_sms_prompt',
    sent
      ? '抖音发布需要短信验证，验证码已发送。请直接回复 6 位验证码。'
      : '抖音发布需要短信验证。请回复：发送验证码',
    { force: !sent },
  );
  return { sms, smsPayload };
}

async function confirmPublishResult(state, title, attempts = 18, delayMs = 2000) {
  for (let i = 0; i < attempts; i += 1) {
    const current = getPublishState(title);
    const payload = current.payload;
    if (payload?.published) {
      const schedule = await notifyPublishDone(state, title);
      endFlow(state);
      return { ok: true, action: 'publish_confirmed', result: current.result, schedule };
    }
    if (payload?.verification?.found) {
      setFlowStep(state, 'waiting_publish_sms');
      await ensurePublishSmsPrompt(state);
      return { ok: false, action: 'publish_needs_sms', result: current.result };
    }
    if (i + 1 < attempts) {
      await new Promise((resolve) => setTimeout(resolve, delayMs));
    }
  }
  setFlowStep(state, 'confirming_publish');
  await notifyOnce(state, 'publish_pending', '视频已提交，正在确认发布结果。');
  return { ok: false, action: 'publish_confirmation_pending' };
}

function userSafePublishFailure(payload) {
  const error = publishErrorOf(payload) || payload?.detail?.error || payload?.publish?.cover?.error;
  if (/upload_page_timeout|hd_publish_btn_not_found|editor_navigation_blocked|publish_editor_not_ready|publish_btn_not_found|publish_btn_obstructed|publish_btn_disabled|publish_submit_unconfirmed|publish_click_returned_to_upload/i.test(error || '')) {
    return '发布页面未准备好，我已保留当前草稿，请稍后回复：发布视频';
  }
  if (/cover|封面/i.test(error || '')) {
    return '封面设置失败，请重新发送可用的封面图片。';
  }
  if (payload?.error === 'file_not_found') {
    return '视频文件不可用，请重新发送视频。';
  }
  if (payload?.error === 'publish_btn_not_found' || payload?.error === 'publish_btn_obstructed') {
    return '发布页面未准备好，我会保留当前草稿，请稍后回复：发布视频';
  }
  if (/upload|上传|video/i.test(error || '')) {
    return '视频上传失败，请重新发送可用的视频。';
  }
  if (/login|session/i.test(error || '')) return LOGIN_QR_PREPARE_MESSAGE;
  return '视频发布暂未完成，我已保留当前状态，请稍后回复：发布视频';
}

function shouldRetryCurrentDraft(payload) {
  return ['publish_editor_not_ready', 'publish_btn_not_found', 'publish_btn_obstructed', 'publish_btn_disabled', 'publish_submit_unconfirmed', 'publish_click_returned_to_upload'].includes(payload?.error);
}

function publishErrorOf(payload) {
  return payload?.error || payload?.publish?.error || null;
}

function publishVerificationOf(payload) {
  return payload?.detail || payload?.publish?.detail || payload?.publish?.verification || null;
}

function userSafeTaskFailure(payload) {
  const nested = payload?.publish || payload?.validation || {};
  const error = payload?.error || nested.error || nested.customerMessage || '';
  const full = JSON.stringify(payload || {});
  if (/publish_verification_required/i.test(`${error}\n${full}`)) {
    return '抖音发布需要短信验证。请直接回复 6 位验证码。';
  }
  if (payload?.customerMessage) return payload.customerMessage;
  if (/ProtocolError|protocolTimeout|Runtime\.callFunctionOn timed out|Network\.enable timed out|Target closed|Session closed|WebSocket/i.test(`${error}\n${full}`)) {
    return '发布页面控制超时，我已保留当前草稿并会尝试恢复。请稍后回复：发布视频';
  }
  if (/upload_page_timeout|hd_publish_btn_not_found|editor_navigation_blocked|publish_editor_not_ready|publish_btn_not_found|publish_btn_obstructed|publish_btn_disabled|publish_submit_unconfirmed|publish_click_returned_to_upload/i.test(`${error}\n${full}`)) {
    return '发布页面未准备好，我已保留素材。请稍后回复：发布视频';
  }
  if (/cover|封面/i.test(error)) return '封面设置失败，请重新发送可用的封面图片。';
  if (/video|upload|file|视频|上传/i.test(error)) return '视频处理失败，请重新发送可用的视频。';
  if (/login|session/i.test(error)) return LOGIN_QR_PREPARE_MESSAGE;
  return '发布失败，请重新发送可用的视频和封面。';
}

async function publishPreparedTask(task, state = null) {
  if (state) {
    state.pendingUpstreamTask = task;
    state.pendingPublish = { title: task.title, taskPath: task.taskPath };
    setFlowStep(state, 'publishing_upstream_task');
  }
  if (routeDryRun()) {
    return { action: 'publish_upstream_task_dry_run', task };
  }
  if (process.env.DOUYIN_SUPPRESS_PUBLISH_START !== 'true') {
    await notifyOnce(state, 'upstream_publish_started', `已收到发布任务，开始发布。\n标题：${task.title || '未命名'}`, { force: true });
  }
  if (process.env.DOUYIN_SYNC_PUBLISH_TASK !== 'true') {
    const job = startPreparedPublishJob(state, task);
    return {
      action: 'publish_upstream_task_job_started',
      task,
      ...job,
      customerAlreadyNotifiedByTool: true,
      agentShouldReplyToFeishu: false,
    };
  }
  const { result, payload } = withFeishuTargetEnv(state, () => runPublishTask(task.taskPath));
  if (result.ok && payload?.ok) {
    await notifyPublishDone(state, payload.plan?.title || task.title || '');
    if (state) endFlow(state);
    return { action: 'publish_upstream_task_success', task, result, payload };
  }
  if (payload?.publish?.blocked) {
    if (state) {
      state.pendingUpstreamTask = task;
      state.pendingPublish = { title: task.title, taskPath: task.taskPath };
    }
    if (payload.publish.reason === 'qrcode') {
      if (state) setFlowStep(state, 'waiting_qr_ready');
      await notifyOnce(state, 'login_qr_prepare', LOGIN_QR_PREPARE_MESSAGE, { force: true });
    } else if (payload.publish.reason === 'sms_code_input' || payload.publish.reason === 'sms_verification') {
      if (state) setFlowStep(state, 'waiting_login_sms');
      await notifyOnce(state, 'login_sms_prompt', '抖音登录需要短信验证。请直接回复 6 位验证码。', { force: true });
    } else {
      if (state) setFlowStep(state, 'waiting_manual');
      await notifyOnce(state, 'manual_required', '抖音需要人工确认，请按页面提示处理。完成后回复：已完成', { force: true });
    }
    return { action: 'publish_upstream_task_blocked', task, result, payload };
  }
  if (payload?.publish?.error === 'publish_verification_required' || /publish_verification_required/i.test(JSON.stringify(payload || {}))) {
    if (state) {
      state.pendingUpstreamTask = task;
      state.pendingPublish = { title: task.title, taskPath: task.taskPath };
      setFlowStep(state, 'waiting_publish_sms');
    }
    await ensurePublishSmsPrompt(state);
    return { action: 'publish_upstream_task_needs_sms', task, result, payload };
  }
  await notifyOnce(state, 'upstream_publish_failed', userSafeTaskFailure(payload), { force: true });
  if (state) setFlowStep(state, 'waiting_upstream_retry');
  return { action: 'publish_upstream_task_failed', task, result, payload };
}

async function handleUpstreamPublishText(text, state) {
  const input = parseUpstreamPublishText(text);
  if (!input) return null;
  activateFlow(state, 'preparing_upstream_task');
  const prepared = prepareUpstreamPublishTask(input);
  if (!prepared.result.ok || !prepared.payload?.ok) {
    await notifyOnce(
      state,
      'upstream_prepare_failed',
      prepared.payload?.customerMessage || '素材处理失败，请重新发送可用的视频和封面。',
      { force: true },
    );
    return { action: 'prepare_upstream_task_failed', text, prepared };
  }
  const taskData = JSON.parse(readFileSync(prepared.taskPath, 'utf8'));
  const task = {
    taskPath: prepared.taskPath,
    inputPath: prepared.inputPath,
    title: taskData.metadata?.title || input['标题'] || input.title || '',
    videoPath: taskData.media?.videoPath,
    coverImagePath: taskData.media?.cover?.imagePath || null,
  };
  state.pendingUpstreamTask = task;
  const current = await waitForSettledLoginState();
  const payload = current.payload;
  if (payload?.kind === 'logged_in') {
    return publishPreparedTask(task, state);
  }
  if (payload?.kind === 'qrcode') {
    setFlowStep(state, 'waiting_qr_ready');
    await notifyOnce(state, 'login_qr_prepare', LOGIN_QR_PREPARE_MESSAGE, { force: true });
    return { action: 'upstream_task_waiting_login_qr', task, current };
  }
  if (payload?.kind === 'sms_code_input' || payload?.kind === 'sms_verification') {
    setFlowStep(state, 'waiting_login_sms');
    await notifyOnce(state, 'login_sms_prompt', '抖音登录需要短信验证。请直接回复 6 位验证码。', { force: true });
    return { action: 'upstream_task_waiting_login_sms', task, current };
  }
  if (isBrowserRecoverableFailure(current)) {
    setFlowStep(state, 'checking_login');
    await notifyOnce(state, 'browser_recovering', '系统正在恢复抖音浏览器连接，请稍后再发送发布任务。', { force: true });
    return { action: 'upstream_task_browser_recovering', task, current };
  }
  setFlowStep(state, 'waiting_manual');
  await notifyOnce(state, 'manual_required', '抖音需要人工确认，请按页面提示处理。完成后回复：已完成', { force: true });
  return { action: 'upstream_task_waiting_manual', task, current };
}

async function continueAfterLoginConfirmed(state, text) {
  const current = await waitForSettledLoginState();
  const payload = current.payload;
  if (payload?.kind === 'logged_in') {
    const pendingCommandResult = await runPendingCommandAfterLogin(state);
    if (pendingCommandResult) return pendingCommandResult;
    const task = pendingUpstreamTask(state);
    if (task) {
      return publishPreparedTask(task, state);
    }
    if (state.pendingVideo?.outputPath && existsSync(state.pendingVideo.outputPath)) {
      const pending = state.pendingVideo;
      state.pendingVideo = null;
      setFlowStep(state, 'publishing');
      return publishDownloadedVideo(pending, text || '发布视频', state);
    }
    setFlowStep(state, 'waiting_video');
    await notifyOnce(state, 'login_success_send_video', '登录成功，请发送视频。');
    return { action: 'login_confirmed_waiting_video', text, result: current.result };
  }
  if (payload?.kind === 'sms_code_input' || payload?.kind === 'sms_verification') {
    setFlowStep(state, 'waiting_login_sms');
    await notifyOnce(state, 'login_sms_prompt', '抖音登录需要短信验证。请直接回复 6 位验证码。');
    return { action: 'login_confirmed_but_sms_required', text, result: current.result };
  }
  if (payload?.kind === 'qrcode') {
    setFlowStep(state, 'waiting_scan_confirm');
    await notifyOnce(
      state,
      'login_claim_rejected_still_qrcode',
      '仍未登录，请用手机抖音 App 扫码并确认。二维码过期请回复：发送二维码。',
      { force: true }
    );
    return { action: 'login_claim_rejected_still_qrcode', text, result: current.result };
  }
  return { action: 'check_login', text, result: current.result };
}

function defaultTitleFor(filePath) {
  return basename(filePath, extname(filePath)).replace(/^\d+_/, '').replace(/_/g, ' ').slice(0, 30) || '视频';
}

async function publishDownloadedVideo(downloaded, text, state = null) {
  const titleMatch = text.match(/(?:标题|title)[:：]\s*([^\n]+)/i);
  const descMatch = text.match(/(?:简介|描述|description)[:：]\s*([\s\S]+)/i);
  const title = titleMatch?.[1]?.trim() || defaultTitleFor(downloaded.outputPath);
  const description = descMatch?.[1]?.trim() || title;
  if (state) {
    state.pendingVideo = downloaded;
    state.pendingPublish = { title, description, fileName: downloaded.fileName, outputPath: downloaded.outputPath };
  }
  if (routeDryRun()) {
    return {
      action: 'publish_video_from_feishu_dry_run',
      fileName: downloaded.fileName,
      outputPath: downloaded.outputPath,
      bytes: downloaded.bytes,
      title,
      description,
    };
  }
  await notifyOnce(state, 'publish_started', `已收到视频，开始发布。\n文件：${downloaded.fileName}`);
  const result = runNode([
    join(__dirname, 'publish-with-guard.js'),
    '--file',
    downloaded.outputPath,
    '--title',
    title,
    '--description',
    description,
    '--fresh',
  ], { timeout: 420000 });
  if (result.ok) {
    if (state) {
      setFlowStep(state, 'confirming_publish');
      await confirmPublishResult(state, title, 8, 1500);
    } else {
      await trySendFeishuText(`视频已提交发布。\n标题：${title}`);
    }
  } else {
    const payload = parseLastJson(result.output);
    if (payload?.blocked) {
      if (payload.reason === 'sms_code_input' || payload.reason === 'sms_verification') {
        if (state) setFlowStep(state, 'waiting_login_sms');
        await notifyOnce(state, 'login_sms_prompt', '抖音登录需要短信验证。请直接回复 6 位验证码。');
      } else if (payload.reason === 'qrcode') {
        if (state) setFlowStep(state, 'waiting_qr_ready');
        await notifyOnce(state, 'login_qr_prepare', LOGIN_QR_PREPARE_MESSAGE);
      } else {
        await notifyOnce(state, 'manual_required', '抖音需要人工确认，请按页面提示处理。完成后回复：已完成');
      }
    } else {
      if (publishErrorOf(payload) === 'publish_verification_required' || publishVerificationOf(payload)?.found) {
        if (state) setFlowStep(state, 'waiting_publish_sms');
        await ensurePublishSmsPrompt(state);
      } else if (payload?.error === 'upload_failed') {
        if (state) {
          state.pendingVideo = null;
          setFlowStep(state, 'waiting_video');
        }
        await notifyOnce(state, 'upload_failed', '视频上传失败，请重新发送视频。', { force: true });
      } else if (result.timedOut) {
        const current = getPublishState(title);
        if (current.payload?.published) {
          await notifyPublishDone(state, title);
          if (state) endFlow(state);
        } else if (current.payload?.verification?.found) {
          if (state) setFlowStep(state, 'waiting_publish_sms');
          await ensurePublishSmsPrompt(state);
        } else {
          await notifyOnce(state, 'publish_pending', '视频发布仍在处理中，我会继续确认结果。');
          if (state) setFlowStep(state, 'confirming_publish');
        }
      } else if (shouldRetryCurrentDraft(payload)) {
        const retry = runNode([join(__dirname, 'douyin-cli.js'), 'publish-current-draft', '--title', title], { timeout: 180000 });
        const retryPayload = parseLastJson(retry.output);
        if (retry.ok) {
          if (state) setFlowStep(state, 'confirming_publish');
          await confirmPublishResult(state, title, 8, 1500);
        } else if (retryPayload?.error === 'publish_verification_required') {
          if (state) setFlowStep(state, 'waiting_publish_sms');
          await ensurePublishSmsPrompt(state);
        } else {
          const current = getPublishState(title);
          if (current.payload?.verification?.found) {
            if (state) setFlowStep(state, 'waiting_publish_sms');
            await ensurePublishSmsPrompt(state);
          } else {
            if (state) {
              state.pendingVideo = downloaded;
              setFlowStep(state, 'confirming_publish');
            }
            await notifyOnce(state, 'publish_pending', '视频发布仍在处理中，我会继续确认结果。');
          }
        }
      } else {
        const current = getPublishState(title);
        if (current.payload?.published) {
          await notifyPublishDone(state, title);
          if (state) endFlow(state);
        } else {
          await notifyOnce(state, 'publish_retry_needed', userSafePublishFailure(payload), { force: true });
          if (state) {
            state.pendingVideo = downloaded;
            setFlowStep(state, 'waiting_publish_confirm');
          }
        }
      }
    }
  }
  return {
    action: 'publish_video_from_feishu',
    fileName: downloaded.fileName,
    outputPath: downloaded.outputPath,
    bytes: downloaded.bytes,
    title,
    result,
  };
}

async function startPublishFlow(state, text) {
  if (routeDryRun() && routeLightMode()) {
    setFlowStep(state, 'waiting_video');
    await notifyOnce(state, 'login_success_send_video', '登录成功，请发送视频。', { force: true });
    return { action: 'start_publish_flow_light_test', text };
  }
  activateFlow(state, 'checking_login');
  const current = await waitForSettledLoginState();
  const payload = current.payload;
  if (payload?.kind === 'logged_in') {
    setFlowStep(state, 'waiting_video');
    await notifyOnce(state, 'login_success_send_video', '登录成功，请发送视频。');
  } else if (payload?.kind === 'qrcode') {
    setFlowStep(state, 'waiting_qr_ready');
    withFeishuTargetEnv(state, () => runNode([
      join(__dirname, 'douyin-login-monitor.js'),
      'check',
      '--notify',
      '--send-qr',
      'ask',
    ]));
  } else if (payload?.kind === 'sms_code_input' || payload?.kind === 'sms_verification') {
    setFlowStep(state, 'waiting_login_sms');
    await notifyOnce(state, 'login_sms_prompt', '抖音登录需要短信验证。请直接回复 6 位验证码。');
  } else if (isBrowserRecoverableFailure(current)) {
    setFlowStep(state, 'checking_login');
    await notifyOnce(state, 'browser_recovering', '系统正在恢复抖音浏览器连接，请稍后再发送发布任务。', { force: true });
  } else {
    setFlowStep(state, 'waiting_manual');
    await notifyOnce(state, 'manual_required', '抖音需要人工确认，请按页面提示处理。完成后回复：已完成');
  }
  return { action: 'start_publish_flow', text, current };
}

async function handleMessage(message, text, state) {
  text = normalizeIncomingText(text);
  if (/^(绑定当前会话|绑定飞书会话|绑定这个会话|绑定本群|绑定当前群|绑定私聊)$/.test(text)) {
    return bindCurrentFeishuTarget(state, message);
  }

  if (isScheduleCommandText(text)) return scheduleAndNotify(state, text);

  if (marketingPendingVideoReview() && !internalConfirmedMarketingPublish()) {
    if (isMarketingVideoRejectText(text)) return rejectMarketingVideoAndStartRegenerateJob(state, text);
    if (isMarketingPublishConfirmText(text)) return marketingAndNotify(state, '确认发布');
    if (/^通过$/.test(text)) {
      const message = '视频已生成。若确认发布，请回复：确认发布；若需修改，请回复：不通过 + 修改意见。';
      await notifyOnce(state, 'marketing_video_review_require_confirm_publish', message, { force: true });
      return { action: 'marketing_video_review_waiting_explicit_confirm', text, customerMessage: message };
    }
    const message = '视频已生成。确认发布请回复：确认发布；需要修改请回复：不通过 + 修改意见。';
    await notifyOnce(state, 'marketing_video_review_waiting', message, { force: true });
    return { action: 'marketing_video_review_waiting', text, customerMessage: message };
  }

  const upstream = await handleUpstreamPublishText(text, state);
  if (upstream) return upstream;

  const incompletePublishTask = maybeIncompletePublishTaskText(text);
  if (incompletePublishTask) {
    await notifyOnce(state, 'incomplete_publish_task', incompletePublishTask, { force: true });
    return { action: 'incomplete_publish_task', text, customerMessage: incompletePublishTask };
  }

  if (/^通过$/.test(text)) {
    if (personaGenerationActive()) {
      const message = '人设方案还在生成，请等我发出审核方案后再回复【通过】或【不通过】。';
      await notifyOnce(state, 'persona_generation_wait_for_review', message, { force: true });
      return { action: 'persona_generation_wait_for_review', text, customerMessage: message };
    }
    if (personaDraftPending()) return personaAndNotify(state, '通过');
    if (marketingPendingPlan()) return confirmMarketingPlanAndStartVideoJob(state, '通过');
    if (loadPersonaState()?.confirmed && onboardingJobRunning(state)) {
      return {
        action: 'onboarding_already_running',
        text,
        customerMessage: '',
        customerAlreadyNotifiedByTool: true,
        agentShouldReplyToFeishu: false,
      };
    }
    if (loadPersonaState()?.confirmed && !marketingPendingVideoReview()) {
      return startOrResumeOnboardingAfterPersona(state, text, {}, { notifyStart: false });
    }
  }

  if (/^(不通过|不满意)(?:[\s\S]*)$/.test(text)) {
    if (personaGenerationActive()) {
      const message = '人设方案还在生成，请等我发出审核方案后再提出修改建议。';
      await notifyOnce(state, 'persona_generation_wait_for_revision', message, { force: true });
      return { action: 'persona_generation_wait_for_revision', text, customerMessage: message };
    }
    if (personaDraftPending()) return personaAndNotify(state, text);
    if (marketingPendingPlan() || marketingPendingVideoReview()) return marketingAndNotify(state, text);
  }

  if (shouldRouteAutomationStartToPersona(text)
    || /^(生成人设|账号定位|帮我做人设|人设状态|账号定位状态|查看人设|完整人设|查看完整人设|人设详情|账号定位详情|确认人设|采用这个人设|确认采用|重新生成人设|调整人设|修改人设)$/.test(text)
    || /^姓名\s*[:：]/.test(text)
    || /姓名\/昵称|主营业务|核心业务|目标客户|精准受众|IP核心诉求|禁忌与偏好/.test(text)
    || personaCollectingActive()
    || personaDraftPending()
    || looksLikePersonaInfo(text)) {
    return personaAndNotify(state, text);
  }

  if (/^(开启自动化营销|启动自动化营销|我要做自动化营销|确认开启|确认启动|确认开启自动化营销|确认启动自动化营销|开启自动确认|开启自动发布模式|自动确认|自动发布模式|跳过确认|以后自动确认|关闭自动确认|关闭自动发布模式|人工确认|手动确认|手动确认模式|人工确认模式|自动化营销状态|营销状态|当前状态|任务进度|关闭自动化营销|暂停自动发布|暂停自动化营销|查看形象|形象审核|审核形象|确认默认形象|默认数字人|查看数字人形象|确认形象|采用形象|采用默认形象|生成视频方案|生成内容方案|生成选题方案|生成模板|生成标题模板|立即生成视频|马上生成视频|现在生成视频|开始生成视频|确认方案|确认模板|采用方案|采用这个方案|生成数字人视频|一键成片|生成视频|确认发布|发布这个视频|确认发布视频|发布生成的视频|不满意|重新生成视频|重做视频|重新成片|生成并发布|生成并发布视频|自动生成并发布|执行自动化营销|每日自动化营销|今日自动化营销|运行自动化营销|训练数字人|生成数字人形象|上传照片训练|上传视频训练|形象定制|查看数字人训练|检查数字人训练|数字人训练状态|数字人状态|训练进度|质检结果|训练结果|继续训练)$/.test(text)
    || /训练视频|授权视频|授权文件|trainingVideoUrl|authVideoUrl|authFileUrl|本人照片|形象照片|头像照片|照片\s*[:：]|photoUrl|photo\s*[:：]/i.test(text)
    || /^(绑定数字人ID|设置modelId|设置模型ID|数字人ID是|数字人ID)/i.test(text)) {
    if (/^(确认方案|确认模板|采用方案|采用这个方案)$/.test(text) && marketingPendingPlan()) {
      return confirmMarketingPlanAndStartVideoJob(state, text);
    }
    return marketingAndNotify(state, text);
  }

  if (/^发布抖音$|^开始发布抖音$|^我要发布抖音$/.test(text)) {
    return startPublishFlow(state, text);
  }

  if (/^(更新数据|数据更新)(?:\s*\d{1,3}\s*天)?$/.test(text)) {
    const login = await ensureLoggedInForCommand(state, 'sync_data', text, { days: parseDataDays(text, 90) });
    if (!login.loggedIn) return { action: login.action, text, current: login.current };
    return syncDataAndNotify(state, text);
  }

  if (/^(数据报告|数据分析|分析数据|查看数据|数据复盘)(?:\s*\d{1,3}\s*天)?$/.test(text)) {
    const login = await ensureLoggedInForCommand(state, 'report_data', text, { days: parseDataDays(text, 90) });
    if (!login.loggedIn) return { action: login.action, text, current: login.current };
    return reportDataAndNotify(state, text);
  }

  if (/^(生成下一条视频|下一条视频|内容方案|下一条内容|生成下一条内容|具体文案|生成具体文案|直接生成文案|生成文案|下一条文案)(?:\s*\d{1,3}\s*天)?$/.test(text)) {
    const login = await ensureLoggedInForCommand(state, 'next_video_plan', text, { days: parseDataDays(text, 90) });
    if (!login.loggedIn) return { action: login.action, text, current: login.current };
    return nextVideoPlanAndNotify(state, text);
  }

  if (/^自动回复评论$|^回复评论$|^处理评论$/.test(text)) {
    const login = await ensureLoggedInForCommand(state, 'auto_reply_comment', text);
    if (!login.loggedIn) return { action: login.action, text, current: login.current };
    return autoReplyAndNotify(state, 'comment', text);
  }

  if (/^自动回复私信$|^回复私信$|^处理私信$/.test(text)) {
    const login = await ensureLoggedInForCommand(state, 'auto_reply_dm', text);
    if (!login.loggedIn) return { action: login.action, text, current: login.current };
    return autoReplyAndNotify(state, 'dm', text);
  }

  if (/^自动回复$|^处理互动$|^自动处理互动$/.test(text)) {
    const login = await ensureLoggedInForCommand(state, 'auto_reply_both', text);
    if (!login.loggedIn) return { action: login.action, text, current: login.current };
    return autoReplyAndNotify(state, 'both', text);
  }

  if (/^截图$|^页面截图$|^当前页面截图$/.test(text)) {
    const current = await waitForSettledLoginState();
    if (isBrowserRecoverableFailure(current)) {
      await notifyOnce(state, 'screenshot_browser_recovering', '系统正在恢复抖音浏览器连接，请稍后再试截图。', { force: true });
      return { action: 'screenshot_browser_recovering', text, current };
    }
    const result = captureCurrentPageScreenshot();
    const payload = parseLastJson(result.output);
    if (result.ok && payload?.ok && payload?.filePath && existsSync(payload.filePath)) {
      const feishu = activeFeishuConfig(state);
      await sendFeishuImage(payload.filePath, feishu);
      await notifyOnce(state, `screenshot_done_${Date.now()}`, '截图已发送。', { force: true });
      return { action: 'screenshot_sent', text, result, filePath: payload.filePath };
    }
    await notifyOnce(state, 'screenshot_failed', '截图失败，请稍后重试。', { force: true });
    return { action: 'screenshot_failed', text, result };
  }

  if (/发送二维码|发二维码|二维码|准备好了|已准备好|已过期|过期了|二维码过期/.test(text)) {
    const current = getCurrentLoginState();
    const qrFlowActive = state?.flow?.step === 'waiting_qr_ready' || state?.flow?.step === 'waiting_scan_confirm';
    const shouldSendQr = current.payload?.kind === 'qrcode' || qrFlowActive;
    if (!shouldSendQr) {
      await notifyOnce(state, 'qr_not_needed', '当前不需要二维码。请按页面提示继续，或回复：已登录');
      return {
        action: 'fresh_qr_blocked_by_state',
        text,
        current: current.payload,
      };
    }
    setFlowStep(state, 'waiting_scan_confirm');
    return {
      action: 'fresh_qr',
      text,
      result: withFeishuTargetEnv(state, () => runNode([
        join(__dirname, 'douyin-login-monitor.js'),
        'fresh-qr',
        '--send',
        '--customer-ready',
        '--max-qr-attempts',
        '3',
      ])),
    };
  }

  if (/已完成|完成验证|验证完成|登录好了|已登录/.test(text)) {
    if (flowActive(state) || pendingUpstreamTask(state) || state.pendingCommand || state.pendingVideo || state.pendingPublish) {
      return continueAfterLoginConfirmed(state, text);
    }
  }

  const active = flowActive(state);
  if (!active) {
    if (/^(通过|确认人设|采用这个人设|确认采用|确认人设通过)$/.test(text) && loadPersonaState()?.confirmed) {
      if (!marketingPendingVideoReview()) {
        return startOrResumeOnboardingAfterPersona(state, text, {}, { notifyStart: false });
      }
      return {
        action: 'persona_confirm_ack_ignored_after_confirmed',
        text,
        customerMessage: '',
        customerAlreadyNotifiedByTool: true,
        agentShouldReplyToFeishu: false,
      };
    }
    const personaReply = personaGeneralReply(text);
    if (personaReply) {
      await notifyOnce(state, `persona_general_reply_${Date.now()}`, personaReply.customerMessage, { force: true });
      return { ...personaReply, text };
    }
    return notifyUsage(state, 'ignored_inactive_show_usage', text);
  }

  const downloaded = await downloadAttachment(message);
  if (downloaded) {
    if (!/发布|上传|发抖音|发视频|投稿|publish/i.test(text)) {
      state.pendingVideo = {
        fileName: downloaded.fileName,
        outputPath: downloaded.outputPath,
        bytes: downloaded.bytes,
        receivedAt: new Date().toISOString(),
      };
      setFlowStep(state, 'waiting_publish_confirm');
      await notifyOnce(state, 'video_received_confirm', '已收到视频。确认发布请回复：发布视频');
      return {
        action: 'video_received_waiting_publish_confirm',
        fileName: downloaded.fileName,
        outputPath: downloaded.outputPath,
        bytes: downloaded.bytes,
      };
    }
    setFlowStep(state, 'publishing');
    return publishDownloadedVideo(downloaded, text, state);
  }

  if (/^发布视频$|^确认发布$|^发抖音$/.test(text)) {
    const task = pendingUpstreamTask(state);
    if (task) {
      return publishPreparedTask(task, state);
    }
    if (!state.pendingVideo?.outputPath || !existsSync(state.pendingVideo.outputPath)) {
      if (state.flow?.step === 'publish_failed' || state.flow?.step === 'waiting_publish_confirm') {
        const result = runNode([join(__dirname, 'douyin-cli.js'), 'publish-current-draft']);
        const payload = parseLastJson(result.output);
        if (result.ok) {
          await confirmPublishResult(state, state.pendingPublish?.title || '', 8, 1500);
        } else if (payload?.error === 'publish_verification_required') {
          setFlowStep(state, 'waiting_publish_sms');
          await ensurePublishSmsPrompt(state);
        }
        return { action: 'publish_current_draft_without_pending_video', text, result };
      }
      await notifyOnce(state, 'publish_confirm_without_video', '还没收到视频。请先发送视频文件，或发送包含“视频地址/封面图片/标题/tags”的发布任务。', { force: true });
      return { action: 'publish_confirm_without_video', text };
    }
    const pending = state.pendingVideo;
    state.pendingVideo = null;
    setFlowStep(state, 'publishing');
    return publishDownloadedVideo(pending, text, state);
  }

  if (/^(登录|重新登录|检查登录|我要登录|开始登录)$/.test(text)) {
    setFlowStep(state, 'checking_login');
    return {
      action: 'login_check_notify',
      text,
      result: withFeishuTargetEnv(state, () => runNode([
        join(__dirname, 'douyin-login-monitor.js'),
        'check',
        '--notify',
        '--send-qr',
        'ask',
      ])),
    };
  }

  if (/^发送验证码$|^重发验证码$|^重新发送验证码$/.test(text)) {
    const sms = state.flow?.step === 'waiting_login_sms'
      ? requestLoginSmsCode()
      : requestPublishSmsCode();
    const smsPayload = parseLastJson(sms.output);
    await notifyOnce(state, 'sms_resend_prompt', sms.ok && smsPayload?.ok
      ? '验证码已发送。请直接回复 6 位验证码。'
      : '未确认验证码已发送，请稍后再试。', { force: true });
    return {
      action: 'request_publish_sms_code',
      text,
      result: sms,
    };
  }

  if (/^\d{6}$/.test(text)) {
    const lastCode = state.lastSmsCode || {};
    const currentVerification = getPublishState(state.pendingPublish?.title || '').payload?.verification;
    if (lastCode.code === text && Date.now() - Number(lastCode.submittedAt || 0) < 120000 && !currentVerification?.found) {
      await notifyOnce(state, 'duplicate_sms_code_ignored', '这是刚提交过的验证码。如未通过或已过期，请回复：发送验证码', { force: true });
      return { action: 'duplicate_sms_code_ignored', text: '[6-digit-code]' };
    }
    state.lastSmsCode = { code: text, submittedAt: Date.now() };
    const result = submitVisibleSmsCode(text);
    const payload = parseSubmitPayload(result);
    if (!result.ok) {
      await notifyOnce(state, 'sms_submit_failed', '验证码提交失败或已过期。请回复：发送验证码', { force: true });
    } else if (payload?.phase === 'publish_submitted') {
      const title = state.pendingPublish?.title || '';
      const verified = await notifyPublishDoneAfterVerified(state, title);
      return { action: 'publish_after_sms_checked', text: '[6-digit-code]', result, verified };
    } else if (payload?.phase === 'publish_sms_code_submitted') {
      setFlowStep(state, 'confirming_publish');
      return confirmPublishResult(state, state.pendingPublish?.title || '', 12, 1500);
    } else if (payload?.phase === 'sms_code_submitted' || payload?.phase === 'qrcode') {
      return waitForLoginConfirmed(state);
    } else if (payload?.phase === 'page_loading') {
      return waitForLoginConfirmed(state);
    } else if (payload?.phase === 'logged_in' || payload?.loggedIn === true) {
      return continueAfterLoginConfirmed(state, text);
    } else if (payload?.phase === 'publish_sms_code_input' || payload?.phase === 'sms_code_input') {
      await notifyOnce(state, 'sms_still_needed', '验证码未通过或已过期。请回复：发送验证码', { force: true });
    }
    return { action: 'submit_sms_code', text: '[6-digit-code]', result };
  }

  if (/已完成|完成验证|验证完成|登录好了|已登录/.test(text)) {
    return continueAfterLoginConfirmed(state, text);
  }

  if (/^(通过|确认人设|采用这个人设|确认采用|确认人设通过)$/.test(text) && loadPersonaState()?.confirmed) {
    if (!marketingPendingVideoReview()) {
      return startOrResumeOnboardingAfterPersona(state, text, {}, { notifyStart: false });
    }
    return {
      action: 'persona_confirm_ack_ignored_after_confirmed',
      text,
      customerMessage: '',
      customerAlreadyNotifiedByTool: true,
      agentShouldReplyToFeishu: false,
    };
  }

  const personaReply = personaGeneralReply(text);
  if (personaReply) {
    await notifyOnce(state, `persona_general_reply_${Date.now()}`, personaReply.customerMessage, { force: true });
    return { ...personaReply, text };
  }

  return notifyUsage(state, 'ignored_show_usage', text);
}

async function pollOnce(opts = {}) {
  const state = loadState();
  const nowSeconds = Math.floor(Date.now() / 1000);
  if (opts.init && Number(state.lastCreateTime || 0) === 0) {
    state.lastCreateTime = nowMs();
    saveState(state);
    return { ok: true, initialized: true, lastCreateTime: state.lastCreateTime };
  }

  const reconciled = await reconcileActiveFlow(state);
  const handled = [];
  if (reconciled) {
    handled.push(reconciled);
  }

  const items = [];
  let pageToken = undefined;
  for (let pageNo = 0; pageNo < Number(opts.maxPages || 10); pageNo += 1) {
    const data = await listFeishuMessages({
      sinceSeconds: Number(opts.sinceSeconds || 900),
      endTime: nowSeconds,
      pageSize: Number(opts.pageSize || 50),
      pageToken,
    });
    items.push(...(data.items || []));
    if (!data.has_more || !data.page_token) break;
    pageToken = data.page_token;
  }

  const sortedItems = items
    .filter((item) => item.sender?.sender_type === 'user')
    .sort((a, b) => Number(a.create_time || 0) - Number(b.create_time || 0));

  for (const item of sortedItems) {
    if (!item.message_id || state.seen?.[item.message_id]) continue;
    if (Number(item.create_time || 0) <= Number(state.lastCreateTime || 0)) {
      state.seen[item.message_id] = Number(item.create_time || Date.now());
      continue;
    }
    const full = await getFeishuMessage(item.message_id);
    setActiveFeishuTarget(state, feishuTargetFromMessage(full) || feishuTargetFromMessage(item), 'poll-message');
    const text = extractText(full);
    const result = await handleMessage(full, text, state);
    state.seen[item.message_id] = Number(item.create_time || Date.now());
    state.lastCreateTime = Math.max(Number(state.lastCreateTime || 0), Number(item.create_time || 0));
    handled.push({ messageId: item.message_id, createTime: item.create_time, ...result });
  }
  saveState(state);
  return { ok: true, handled, seen: Object.keys(state.seen || {}).length };
}

async function selfTestStartFlow(opts = {}) {
  const state = loadState();
  if (opts.reset) {
    state.flow = null;
    state.pendingVideo = null;
    state.pendingPublish = null;
    state.pendingUpstreamTask = null;
    state.lastSmsCode = null;
    state.notified = {};
    state.lastCreateTime = nowMs();
    state.resetSchedule = disableSchedulesForReset();
    clearActiveFeishuTarget(state);
  }
  const result = await startPublishFlow(state, '发布抖音');
  saveState(state);
  return { ok: true, mode: 'self-test-start-flow', result, flow: state.flow };
}

async function routeText(opts = {}) {
  if (opts.dryRun) process.env.FEISHU_DRY_RUN = 'true';
  const state = loadState();
  if (opts.reset) {
    state.flow = null;
    state.pendingVideo = null;
    state.pendingPublish = null;
    state.pendingUpstreamTask = null;
    state.lastSmsCode = null;
    state.notified = {};
    state.resetSchedule = disableSchedulesForReset();
    clearActiveFeishuTarget(state);
  }
  const text = String(opts.text || '').trim();
  if (!text) return { ok: false, error: 'text_required' };
  if (opts.messageId) state.lastRouteMessageId = opts.messageId;
  if (opts.messageId && !String(opts.messageId).startsWith('manual_')) {
    markMessageSeen(state, opts.messageId, opts.createTime || Date.now());
    saveState(state);
  }
  let sourceMessage = null;
  if (opts.messageId && !String(opts.messageId).startsWith('manual_')) {
    sourceMessage = await getFeishuMessage(opts.messageId).catch((err) => {
      console.warn(`[feishu] source message lookup failed: ${err.message}`);
      return null;
    });
  }
  const explicitTarget = normalizeChatId(opts.chatId || opts.receiveId);
  if (explicitTarget) {
    setActiveFeishuTarget(state, {
      receiveId: explicitTarget,
      receiveIdType: opts.receiveIdType || 'chat_id',
    }, 'route-text-arg');
  } else if (sourceMessage) {
    setActiveFeishuTarget(state, feishuTargetFromMessage(sourceMessage), 'route-text-message');
  }
  clearStaleFeishuTargetForSourceLessRoute(state, explicitTarget, sourceMessage);
  const message = buildSyntheticMessage(text, {
    messageId: opts.messageId,
    chatId: sourceMessage?.chat_id || explicitTarget || undefined,
    createTime: opts.createTime,
  });
  const reconciled = await reconcileActiveFlow(state);
  const result = await handleMessage(message, text, state);
  saveState(state);
  return {
    ok: true,
    mode: 'route-text',
    text: /^\d{6}$/.test(text) ? '[6-digit-code]' : text,
    reconciled,
    result,
    flow: state.flow,
    pendingVideo: state.pendingVideo ? {
      fileName: state.pendingVideo.fileName,
      outputPath: state.pendingVideo.outputPath,
      bytes: state.pendingVideo.bytes,
    } : null,
    pendingPublish: state.pendingPublish || null,
    pendingUpstreamTask: state.pendingUpstreamTask || null,
  };
}

async function watch(opts = {}) {
  const intervalMs = Number(opts.intervalMs || 3000);
  const maxRounds = opts.maxRounds ? Number(opts.maxRounds) : Infinity;
  const results = [];
  for (let round = 1; round <= maxRounds; round += 1) {
    const result = await pollOnce(opts);
    results.push(result);
    console.log(JSON.stringify({ round, ...result }, null, 2));
    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }
  return { ok: true, rounds: results.length };
}

async function main() {
  const [command = 'poll', ...rest] = process.argv.slice(2);
  const args = parseArgs(rest);
  if (command !== 'poll' && command !== 'watch' && command !== 'self-test-start-flow' && command !== 'route-text') {
    console.error('Usage: node scripts/feishu-reply-watcher.js poll|watch|self-test-start-flow|route-text [--text "..."] [--since-seconds 900] [--interval-ms 3000] [--init] [--reset]');
    process.exit(2);
  }
  const result = command === 'watch'
    ? await watch(args)
    : (command === 'self-test-start-flow'
      ? await selfTestStartFlow(args)
      : (command === 'route-text' ? await routeText(args) : await pollOnce(args)));
  console.log(JSON.stringify(result, null, 2));
}

main().catch((err) => {
  console.log(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
  process.exit(1);
});
