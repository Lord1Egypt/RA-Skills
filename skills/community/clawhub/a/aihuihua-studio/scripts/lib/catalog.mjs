/**
 * 模型目录：每个模型叫什么、能干什么、收哪些参数、多少点数、怎么调网站接口。
 *
 * SKILL.md 里的能力表、`models` 命令的输出、`gen` 命令的参数校验都从这里来，
 * 改模型只改这一处。价格跟网站后端的配置走（superx 在 src/config/config.js，
 * aihuihua 在 .env），网站调价了要同步改这里再发新版技能 —— 真正扣多少以网站为准，
 * 这里的数字只用来提前告诉用户。
 *
 * 选项的 key 就是命令行参数名（--size、--image …）。type:
 *   enum   取 values 之一          int   整数（min/max）
 *   bool   开关（--no-xxx 关掉）   text  任意文本
 *   file   本地路径或 URL，自动上传成 URL；multiple 表示可重复传多次
 */
import crypto from 'node:crypto';
import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
import { ApiError, requestJson, requestStream } from './http.mjs';
import { SITE, api, artApi, fullUrl, readState, writeState } from './store.mjs';
import { ensureUrl, ensureUrls } from './upload.mjs';

const BOTH = ['superx', 'aihuihua'];
const site = () => SITE.id;
const P = () => SITE.pointName; // superx 叫「点数」，aihuihua 叫「积分」

// 文字转语音按字数计费：系数和后端 ttsMiddleware 的 POINTS_PER_CHAR 一致（火山价换算），调价两边一起改
const TTS_POINTS_PER_CHAR = (3 * 4) / 10000 / 0.068;
const TTS_MAX_CHARS = 5000;
const ttsPoints = (text) => Math.max(1, Math.ceil([...String(text).trim()].length * TTS_POINTS_PER_CHAR));

// ─── 通用执行器 ────────────────────────────────────────────────

