/**
 * outreach_todo.mjs — 待办跟进列表
 *
 * 用法: node scripts/outreach_todo.mjs '{"overdue_hours":24}'
 *
 * 参数:
 *   overdue_hours    — 超时阈值（小时），默认 24
 *   include_unread   — 是否包含未读，默认 true
 *   include_overdue  — 是否包含超时未回复，默认 true
 */

import { callAPI, parseArgs } from './_api_client.mjs';

const params = parseArgs();
const result = await callAPI('/openapi/v1/outreach/todo', params, null, { skipUserIdentity: false });
console.log(JSON.stringify(result, null, 2));
