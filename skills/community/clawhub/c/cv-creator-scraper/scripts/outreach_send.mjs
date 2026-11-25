/**
 * outreach_send.mjs — 发送建联邮件（单笔/批量统一）
 *
 * 单笔: node scripts/outreach_send.mjs '{"to":"creator@x.com","uid":"7123456789","platform":"tiktok","subject":"Hi","body_html":"<p>...</p>"}'
 * 批量: node scripts/outreach_send.mjs '{"recipients":[{"email":"a@x.com","uid":"123","nickname":"A","platform":"tiktok"}],"subject":"Hi","body_html":"<p>...</p>"}'
 *
 * 参数:
 *   to (string)          — 达人邮箱（单笔，与 recipients 互斥）
 *   uid (string)         — 达人平台 UID（单笔必传，来自搜索结果的 uid 字段，OpenAPI 自动反查完整数据）
 *   nickname (string)    — 达人昵称（可选）
 *   platform (string)    — 达人平台（推荐传入：tiktok/youtube/instagram）
 *   recipients (array)   — 收件人列表（批量，与 to 互斥，每项需含 email + uid + platform）
 *   subject              — 邮件主题
 *   body_html            — HTML 正文
 *   body_text            — 纯文本正文
 *   channel              — 渠道: saas(默认，平台代发) / gmail / outlook。脚本内部 saas→ses 映射
 *   template_id          — 模板ID
 *   send_mode            — immediate(默认) / smart
 *   force_new            — 强制新建会话（默认 false）
 *   attachment_ids       — 附件ID列表
 */

import {
  attachOutreachWorkspaceUrl,
  callAPI,
  parseArgs,
} from './_api_client.mjs';

const params = parseArgs();

if (!params.to && !params.recipients) {
  console.error(JSON.stringify({ error: '"to" or "recipients" is required' }));
  process.exit(1);
}

// channel 参数映射：对外统一用 saas（平台代发），后端只认 ses。
// 用户传 saas 或不传 → 映射为 ses；传 ses/gmail/outlook 保持原样。
const CHANNEL_MAP = { saas: 'ses' };
if (params.channel && CHANNEL_MAP[params.channel]) {
  params.channel = CHANNEL_MAP[params.channel];
} else if (!params.channel) {
  params.channel = 'ses';
}

const result = await callAPI('/openapi/v1/outreach/send', params, null, { skipUserIdentity: false });
await attachOutreachWorkspaceUrl(result, {
  task_id: result?.data?.task_id,
  email: params.to,
});
console.log(JSON.stringify(result, null, 2));
