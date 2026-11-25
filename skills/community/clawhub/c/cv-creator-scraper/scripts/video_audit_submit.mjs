#!/usr/bin/env node
// 提交视频脚本审核任务（异步），支持两条摄入链路
//
// 用法:
//   # 链路1: 社媒 URL（TikTok/Instagram Reels/YouTube Shorts，后端自动下载）
//   node scripts/video_audit_submit.mjs '{"video_url":"https://www.tiktok.com/@creator/video/123456"}'
//
//   # 链路2: 上传素材（先调 media_upload.mjs 拿 oss_url，再传 oss_url）
//   node scripts/video_audit_submit.mjs '{"oss_url":"https://oss.creativault.tech/media_ingestion/uploads/user@example.com/20260615_103000_a1b2c3d4.mp4","brief":"发布前自审"}'
//
//   # 完整参数示例
//   node scripts/video_audit_submit.mjs '{"video_url":"...","brief":"产品卖点...","audit_mode":"high","enable_benchmark":true}'
//
// 参数（字段名与后端 SubmitAuditTaskRequest 一致）:
//   video_url         — 链路1必填（与 oss_url 二选一），社媒视频 URL
//                       仅支持以下三种格式，提交前本地白名单校验，不合格直接拒绝且不扣积分：
//                         TikTok:          https://www.tiktok.com/@{username}/video/{数字ID}
//                         YouTube Shorts:  https://www.youtube.com/shorts/{id} 或 https://youtu.be/{id}
//                         Instagram Reels: https://www.instagram.com/reel/{shortcode}
//                       不支持 youtube.com/watch?v=（长视频页）、vt.tiktok.com 分享短链、抖音
//   oss_url           — 链路2必填（与 video_url 二选一），media_upload.mjs 返回的完整 oss_url
//                       必须是 *.creativault.tech 下的 HTTPS 完整 URL
//   brief             — 可选，客户 Brief（用于符合度审核）
//   campaign_id       — 可选，活动 ID
//   audit_mode        — 可选，审核模式: high(默认) / low
//   enable_benchmark  — 可选，与已有案例对标，默认 false
//
// 兼容的旧参数名（会自动映射，仅为兼容存量调用）:
//   url               → video_url
//   oss_url_override  → oss_url
//   uploaded_oss_key  → 不再接受。它是 OSS key 而非 URL，无法安全转换，见下方报错提示
//
// 链路差异:
//   链路1 (video_url): 支持反查达人数据（粉丝/历史均播/爆款分级）
//   链路2 (oss_url):   creator_metadata/video_metrics 返回 status=not_applicable
//                      （上传素材天然无社媒身份，非数据缺失）
//
// 返回:
//   task_id              — 任务唯一标识（UUID）
//   status               — "pending"
//   estimated_time_seconds — 预估耗时（约 240 秒）
//
// 积分消耗以服务端计费配置和响应为准。

import { callAPI, parseArgs } from './_api_client.mjs';

// 平台白名单：与后端 talent_video_download_client.py 的 PLATFORM_PATTERNS 逐条对齐。
// 后端 submit 也会拒绝（40004），本地拦截的价值是不消耗一次 API 请求配额，
// 并且能立刻给出正确格式提示，而不是让用户拿着一句「不支持」自己猜。
const PLATFORM_PATTERNS = {
  tiktok: /^https?:\/\/(www\.)?tiktok\.com\/@[\w.\-]+\/video\/\d+/i,
  youtube_shorts: /^https?:\/\/(www\.)?(youtube\.com\/shorts\/[\w\-]+|youtu\.be\/[\w\-]+)/i,
  instagram_reels: /^https?:\/\/(www\.)?instagram\.com\/(reels?|p)\/[\w\-]+/i,
};

const SUPPORTED_URL_FORMATS = [
  'TikTok:           https://www.tiktok.com/@{username}/video/{数字ID}',
  'YouTube Shorts:   https://www.youtube.com/shorts/{videoId} 或 https://youtu.be/{videoId}',
  'Instagram Reels:  https://www.instagram.com/reel/{shortcode}',
];

function detectPlatform(url) {
  const trimmed = String(url || '').trim();
  for (const [platform, pattern] of Object.entries(PLATFORM_PATTERNS)) {
    if (pattern.test(trimmed)) return platform;
  }
  return null;
}

/** 针对高频误传形态给定向提示，避免用户只看到「不支持」而不知道差在哪。 */
function explainUnsupportedUrl(url) {
  const value = String(url || '').trim();
  if (/^https?:\/\/(www\.)?youtube\.com\/watch/i.test(value)) {
    return '这是 YouTube 长视频页链接，仅支持 Shorts 短视频（youtube.com/shorts/... 或 youtu.be/...）';
  }
  if (/^https?:\/\/(vt|vm)\.tiktok\.com\//i.test(value)) {
    return 'TikTok 分享短链无法识别，请在浏览器打开后复制完整链接（形如 /@用户名/video/数字ID）';
  }
  if (/^https?:\/\/(www\.)?douyin\.com\//i.test(value)) {
    return '抖音不在支持范围内，仅支持 TikTok / YouTube Shorts / Instagram Reels';
  }
  return '不在支持的平台白名单内';
}

/** 与后端 media_ingestion/models.py 的 is_trusted_oss_url 对齐。 */
function isTrustedOssUrl(value) {
  try {
    const parsed = new URL(String(value || '').trim());
    const host = parsed.hostname.toLowerCase().replace(/\.$/, '');
    return parsed.protocol === 'https:'
      && Boolean(host)
      && (host === 'creativault.tech' || host.endsWith('.creativault.tech'))
      && parsed.pathname.replace(/^\/+|\/+$/g, '').length > 0;
  } catch {
    return false;
  }
}