/** 流式生图：把进度打出来，返回终态对象；终态带非 0 code 就抛错 */
async function runStream(endpoint, body, { token, log }) {
  let last = '';
  const events = await requestStream(artApi(endpoint), {
    data: body,
    token,
    onEvent: (e) => {
      const text = [e.progress, e.status].filter(Boolean).join(' ');
      if (text && text !== last && !e.ps) {
        last = text;
        log(`  … ${text}`);
      }
    },
  });
  const final = [...events].reverse().find((e) => e.code !== undefined || e.state === 'complete' || e.buttons || e.id)
    || events[events.length - 1];
  if (!final) throw new ApiError('网站没有返回结果，可以稍后用 history 看看有没有生成出来');
  if (final.code !== undefined && final.code !== 0 && final.code !== '0') {
    throw new ApiError(final.message || final.msg || `生成失败（${final.code}）`, { code: final.code, body: final });
  }
  return final;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const newRequestId = () => `agent_${Date.now().toString(36)}_${crypto.randomBytes(8).toString('hex')}`;

/** 视频这类异步任务：反复查直到成功/失败，或者超时（超时不算失败，任务还在网站上跑） */
async function pollTask(readPath, { token, log, timeoutSec = 1800, interval = 10 }) {
  const deadline = Date.now() + timeoutSec * 1000;
  let lastStatus = '';
  for (;;) {
    const res = await requestJson(artApi(readPath), { token, timeout: 30_000 });
    const t = res.data || {};
    const extra = t.status === 'queued' && t.queue_position ? `，前面还有 ${t.queue_position} 个`
      : t.progress?.total_steps ? `，第 ${t.progress.step}/${t.progress.total_steps} 步` : '';
    // 步数每步都变，按 10% 左右的粒度打，别刷屏
    const key = `${t.status}${t.queue_position ?? ''}${t.progress?.total_steps ? Math.floor((t.progress.step / t.progress.total_steps) * 10) : ''}`;
    if (key !== lastStatus) {
      lastStatus = key;
      log(`  … 任务 ${t.id} 状态：${STATUS_TEXT[t.status] || t.status}${extra}${t.message ? `（${t.message}）` : ''}`);
    }
    if (t.status === 'succeeded') return t;
    if (t.status === 'failed') throw new ApiError(t.error || '视频生成失败，点数已退回', { code: 'TASK_FAILED', body: t });
    if (Date.now() > deadline) {
      const err = new ApiError(`等了 ${Math.round(timeoutSec / 60)} 分钟还没出片，任务还在网站上继续跑，稍后用 task 命令接着查`, { code: 'TASK_PENDING', body: t });
      err.pending = t;
      throw err;
    }
    await sleep(interval * 1000);
  }
}

const STATUS_TEXT = {
  submitting: '提交中', queued: '排队中', running: '生成中', processing: '生成中', storing: '已生成，正在保存',
  succeeded: '已完成', failed: '失败', unknown: '提交结果待核实', submission_unknown: '提交结果待核实',
};

// ─── 专属版：视频只有本地部署的 MiniMax H3（site.json 的 localH3），走网站的 /minimax-h3-local 扣点接口（网站 H3 半价）──────────

const LOCAL_ETA = { 4: '约 5 分钟', 5: '约 5～6 分钟', 6: '约 7 分钟' };
const localEta = (d) => LOCAL_ETA[d] || (d <= 10 ? '约 8～12 分钟' : '约 13～20 分钟');
const localH3Points = (duration) => Math.ceil((500 * duration * 1000) / 2 / 68000);

const LOCAL_H3_MODEL = {
  id: 'minimax-h3',
  type: 'video',
  sites: [],
  local: true,
  name: 'MiniMax H3（海螺，专属本地版）',
  summary: '海螺 H3 视频（专属本地部署，价格是网站 H3 的一半）：运镜和物理效果好，自带音效；文生视频、首帧、首尾帧；4～15 秒，768P',
  details: [
    '文生视频：只写提示词，--ratio 选比例（默认 16:9）；首帧图生视频：--first；首尾帧：--first + --last（按首帧比例出片）',
    '只有 768P（16:9 出 1344×768，24fps）；不支持 2K、参考图 / 参考视频 / 参考音频',
    '生成时间（轮到这条之后，单卡串行，前面有任务还要排队）：4 秒约 5 分钟、5 秒约 5～6 分钟、6 秒约 7 分钟、10 秒约 11～12 分钟、15 秒约 16～20 分钟（10 秒以上为估算）；提交前把预计时间告诉用户',
    '同一个账号同时最多 3 个没完成的视频任务；超过 8 分钟的建议 --no-wait 提交，之后用 task 取结果（task 输出有排队位置和「第 x/25 步」，可估剩余时间）',
    '提示词里把人物站位、朝向、运镜写清楚；不满意可以换 --seed 再来',
    `提交时预扣${P()}，生成失败全额退回`,
  ],
  options: [
    { key: 'duration', type: 'int', min: 4, max: 15, default: 6, desc: '时长（秒）' },
    { key: 'ratio', type: 'enum', values: ['16:9', '21:9', '4:3', '1:1', '3:4', '9:16'], desc: '比例（文生视频用，默认 16:9；有首帧时按首帧比例）' },
    { key: 'first', type: 'file', desc: '首帧图' },
    { key: 'last', type: 'file', desc: '尾帧图（必须同时给 --first）' },
    { key: 'seed', type: 'int', min: 0, max: 2 ** 53, desc: '随机种子，同参数同种子结果可复现' },
    { key: 'wait', type: 'bool', default: true, desc: '等出片并下载，--no-wait 只提交' },
  ],
  costText: () => `每秒约 3.7${P()}（6 秒 ${localH3Points(6)}${P()}，15 秒 ${localH3Points(15)}${P()}）`,
  cost: (o) => localH3Points(o.duration),
  validate(o) {
    if (o.last && !o.first) return '--last 尾帧必须同时给 --first 首帧';
    return '';
  },
  async run({ prompt, o, token, log }) {
    const media = [];
    if (o.first) media.push({ role: 'first_frame', url: await ensureUrl(o.first, token) });
    if (o.last) media.push({ role: 'last_frame', url: await ensureUrl(o.last, token) });
    const body = {
      prompt, resolution: '768P', duration: o.duration, ratio: o.first ? 'adaptive' : (o.ratio || '16:9'), aigc_watermark: false, media,
    };
    if (o.seed !== undefined) body.seed = o.seed;
    const quote = (await requestJson(artApi('minimax-h3-local/quote'), { data: body, token, timeout: 120_000 })).data;
    const res = await requestJson(artApi('minimax-h3-local/tasks'), {
      data: { ...body, request_id: newRequestId(), quote_token: quote.quote_token }, token, timeout: 120_000,
    });
    const task = res.data;
    if (task.status === 'failed') throw new ApiError(`视频提交失败：${task.error || '未知错误'}（${P()}已退回）`, { code: 'TASK_FAILED', body: task });
    log(`  已提交：任务 ${task.id}，预扣 ${task.reserved_points} ${P()}；${o.duration} 秒视频生成${localEta(o.duration)}，前面有任务还要排队`);
    rememberTask({ model: 'minimax-h3', id: task.id });
    if (o.wait === false) return { cost: task.reserved_points, pending: { model: 'minimax-h3', id: task.id, status: task.status } };
    const done = await pollTask(`minimax-h3/tasks/${task.id}`, { token, log, timeoutSec: 3600, interval: 15 });
    return { cost: done.points, results: [{ kind: 'video', url: fullUrl(done.video_url), id: done.id }] };
  },
  async resume({ id: taskId, token, log, wait }) {
    if (!wait) return { task: (await requestJson(artApi(`minimax-h3/tasks/${taskId}`), { token })).data };
    const done = await pollTask(`minimax-h3/tasks/${taskId}`, { token, log, timeoutSec: 3600, interval: 15 });
    return { cost: done.points, results: [{ kind: 'video', url: fullUrl(done.video_url), id: done.id }] };
  },
};

const img = (url, extra = {}) => ({ kind: 'image', url: fullUrl(url, extra.paintingType), ...extra });

// ─── 价格 ──────────────────────────────────────────────────────

// 和网站 GPT_IMAGE_25_COST_TABLE 一致（2026-09-11 定版），每张参考图另加 2
// auto：改图跟随原图比例（总像素同 1536x1024），按 1024 档计价
const GPT25_SIZES = ['auto', '1024x1024', '1536x1024', '1024x1536', '2048x2048', '3840x2160'];
const GPT25_QUALITIES = ['low', 'medium', 'high', 'xhigh', 'max'];
const GPT25_TABLE = {
  low: [4, 4, 4, 4, 6, 8],
  medium: [6, 6, 6, 6, 8, 12],
  high: [10, 10, 10, 10, 25, 30],
  xhigh: [22, 22, 22, 22, 45, 50],
  max: [50, 50, 50, 50, 100, 110],
};
const gpt25Cost = (o) => GPT25_TABLE[o.quality][GPT25_SIZES.indexOf(o.size)] + 2 * (o.image || []).length;

// Seedance：和网站 src/seedance/contract.js 同一个公式，68 元 = 1000 点，整次任务向上取整
const SEEDANCE_PIXELS = { '480p': 864 * 496, '720p': 1280 * 720, '1080p': 1920 * 1080, '4k': 3840 * 2160 };
const SEEDANCE = {
  'seedance-2.5': { name: '即梦 Seedance 2.5', desc: '最强模型，画面与音效同步生成，最长 30 秒', prices: { '480p': 70, '720p': 70, '1080p': 77 }, duration: [4, 30], modes: ['text', 'first', 'frames', 'reference'], maxRefs: 9, audio: true, videoPrices: { '480p': 42, '720p': 42, '1080p': 46 }, videos: [10, 30, 30] },
  'seedance-2.0': { name: '即梦 Seedance 2.0', desc: '全模态能力，支持 1080P 与 4K 输出', prices: { '480p': 46, '720p': 46, '1080p': 51, '4k': 26 }, duration: [4, 15], modes: ['text', 'first', 'frames', 'reference'], maxRefs: 9, audio: true, videoPrices: { '480p': 28, '720p': 28, '1080p': 31, '4k': 16 }, videos: [3, 15, 15] },
  'seedance-2.0-fast': { name: '即梦 Seedance 2.0 Fast', desc: '极速推理，效果接近 2.0', prices: { '480p': 37, '720p': 37 }, duration: [4, 15], modes: ['text', 'first', 'frames', 'reference'], maxRefs: 9, audio: true, videoPrices: { '480p': 22, '720p': 22 }, videos: [3, 15, 15] },
  'seedance-2.0-mini': { name: '即梦 Seedance 2.0 mini', desc: '极致性价比，出片更快', prices: { '480p': 23, '720p': 23 }, duration: [4, 15], modes: ['text', 'first', 'frames', 'reference'], maxRefs: 9, audio: true, videoPrices: { '480p': 14, '720p': 14 }, videos: [3, 15, 15] },
  'seedance-1.0-pro': { name: '即梦 Seedance 1.0 Pro', desc: '经典版本，价格最低', prices: { '480p': 15, '720p': 15, '1080p': 15 }, duration: [2, 12], modes: ['text', 'first', 'frames'], maxRefs: 0, audio: false, videoPrices: {}, videos: [0, 0, 0] },
};
// inputSeconds：参考视频合计秒数（每段向上取整）。带视频时换「输入含视频」单价、输入时长计入、至少按 2 倍输出时长，
// 是网站提交时的预扣上限；出片后网站按上游实际用量结算，多扣的退回。
const seedancePoints = (model, resolution, duration, inputSeconds = 0) => {
  const spec = SEEDANCE[model];
  const unit = inputSeconds ? spec.videoPrices[resolution] : spec.prices[resolution];
  const seconds = inputSeconds ? Math.max(duration + inputSeconds, duration * 2) : duration;
  return Math.ceil(((seconds * 24 + 1) * SEEDANCE_PIXELS[resolution] * unit) / (1024 * 68000));
};
// 用本机 ffprobe 读参考视频时长（本地文件或 URL）；没装 ffprobe 或读不出返回 null
function probeSeconds(file) {
  const r = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', String(file)], { encoding: 'utf8', timeout: 30_000 });
  const v = Number(String(r.stdout || '').trim());
  return r.status === 0 && Number.isFinite(v) && v > 0 ? v : null;
}
// 参考视频合计秒数（预估价用，和网站后端 checkVideos 一样每段减 0.1 秒再向上取整）；有一段读不出就按模型允许的最长合计算（只会估高）
function refVideoSeconds(spec, files = []) {
  if (!files.length) return 0;
  const secs = files.map(probeSeconds);
  if (secs.some((v) => v === null)) return spec.videos[2];
  return secs.reduce((sum, v) => sum + Math.ceil(v - 0.1), 0);
}

// MJ 按钮：和网站 config.mjButtons 一致，别名给 agent 用
const MJ_ACTIONS = [
  ['U1', 'MJ::JOB::upsample::1', 2, '放大第 1 张'], ['U2', 'MJ::JOB::upsample::2', 2, '放大第 2 张'],
  ['U3', 'MJ::JOB::upsample::3', 2, '放大第 3 张'], ['U4', 'MJ::JOB::upsample::4', 2, '放大第 4 张'],
  ['V1', 'MJ::JOB::variation::1', 8, '以第 1 张为基础出 4 张变体'], ['V2', 'MJ::JOB::variation::2', 8, '以第 2 张出变体'],
  ['V3', 'MJ::JOB::variation::3', 8, '以第 3 张出变体'], ['V4', 'MJ::JOB::variation::4', 8, '以第 4 张出变体'],
  ['zoom1.5', 'MJ::Outpaint::75', 8, '画面向外扩 1.5 倍（只对放大后的单图有效）'],
  ['zoom2', 'MJ::Outpaint::50', 16, '画面向外扩 2 倍（只对放大后的单图有效）'],
  ['pan-left', 'MJ::JOB::pan_left', 8, '向左扩图'], ['pan-right', 'MJ::JOB::pan_right', 8, '向右扩图'],
  ['pan-up', 'MJ::JOB::pan_up', 8, '向上扩图'], ['pan-down', 'MJ::JOB::pan_down', 8, '向下扩图'],
];

// ─── 模型 ──────────────────────────────────────────────────────

const gpt25 = (variant) => ({
  id: `gpt-image-2.5-${variant}`,
  type: 'image',
  sites: BOTH,
  name: `GPT Image 2.5 ${variant === 'flare' ? 'Flare' : 'Sunburst'}`,
  summary: variant === 'flare'
    ? 'OpenAI 最新一代生图，速度快、性价比高：文生图、精确改图、多图融合、局部重绘、透明背景'
    : 'GPT Image 2.5 精细版：细节和文字渲染更好、更听话，出图更慢；适合海报、带字设计、产品精修',
  details: [
    '没传 --image 是文生图；传 1～10 张 --image 是改图 / 多图参考（保留人物、商品、版式）',
    '--mask 配合 1 张 --image 做局部重绘：mask 是和原图同尺寸的 PNG，透明区域是要重画的地方',
    '中英文提示词都行，能准确渲染图片里的文字（海报、包装、信息图）',
    '--background transparent 出透明底（需 png 或 webp），做贴纸、图标、抠好的商品图',
  ],
  options: [
    { key: 'size', type: 'enum', values: GPT25_SIZES, default: '1024x1024', desc: '尺寸：自动 / 方图 / 横图 3:2 / 竖图 2:3 / 2K 方图 / 4K 横图' },
    { key: 'quality', type: 'enum', values: GPT25_QUALITIES, default: 'high', desc: '画质，越高越精细越慢越贵' },
    { key: 'image', type: 'file', multiple: true, max: 10, desc: '参考图 / 要改的原图，本地路径或 URL，可传多次' },
    { key: 'mask', type: 'file', desc: '局部重绘蒙版（PNG，透明处重画），只能配 1 张 --image' },
    { key: 'format', type: 'enum', values: ['png', 'jpeg', 'webp'], default: 'png', desc: '输出格式' },
    { key: 'background', type: 'enum', values: ['auto', 'transparent', 'opaque'], default: 'auto', desc: '背景；transparent 透明底' },
  ],
  costText: () => `按画质×尺寸计价，每张参考图 +2${P()}。1K（auto 与 1024/1536 三种尺寸）：low 4 / medium 6 / high 10 / xhigh 22 / max 50；2048x2048：6 / 8 / 25 / 45 / 100；3840x2160：8 / 12 / 30 / 50 / 110`,
  cost: gpt25Cost,
  validate(o) {
    if (o.mask && (o.image || []).length !== 1) return '局部重绘（--mask）需要且只能传 1 张 --image';
    if (o.background === 'transparent' && o.format === 'jpeg') return '透明背景只能配合 png 或 webp';
    return '';
  },
  async run({ prompt, o, token, log }) {
    const body = {
      prompt, variant, size: o.size, quality: o.quality, output_format: o.format, background: o.background,
    };
    if (o.image?.length) body.image_urls = await ensureUrls(o.image, token);
    if (o.mask) body.mask_url = await ensureUrl(o.mask, token);
    const final = await runStream('gpt-image-25-generate', body, { token, log });
    return { cost: final.data?.cost, results: [img(final.data.img_url, { id: final.data.id })] };
  },
});

const MODELS = [
  gpt25('flare'),
  gpt25('sunburst'),
  {
    id: 'gpt-image-2',
    type: 'image',
    sites: BOTH,
    name: 'GPT Image 2',
    summary: '上一代 GPT 生图，对话式理解提示词，支持参考图改图；固定价格',
    details: ['可传最多 10 张 --image 做参考 / 改图', '尺寸由模型按提示词自动决定（可以在提示词里写「横版 16:9」）'],
    options: [{ key: 'image', type: 'file', multiple: true, max: 10, desc: '参考图，本地路径或 URL，可传多次' }],
    costText: () => `每张 8${P()}`,
    cost: () => 8,
    async run({ prompt, o, token, log }) {
      const body = { prompt };
      if (o.image?.length) body.image_urls = await ensureUrls(o.image, token);
      const final = await runStream('gpt-image-2-generate', body, { token, log });
      return { cost: final.data?.cost ?? 8, results: [img(final.data.img_url, { id: final.data.id })] };
    },
  },
  {
    id: 'nano-banana-pro',
    type: 'image',
    sites: BOTH,
    name: 'Nano Banana Pro（Gemini 3 Pro Image）',
    summary: 'Google 的生图 / 改图模型：人物一致性强、换装换背景、多图合成、风格迁移（吉卜力、手办等）',
    details: ['可传多张 --image：保持同一个人 / 物体，换场景、换衣服、合成到一张图', '很适合「把这张照片改成 X 风格」这类编辑'],
    options: [{ key: 'image', type: 'file', multiple: true, max: 10, desc: '参考图，本地路径或 URL，可传多次' }],
    costText: () => `每张 8${P()}`,
    cost: () => 8,
    async run({ prompt, o, token, log }) {
      const body = { prompt };
      if (o.image?.length) body.image_urls = await ensureUrls(o.image, token);
      const final = await runStream('nanobanana-generate', body, { token, log });
      return { cost: final.data?.cost ?? 8, results: [img(final.data.img_url, { id: final.data.id })] };
    },
  },
  {
    id: 'gpt-4o-image',
    type: 'image',
    sites: BOTH,
    name: 'GPT-4o 图片（gpt-image-1）',
    summary: 'GPT-4o 生图 / 图片编辑，一次可出多张',
    details: ['--n 一次出 1～10 张，按张计费', '传 --image 走编辑模式（最多 10 张参考图）'],
    options: [
      { key: 'n', type: 'int', min: 1, max: 10, default: 1, desc: '张数' },
      { key: 'size', type: 'enum', values: ['auto', '1024x1024', '1536x1024', '1024x1536'], default: 'auto', desc: '尺寸' },
      { key: 'image', type: 'file', multiple: true, max: 10, desc: '参考图 / 要编辑的图' },
    ],
    costText: () => `每张 8${P()}（--n 张数 × 8）`,
    cost: (o) => 8 * o.n,
    async run({ prompt, o, token, log }) {
      const body = { prompt, n: o.n, size: o.size };
      if (o.image?.length) body.images = await ensureUrls(o.image, token);
      const final = await runStream('gpt4o-image', body, { token, log });
      const list = final.data?.result || [];
      return { cost: final.data?.cost, results: list.map((r) => img(r.img_url, { id: r.id })) };
    },
  },
  {
    id: 'seedream-5',
    type: 'image',
    sites: BOTH,
    name: '即梦 Seedream 5.0（豆包）',
    summary: '字节即梦 / 豆包 Seedream 5.0：2K～3K 高清大图，中文理解好；支持组图（一次多张连贯图）和故事书（分镜 + 文案）',
    details: [
      '--mode single 单张；group 组图（--count 1～15 张同一主题、风格统一）；story 故事书（自动写故事 + 每页配图）',
      '可传 --image 做参考图（人物 / 风格保持）',
      '尺寸都是 2K 级别以上，适合做壁纸、海报、绘本',
    ],
    options: [
      { key: 'size', type: 'enum', values: ['2048x2048', '2304x1728', '1728x2304', '2560x1440', '1440x2560', '2496x1664', '1664x2496', '3024x1296'], default: '2048x2048', desc: '尺寸：1:1 / 4:3 / 3:4 / 16:9 / 9:16 / 3:2 / 2:3 / 21:9' },
      { key: 'mode', type: 'enum', values: ['single', 'group', 'story'], default: 'single', desc: '单张 / 组图 / 故事书' },
      { key: 'count', type: 'int', min: 1, max: 15, desc: '组图、故事书的张数' },
      { key: 'image', type: 'file', multiple: true, max: 10, desc: '参考图' },
    ],
    costText: () => `每张 8${P()}，组图 / 故事书按实际生成张数计`,
    cost: (o) => 8 * (o.mode === 'single' ? 1 : (o.count || 1)),
    async run({ prompt, o, token, log }) {
      const body = { prompt, size: o.size, mode: o.mode };
      if (o.count && o.mode !== 'single') body.count = o.count;
      if (o.image?.length) {
        const urls = await ensureUrls(o.image, token);
        body.image = urls.length === 1 ? urls[0] : urls;
      }
      const final = await runStream('jimeng4-generate', body, { token, log });
      const result = final.data?.result || {};
      const images = (result.images || []).map((x) => (typeof x === 'string' ? x : x.url || x.img_url || x.image_url)).filter(Boolean);
      const out = { cost: final.data?.cost, results: images.map((u) => img(u, { id: final.data.id })) };
      if (o.mode === 'story') out.story = result;
      return out;
    },
  },
  {
    id: 'midjourney',
    type: 'image',
    sites: BOTH,
    name: 'Midjourney',
    summary: '艺术感最强的生图：插画、概念图、摄影风格；一次出 4 张的四宫格，之后可以放大（U）、变体（V）、扩图',
    details: [
      '提示词最好用英文，可以带 MJ 参数放在最后：--ar 16:9（比例）、--v 7 / --niji 6（版本）、--s 250（风格化）、--q 1、--no text、--seed 123、--sref <图片URL>（风格参考）、--cref <图片URL>（人物参考）',
      '中文会被自动翻译成英文；参考图直接把图片 URL 放在提示词最前面，和文字用空格隔开',
      '出图后用 mj-action 命令：U1～U4 放大单张（2 点），V1～V4 出变体（8 点），zoom1.5 / zoom2、pan-left/right/up/down 扩图；一小时内有效',
    ],
    options: [],
    costText: () => `出图 8${P()}；U 放大 2；V 变体 8；zoom1.5 8；zoom2 16；pan 扩图 8`,
    cost: () => 8,
    async run({ prompt, token, log }) {
      const final = await runStream('imagine', { prompt }, { token, log });
      return mjResult(final, token);
    },
  },
  {
    id: 'upscale',
    type: 'tool',
    sites: BOTH,
    name: '图片高清放大',
    summary: 'AI 超分辨率放大，老照片 / 小图变清晰',
    details: ['--image 传 1 张（本地或 URL），--scale 放大倍数'],
    noPrompt: true,
    options: [
      { key: 'image', type: 'file', required: true, desc: '要放大的图片' },
      { key: 'scale', type: 'int', min: 2, max: 4, default: 2, desc: '放大倍数 2～4' },
    ],
    costText: () => `倍数² × 5 + 10${P()}：2 倍 30，3 倍 55，4 倍 90`,
    cost: (o) => o.scale * o.scale * 5 + 10,
    async run({ o, token }) {
      const url = await ensureUrl(o.image, token);
      const res = await requestJson(artApi('image-upscale'), { data: { img_url: url, scale_num: o.scale }, token, timeout: 10 * 60_000 });
      return { results: [img(res.data?.ossPath || res.data?.img_url)] };
    },
  },
  {
    id: 'faceswap',
    type: 'tool',
    sites: BOTH,
    name: 'AI 换脸',
    summary: '把一张人脸照片换到底图人物脸上',
    details: ['--image 底图（被换脸的那张，可以是 AI 生成的图）；--face 清晰的正脸照片，别戴眼镜效果更好'],
    noPrompt: true,
    options: [
      { key: 'image', type: 'file', required: true, desc: '底图' },
      { key: 'face', type: 'file', required: true, desc: '人脸照片' },
    ],
    costText: () => `每次 60${P()}`,
    cost: () => 60,
    async run({ o, token }) {
      const source = await ensureUrl(o.image, token);
      const target = await ensureUrl(o.face, token);
      const res = await requestJson(artApi('face-swap'), { data: { source, target }, token, timeout: 10 * 60_000 });
      return { results: [img(res.data?.ossPath || res.data?.img_url)] };
    },
  },
  {
    id: 'remove-bg',
    type: 'tool',
    sites: BOTH,
    name: 'AI 抠图（去背景）',
    summary: '一键去掉背景，输出透明底 PNG（RMBG-2.0，发丝级边缘）',
    details: ['--image 传 1 张（本地或 URL）；自动识别人物 / 商品 / 动物等主体，失败不扣点'],
    noPrompt: true,
    options: [{ key: 'image', type: 'file', required: true, desc: '要抠图的图片' }],
    costText: () => `每次 5${P()}`,
    cost: () => 5,
    async run({ o, token }) {
      const imgUrl = await ensureUrl(o.image, token);
      const res = await requestJson(artApi('remove-bg'), { data: { imgUrl }, token, timeout: 5 * 60_000 });
      return { results: [img(res.data?.ossPath || res.data?.url, { ext: 'png' })] };
    },
  },
  ...Object.entries(SEEDANCE).map(([id, spec]) => ({
    id,
    type: 'video',
    sites: BOTH,
    name: spec.name,
    summary: `${spec.desc}；${spec.audio ? '自带音效 / 配乐' : '无声'}，${spec.duration[0]}～${spec.duration[1]} 秒`,
    details: [
      `生成方式（--mode，不传按图片张数自动选）：text 文生视频；first 首帧图生视频（1 张 --image）；frames 首尾帧（2 张 --image，按顺序首帧、尾帧）${spec.maxRefs ? `；reference 全能参考（0～${spec.maxRefs} 张 --image，保持人物 / 商品 / 场景）` : ''}`,
      ...(spec.videos[0] ? [`参考视频（白模动画、动作 / 运镜参考）：--ref-video 最多 ${spec.videos[0]} 段，合计 ≤${spec.videos[2]} 秒，单段 ≥2 秒，MP4/MOV ≤200MB、24～60fps、480P～4K；传了自动用 reference 方式，可以不传 --image；提示词里用「视频1」「图1」指代`] : []),
      `分辨率：${Object.keys(spec.prices).join(' / ')}；比例：16:9、4:3、1:1、3:4、9:16、21:9，图生视频可用 adaptive（跟随图片）`,
      '提交后一般 1～10 分钟出片，命令会一直等到出片并下载；--no-wait 只提交，之后用 task 命令查',
      spec.videos[0] ? '提交时一次扣足点数，失败全额退回；带参考视频时按「输入含视频」单价、输入时长也计费，提交按上限预扣，出片后按实际用量退差额' : '提交时一次扣足点数，失败全额退回',
    ],
    options: [
      { key: 'image', type: 'file', multiple: true, max: Math.max(2, spec.maxRefs), desc: '首帧 / 首尾帧 / 参考图' },
      ...(spec.videos[0] ? [{ key: 'ref-video', type: 'file', multiple: true, max: spec.videos[0], desc: '参考视频（白模 / 动作参考，mp4/mov）' }] : []),
      { key: 'mode', type: 'enum', values: spec.modes, desc: '生成方式，不传自动判断' },
      { key: 'resolution', type: 'enum', values: Object.keys(spec.prices), default: Object.keys(spec.prices).includes('720p') ? '720p' : '480p', desc: '分辨率' },
      { key: 'duration', type: 'int', min: spec.duration[0], max: spec.duration[1], default: 5, desc: '时长（秒）' },
      { key: 'ratio', type: 'enum', values: ['16:9', '4:3', '1:1', '3:4', '9:16', '21:9', 'adaptive'], desc: '画面比例，文生视频默认 16:9，图生视频默认 adaptive' },
      ...(spec.audio ? [{ key: 'audio', type: 'bool', default: true, desc: '同时生成音效，--no-audio 关掉' }] : []),
      { key: 'wait', type: 'bool', default: true, desc: '等出片并下载，--no-wait 只提交' },
    ],
    costText: () => {
      const rows = Object.keys(spec.prices).map((r) => `${r} 每 5 秒约 ${seedancePoints(id, r, 5)}`);
      return `按分辨率 × 时长计价（${P()}）：${rows.join('，')}${spec.videos[0] ? '；带参考视频时参考视频时长也计费（按上限预扣、出片后按实际结算）' : ''}；具体以 price 命令为准`;
    },
    cost: (o) => seedancePoints(id, o.resolution, o.duration, refVideoSeconds(spec, o['ref-video'])),
    prepare(o) {
      const n = (o.image || []).length;
      if (!o.mode) o.mode = (o['ref-video'] || []).length ? 'reference' : n === 0 ? 'text' : n === 1 ? 'first' : n === 2 ? 'frames' : 'reference';
      if (!o.ratio) o.ratio = o.mode === 'text' || o.mode === 'reference' ? '16:9' : 'adaptive';
    },
    validate(o) {
      const n = (o.image || []).length;
      const v = (o['ref-video'] || []).length;
      if (v && o.mode !== 'reference') return '--ref-video 只能用在 reference（全能参考）方式，不能和首帧 / 首尾帧混用';
      if (v > spec.videos[0]) return `${spec.name} 最多 ${spec.videos[0]} 段 --ref-video`;
      const need = { text: [0, 0], first: [1, 1], frames: [2, 2], reference: [v ? 0 : 1, spec.maxRefs] }[o.mode];
      if (!spec.modes.includes(o.mode)) return `${spec.name} 不支持 ${o.mode} 方式`;
      if (n < need[0] || n > need[1]) return { text: '文生视频不要传 --image', first: '首帧模式传 1 张 --image', frames: '首尾帧模式传 2 张 --image', reference: spec.videos[0] ? `全能参考传 1～${spec.maxRefs} 张 --image 或至少 1 段 --ref-video` : `参考图模式传 1～${spec.maxRefs} 张 --image` }[o.mode];
      if (o.mode === 'text' && o.ratio === 'adaptive') return '文生视频请指定固定比例（--ratio 16:9 等）';
      return '';
    },
    async run({ prompt, o, token, log }) {
      const body = {
        request_id: newRequestId(), model: id, mode: o.mode, prompt, resolution: o.resolution, duration: o.duration, ratio: o.ratio,
        audio: spec.audio ? o.audio !== false : false, images: await ensureUrls(o.image, token),
        ...((o['ref-video'] || []).length ? { videos: await ensureUrls(o['ref-video'], token) } : {}),
      };
      const res = await requestJson(artApi('seedance/tasks'), { data: body, token, timeout: 120_000 });
      const task = res.data;
      log(`  已提交：任务 ${task.id}，预扣 ${task.reserved_points ?? task.points ?? '?'} ${P()}`);
      rememberTask({ model: id, id: task.id });
      if (o.wait === false) return { cost: task.points, pending: { model: id, id: task.id, status: task.status } };
      const done = await pollTask(`seedance/tasks/${task.id}`, { token, log });
      return { cost: done.points, results: [{ kind: 'video', url: fullUrl(done.video_url), id: done.id }] };
    },
    async resume({ id: taskId, token, log, wait }) {
      if (!wait) {
        const res = await requestJson(artApi(`seedance/tasks/${taskId}`), { token });
        return { task: res.data };
      }
      const done = await pollTask(`seedance/tasks/${taskId}`, { token, log });
      return { cost: done.points, results: [{ kind: 'video', url: fullUrl(done.video_url), id: done.id }] };
    },
  })),
  {
    id: 'minimax-h3',
    type: 'video',
    sites: BOTH,
    name: 'MiniMax H3（海螺）',
    summary: '海螺 H3 视频：运镜和物理效果好，支持首尾帧、多图参考，还能用参考视频 / 参考音频；4～15 秒，768P 或 2K',
    details: [
      '文生视频：只写提示词；首帧图生视频：--first；首尾帧：--first + --last（比例自动 adaptive）',
      '参考素材（不能和首尾帧混用）：--image 参考图 ≤9 张、--ref-video 参考视频 ≤3 个、--ref-audio 参考音频 ≤3 个',
      '提交前先向网站报价，按官方价计费：768P 约 7.4 点/秒，2K 约 11.8 点/秒，参考图超过 5 张每张 +3 点、参考视频按时长另计；结束后按实际用量多退少不补',
      '一般 3～15 分钟出片；--no-wait 只提交，之后用 task 命令查',
    ],
    options: [
      { key: 'resolution', type: 'enum', values: ['768P', '2K'], default: '768P', desc: '分辨率' },
      { key: 'duration', type: 'int', min: 4, max: 15, default: 6, desc: '时长（秒）' },
      { key: 'ratio', type: 'enum', values: ['16:9', '21:9', '4:3', '1:1', '3:4', '9:16', 'adaptive'], desc: '比例，首尾帧必须 adaptive（自动）' },
      { key: 'first', type: 'file', desc: '首帧图' },
      { key: 'last', type: 'file', desc: '尾帧图（必须同时给 --first）' },
      { key: 'image', type: 'file', multiple: true, max: 9, desc: '参考图' },
      { key: 'ref-video', type: 'file', multiple: true, max: 3, desc: '参考视频（mp4）' },
      { key: 'ref-audio', type: 'file', multiple: true, max: 3, desc: '参考音频' },
      { key: 'watermark', type: 'bool', default: false, desc: '加 AI 生成水印' },
      { key: 'wait', type: 'bool', default: true, desc: '等出片并下载，--no-wait 只提交' },
    ],
    costText: () => `按官方价：768P 每秒约 7.4${P()}、2K 每秒约 11.8${P()}；提交前会先报价`,
    cost: (o) => Math.ceil(((o.resolution === '2K' ? 800 : 500) * o.duration * 1000) / 68000),
    prepare(o) {
      if (!o.ratio) o.ratio = o.first ? 'adaptive' : '16:9';
    },
    validate(o) {
      if (o.last && !o.first) return '--last 尾帧必须同时给 --first 首帧';
      const refs = (o.image || []).length + (o['ref-video'] || []).length + (o['ref-audio'] || []).length;
      if (o.first && refs) return '首尾帧和参考素材不能混用';
      if (o.first && o.ratio !== 'adaptive') return '首尾帧模式必须 --ratio adaptive';
      if (!o.first && !refs && o.ratio === 'adaptive') return '文生视频请指定固定比例';
      return '';
    },
    async run({ prompt, o, token, log }) {
      const media = [];
      if (o.first) media.push({ role: 'first_frame', url: await ensureUrl(o.first, token) });
      if (o.last) media.push({ role: 'last_frame', url: await ensureUrl(o.last, token) });
      for (const u of await ensureUrls(o.image, token)) media.push({ role: 'reference_image', url: u });
      for (const u of await ensureUrls(o['ref-video'], token)) media.push({ role: 'reference_video', url: u });
      for (const u of await ensureUrls(o['ref-audio'], token)) media.push({ role: 'reference_audio', url: u });
      const body = {
        prompt, resolution: o.resolution, duration: o.duration, ratio: o.ratio, aigc_watermark: !!o.watermark, media,
      };
      const quote = (await requestJson(artApi('minimax-h3/quote'), { data: body, token, timeout: 120_000 })).data;
      log(`  报价：${quote.points} ${P()}（最多预扣 ${quote.max_points}）`);
      const res = await requestJson(artApi('minimax-h3/tasks'), {
        data: { ...body, request_id: newRequestId(), quote_token: quote.quote_token }, token, timeout: 120_000,
      });
      const task = res.data;
      log(`  已提交：任务 ${task.id}`);
      rememberTask({ model: 'minimax-h3', id: task.id });
      if (o.wait === false) return { cost: task.reserved_points, pending: { model: 'minimax-h3', id: task.id, status: task.status } };
      const done = await pollTask(`minimax-h3/tasks/${task.id}`, { token, log, timeoutSec: 2400, interval: 15 });
      return { cost: done.points, results: [{ kind: 'video', url: fullUrl(done.video_url), id: done.id }] };
    },
    async resume({ id: taskId, token, log, wait }) {
      if (!wait) return { task: (await requestJson(artApi(`minimax-h3/tasks/${taskId}`), { token })).data };
      const done = await pollTask(`minimax-h3/tasks/${taskId}`, { token, log, timeoutSec: 2400, interval: 15 });
      return { cost: done.points, results: [{ kind: 'video', url: fullUrl(done.video_url), id: done.id }] };
    },
  },
  {
    id: 'suno',
    type: 'music',
    sites: BOTH,
    name: 'Suno 音乐',
    summary: 'AI 写歌：一句描述生成带人声的完整歌曲（含作词），或用自己的歌词 + 风格作曲；也能出纯音乐。每次出 2 首',
    details: [
      '描述模式：只写提示词（例如「一首关于夏天海边的轻快中文流行歌」），自动作词作曲',
      '歌词模式：--lyrics 传歌词文本或歌词文件路径（可用 [Verse] [Chorus] 标段），--style 写风格（例如 "mandopop, female vocal, piano"），--title 歌名',
      '--instrumental 纯音乐（无人声），用提示词或 --style 描述曲风',
      '一般 1～3 分钟出歌，下载为 mp3，同时给出封面图',
    ],
    options: [
      { key: 'lyrics', type: 'text', desc: '歌词文本，或歌词文件路径' },
      { key: 'style', type: 'text', desc: '音乐风格 / 标签（英文效果更好）' },
      { key: 'title', type: 'text', desc: '歌名' },
      { key: 'instrumental', type: 'bool', default: false, desc: '纯音乐' },
    ],
    promptOptional: true,
    costText: () => `每次 40${P()}（一次出 2 首）`,
    cost: () => 40,
    validate(o, prompt) {
      if (!prompt && !o.lyrics && !(o.instrumental && o.style)) return '写一句描述（提示词），或者用 --lyrics 给歌词';
      if (o.lyrics && !o.style && !o.instrumental) return '歌词模式要同时给 --style 音乐风格';
      return '';
    },
    async run({ prompt, o, token, log }) {
      let lyrics = o.lyrics || '';
      if (lyrics && fs.existsSync(lyrics) && fs.statSync(lyrics).isFile()) lyrics = fs.readFileSync(lyrics, 'utf8');
      let body;
      if (o.instrumental) {
        body = site() === 'aihuihua'
          ? { generateType: 'type_manual', isPureMusic: true, musicStyle: o.style || prompt, musicTitle: o.title || '' }
          : { generateType: 'type_desc', isPureMusic: true, prompt: [prompt, o.style].filter(Boolean).join(', ') };
      } else if (lyrics) {
        body = { generateType: 'type_manual', lyric: lyrics, musicStyle: o.style, musicTitle: o.title || '' };
      } else {
        body = { generateType: 'type_desc', prompt, isPureMusic: false };
        if (o.title) body.musicTitle = o.title;
      }
      let lastStatus = '';
      const events = await requestStream(artApi('suno-music-generate'), {
        data: body,
        token,
        onEvent: (e) => {
          if (e.status && e.status !== lastStatus) {
            lastStatus = e.status;
            log(`  … ${e.status}`);
          }
        },
      });
      const final = [...events].reverse().find((e) => e.state === 'complete' || (e.code !== undefined && e.code !== 0));
      if (!final) throw new ApiError('音乐服务没有返回结果，稍后用 history 看看');
      if (final.code !== undefined && final.code !== 0) throw new ApiError(final.message || '音乐生成失败', { code: final.code });
      const songs = final.audioResult || [];
      const results = [];
      songs.forEach((s) => {
        results.push({ kind: 'audio', url: s.audioUrl, title: s.title, duration: s.duration, tags: s.tags });
        if (s.imgLargeUrl || s.imgUrl) results.push({ kind: 'image', url: s.imgLargeUrl || s.imgUrl, title: `${s.title || ''} 封面` });
      });
      return { cost: final.cost, results, lyrics: songs.map((s) => ({ title: s.title, lyrics: s.prompt })) };
    },
  },
  {
    id: 'tts',
    type: 'speech',
    sites: BOTH,
    name: '文字转语音（豆包语音合成 2.0）',
    summary: '把文字念成 mp3：400 多种音色（中文男女声、旁白、角色、有声书、客服，以及英日韩西法等外语），可调语速、用一句话指定语气',
    details: [
      '--prompt 就是要念的文字（也可以传 .txt 文件路径），一次最多 5000 字，长文会自动分段合成后拼成一个 mp3',
      `先用 voices 命令挑音色（可按 --lang --gender --scene --q 筛选，每个音色都附试听链接，试听不扣${P()}），再用 --voice <音色ID>`,
      '不传 --voice 默认用「擎苍」（沉稳男声，适合旁白、诗词朗诵）',
      '--speed 0.5～2 倍速；--instruction 一句话语气，例如「用开心活泼的语气」「用沉稳庄重的语气朗读」',
    ],
    options: [
      { key: 'voice', type: 'text', desc: '音色 ID（voices 命令查）' },
      { key: 'speed', type: 'text', default: '1', desc: '语速倍数 0.5～2' },
      { key: 'instruction', type: 'text', desc: '语气指令（可选）' },
    ],
    costText: () => `按字数计费，最少 1 ${P()}`,
    cost: (o, prompt = '') => ttsPoints(prompt),
    validate(o, prompt) {
      const n = Number(o.speed);
      if (!Number.isFinite(n) || n < 0.5 || n > 2) return '--speed 要在 0.5～2 之间';
      if ([...prompt].length > TTS_MAX_CHARS) return `一次最多 ${TTS_MAX_CHARS} 字，请拆开多次合成`;
      return '';
    },
    async run({ prompt, o, token }) {
      const res = await requestJson(api('text-speech'), {
        data: { input: prompt, voice: o.voice || undefined, speed: Number(o.speed), instruction: o.instruction || '' },
        token,
        timeout: 10 * 60_000,
      });
      return { cost: res.cost, results: [{ kind: 'audio', url: res.data, ext: 'mp3', id: res.id }] };
    },
  },
];

// ─── MJ ────────────────────────────────────────────────────────

/** MJ 出图结束后再查一次，拿转存到 OSS 的图（上游临时地址国内常打不开）和按钮 */
async function mjResult(final, token) {
  const imgId = final.id;
  let detail = null;
  for (let i = 0; i < 4 && imgId; i += 1) {
    await sleep(1500);
    try {
      detail = (await requestJson(artApi('get-my-img-detail-by-img-id'), { data: { imgId }, token })).data;
      if (detail?.img_url) break;
    } catch {
      /* 记录还没写完，再等等 */
    }
  }
  const buttons = (final.buttons || detail?.buttons || []).map((b) => b.customId).filter(Boolean);
  const cache = readState('mj-buttons.json') || {};
  cache[imgId] = { buttons, at: Date.now() };
  for (const k of Object.keys(cache)) if (Date.now() - cache[k].at > 3 * 3600_000) delete cache[k];
  writeState('mj-buttons.json', cache);
  const url = detail?.img_url ? fullUrl(detail.img_url, 'mj') : final.uri;
  const actions = MJ_ACTIONS.filter(([, prefix]) => buttons.some((b) => b.startsWith(prefix))).map(([alias]) => alias);
  return { cost: final.cost, results: [img(url, { id: imgId, paintingType: 'mj' })], mj: { imgId, actions } };
}

export async function mjAction({ imgId, action, token, log }) {
  const hit = MJ_ACTIONS.find(([alias, prefix, , label]) => [alias.toLowerCase(), prefix.toLowerCase(), label].includes(String(action).toLowerCase()));
  if (!hit) throw new ApiError(`不认识的操作「${action}」，可用：${MJ_ACTIONS.map((a) => a[0]).join(' ')}`, { code: 'USAGE' });
  let buttons = readState('mj-buttons.json')?.[imgId]?.buttons || [];
  if (!buttons.length) {
    const detail = (await requestJson(artApi('get-my-img-detail-by-img-id'), { data: { imgId }, token })).data;
    buttons = (detail?.buttons || []).map((b) => b.customId);
  }
  const buttonId = buttons.find((b) => b.startsWith(hit[1]));
  if (!buttonId) throw new ApiError(`这张图没有「${hit[0]}」操作（四宫格才能 U/V，放大后的单图才能 zoom / pan）`, { code: 'USAGE' });
  log(`  ${hit[3]}，消耗 ${hit[2]} ${P()}`);
  const final = await runStream('do-button-click', { buttonId, imgId }, { token, log });
  return mjResult(final, token);
}

export const MJ_ACTION_LIST = MJ_ACTIONS;

// ─── 对外 ──────────────────────────────────────────────────────

function rememberTask(task) {
  const list = readState('tasks.json') || [];
  list.unshift({ ...task, at: Date.now() });
  writeState('tasks.json', list.slice(0, 50));
}

export function modelsForSite(siteId = SITE.id) {
  const list = MODELS.filter((m) => m.sites.includes(siteId));
  if (!SITE.localH3) return list;
  // 专属版：其他照旧走网站，视频只留本地 H3
  return [...list.filter((m) => m.type !== 'video'), LOCAL_H3_MODEL];
}

export function findModel(id) {
  const key = String(id || '').toLowerCase();
  const alias = {
    'gpt-image-2.5': 'gpt-image-2.5-flare', flare: 'gpt-image-2.5-flare', sunburst: 'gpt-image-2.5-sunburst',
    'nano-banana': 'nano-banana-pro', nanobanana: 'nano-banana-pro', mj: 'midjourney',
    'gpt-4o': 'gpt-4o-image', seedream: 'seedream-5', jimeng: 'seedream-5', seedance: 'seedance-2.0-fast', h3: 'minimax-h3', hailuo: 'minimax-h3',
    music: 'suno', matting: 'remove-bg', speech: 'tts', voice: 'tts', doubao: 'tts',
  }[key] || key;
  return modelsForSite().find((m) => m.id === alias) || null;
}

export { SEEDANCE, seedancePoints, STATUS_TEXT };
