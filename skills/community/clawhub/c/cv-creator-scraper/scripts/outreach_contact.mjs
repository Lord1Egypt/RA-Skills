/**
 * outreach_contact.mjs — 查询达人建联信息（状态+历史+AI总结）
 *
 * 用法: node scripts/outreach_contact.mjs '{"email":"creator@x.com"}'
 *
 * 参数:
 *   email (必填)       — 达人邮箱
 *   include_history    — 是否包含沟通历史（默认 true）
 *   include_summary    — 是否包含 AI 总结（默认 true）
 */

import { callAPI, parseArgs, validateRequired } from './_api_client.mjs';

const params = parseArgs();
validateRequired(params, ['email']);

const result = await callAPI('/openapi/v1/outreach/contact', params, null, { skipUserIdentity: false });
console.log(JSON.stringify(result, null, 2));