/** 用户输入类错误必须双写 stdout + stderr：宿主按非 0 退出码丢输出时 stderr 也会被丢。 */
function failWithUserFacingError(output) {
  const payload = { success: false, failure_stage: 'local_validation', ...output };
  console.log(JSON.stringify(payload, null, 2));
  console.error(JSON.stringify(payload, null, 2));
  process.exit(1);
}

const params = parseArgs();

// 字段名以后端 SubmitAuditTaskRequest 为准（video_url / oss_url）。
// 旧名 url、oss_url_override 语义等价，做无损映射。
const videoUrl = String(params.video_url || params.url || '').trim();
const ossUrl = String(params.oss_url || params.oss_url_override || '').trim();

// uploaded_oss_key 是 OSS 对象 key，后端 submit 只接受完整 HTTPS URL。
// 这里不替调用方拼域名——那会把桶域名硬编码进 skill，域名一变就静默失效。
if (params.uploaded_oss_key && !ossUrl) {
  failWithUserFacingError({
    error: 'uploaded_oss_key 不再被接受：后端需要完整的 OSS URL，不是 OSS key',
    reason: 'media_upload.mjs 的响应里同时返回 oss_key 和 oss_url，请改传 oss_url',
    received: params.uploaded_oss_key,
    expected_example: 'https://oss.creativault.tech/media_ingestion/uploads/user@example.com/20260615_103000_a1b2c3d4.mp4',
    action_required: '改用 media_upload 返回的 oss_url 重新提交',
  });
}

const hasVideoUrl = Boolean(videoUrl);
const hasOssUrl = Boolean(ossUrl);

// 链路二选一：后端 model_validator 要求恰好一个，都空或都传都会被拒。
if (!hasVideoUrl && !hasOssUrl) {
  failWithUserFacingError({
    error: '链路必填参数缺失：video_url / oss_url 必须二选一',
    reason: '链路1 传 video_url（社媒 URL），链路2 传 oss_url（先调 media_upload.mjs 拿到）',
    examples: {
      链路1: '{"video_url":"https://www.tiktok.com/@creator/video/123"}',
      链路2: '{"oss_url":"https://oss.creativault.tech/media_ingestion/uploads/.../xxx.mp4"}',
    },
    action_required: '向用户索取视频链接，或先上传素材拿到 oss_url',
  });
}

if (hasVideoUrl && hasOssUrl) {
  failWithUserFacingError({
    error: 'video_url 和 oss_url 不能同时传',
    reason: '两条链路只能选其一：链路1 用 video_url，链路2 用 oss_url',
    action_required: '去掉其中一个参数后重新提交',
  });
}

// 链路1: 基础 URL 形态校验
if (hasVideoUrl && !/^https?:\/\/.+/i.test(videoUrl)) {
  failWithUserFacingError({
    error: `video_url 必须是合法的 HTTP/HTTPS URL: ${videoUrl}`,
    reason: '不是一个可识别的 URL',
    supported_formats: SUPPORTED_URL_FORMATS,
    action_required: '向用户索取符合格式的视频链接',
  });
}

// 链路1: 平台白名单校验
if (hasVideoUrl && !detectPlatform(videoUrl)) {
  failWithUserFacingError({
    error: `不支持的视频 URL（仅支持 TikTok / YouTube Shorts / Instagram Reels）: ${videoUrl}`,
    reason: explainUnsupportedUrl(videoUrl),
    supported_formats: SUPPORTED_URL_FORMATS,
    action_required: '必须把 error 与 reason 原文告知用户并索取符合格式的链接，不要重复提交',
  });
}

// 链路2: OSS URL 可信域名校验（对齐后端 is_trusted_oss_url，避免白跑一次请求）
if (hasOssUrl && !isTrustedOssUrl(ossUrl)) {
  failWithUserFacingError({
    error: `oss_url 必须是 *.creativault.tech 下的 HTTPS 完整 URL: ${ossUrl}`,
    reason: '后端只接受 CreatiVault 自有域名下的媒体地址，外链和 HTTP 一律拒绝',
    expected_example: 'https://oss.creativault.tech/media_ingestion/uploads/user@example.com/20260615_103000_a1b2c3d4.mp4',
    action_required: '使用 media_upload.mjs 返回的 oss_url 原值，不要手工改写',
  });
}

// 校验 audit_mode（后端只支持 high / low，不再支持 medium）
if (params.audit_mode && !['high', 'low'].includes(params.audit_mode)) {
  console.error(JSON.stringify({
    error: 'audit_mode must be one of: high / low',
    received: params.audit_mode,
  }));
  process.exit(1);
}

const body = {
  ...(hasVideoUrl && { video_url: videoUrl }),
  ...(hasOssUrl && { oss_url: ossUrl }),
  ...(params.brief && { brief: params.brief }),
  ...(params.user_id && { user_id: params.user_id }),
  ...(params.campaign_id && { campaign_id: params.campaign_id }),
  ...(params.audit_mode && { audit_mode: params.audit_mode }),
  ...(params.is_benchmark !== undefined && { is_benchmark: Boolean(params.is_benchmark) }),
  ...(params.enable_benchmark !== undefined && { enable_benchmark: Boolean(params.enable_benchmark) }),
};

const result = await callAPI('/openapi/v1/video-script-audit/tasks/submit', body);
console.log(JSON.stringify(result, null, 2));
