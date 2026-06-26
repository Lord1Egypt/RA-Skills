#!/usr/bin/env node
// 轮询采集任务状态，每 60 秒查询一次，直到任务完成/失败/超时
//
// 用法:
//   node poll_task_status.mjs '{"task_id":"task_20260315_abc123"}'
//   node poll_task_status.mjs '{"task_id":"task_xxx","interval":30,"max_attempts":60}'
//
// 参数:
//   task_id       — 必填，任务 ID
//   interval      — 可选，轮询间隔秒数，默认 60
//   max_attempts  — 可选，最大轮询次数，默认 45（即默认最多等 45 分钟）

import { callAPI, parseArgs, validateRequired } from './_api_client.mjs';

const params = parseArgs();
validateRequired(params, ['task_id']);

const taskId = params.task_id;
const interval = params.interval || 60;
const maxAttempts = params.max_attempts || 45;

const TERMINAL_STATES = ['completed', 'failed', 'timeout'];

function sleep(seconds) {
  return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}

console.error(`[轮询] 开始监控任务 ${taskId}，间隔 ${interval}s，最多 ${maxAttempts} 次`);

for (let attempt = 1; attempt <= maxAttempts; attempt++) {
  const result = await callAPI('/openapi/v1/collection/tasks/status', {
    task_id: taskId,
  });

  const { status, progress, total, completed, failed } = result.data;

  console.error(`[轮询 ${attempt}/${maxAttempts}] 状态: ${status} | 进度: ${progress}% | 完成: ${completed}/${total} | 失败: ${failed}`);

  if (TERMINAL_STATES.includes(status)) {
    // 任务结束，输出最终结果到 stdout
    console.log(JSON.stringify(result, null, 2));
    process.exit(status === 'completed' ? 0 : 1);
  }

  if (attempt < maxAttempts) {
    await sleep(interval);
  }
}

// 超过最大轮询次数
console.error(`[轮询] 已达最大轮询次数 ${maxAttempts}，任务仍在处理中`);
console.log(JSON.stringify({
  success: false,
  error: { message: `轮询超时：已等待 ${maxAttempts * interval} 秒，任务仍未完成` },
  data: { task_id: taskId },
}));
process.exit(1);
