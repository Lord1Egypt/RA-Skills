#!/usr/bin/env node
// 查询视频脚本审核任务状态（单次查询，不轮询）
//
// 用法:
//   node scripts/video_audit_status.mjs '{"task_id":"550e8400-e29b-41d4-a716-446655440000"}'
//
// 参数:
//   task_id — 必填，任务 ID（UUID，从 submit 返回）
//
// 返回:
//   task_id       — 任务 ID
//   status        — pending / processing / completed / failed
//   progress      — 进度百分比（0/50/100）
//   created_at    — 创建时间
//   completed_at  — 完成时间（未完成为 null）
//   error_message — 错误信息（失败时）

import { callAPI, parseArgs, validateRequired } from './_api_client.mjs';

const params = parseArgs();
validateRequired(params, ['task_id']);

const result = await callAPI('/openapi/v1/video-script-audit/tasks/status', {
  task_id: params.task_id,
});

console.log(JSON.stringify(result, null, 2));
