/**
 * outreach_task.mjs — 查询发送任务（状态+结果统一）
 *
 * 查询: node scripts/outreach_task.mjs '{"task_id":"task_xxx"}'
 * 含结果: node scripts/outreach_task.mjs '{"task_id":"batch_xxx","include_result":true}'
 * 轮询: node scripts/outreach_task.mjs '{"task_id":"batch_xxx","poll":true}'
 *
 * 参数:
 *   task_id (必填)     — 任务ID
 *   include_result     — 完成后附带逐条结果（默认 false）
 *   result_filter      — 结果筛选: all / sent / failed
 *   poll               — 自动轮询直到终态（默认 false）
 *   poll_interval      — 轮询间隔秒数（默认 5）
 *   poll_max_attempts  — 最大轮询次数（默认 60）
 */

import { callAPI, parseArgs, validateRequired } from './_api_client.mjs';

const params = parseArgs();
validateRequired(params, ['task_id']);

const poll = params.poll || false;
const interval = params.poll_interval || 5;
const maxAttempts = params.poll_max_attempts || 60;
const terminalStatuses = ['completed', 'completed_with_errors', 'failed', 'timeout', 'quota_exceeded'];

// 构建请求体（去掉 poll 相关参数）
const requestBody = { task_id: params.task_id };
if (params.include_result) requestBody.include_result = true;
if (params.result_filter) requestBody.result_filter = params.result_filter;
if (params.result_page) requestBody.result_page = params.result_page;
if (params.result_size) requestBody.result_size = params.result_size;

if (!poll) {
  // 单次查询
  const result = await callAPI('/openapi/v1/outreach/task', requestBody, null, { skipUserIdentity: false });
  console.log(JSON.stringify(result, null, 2));
} else {
  // 轮询模式
  for (let i = 0; i < maxAttempts; i++) {
    const result = await callAPI('/openapi/v1/outreach/task', requestBody, null, { skipUserIdentity: false });
    const status = result?.data?.status;

    if (terminalStatuses.includes(status)) {
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    }

    const progress = result?.data?.progress;
    const progressStr = progress ? ` (sent:${progress.sent}/${progress.total})` : '';
    process.stderr.write(`[${i + 1}/${maxAttempts}] Status: ${status}${progressStr}, waiting ${interval}s...\n`);
    await new Promise(r => setTimeout(r, interval * 1000));
  }

  console.error(`Timeout: task ${params.task_id} did not complete after ${maxAttempts} attempts`);
  process.exit(1);
}
