#!/usr/bin/env node
// 获取视频脚本审核结果（仅 status=completed 时可用）
//
// 用法:
//   node scripts/video_audit_result.mjs '{"task_id":"550e8400-e29b-41d4-a716-446655440000"}'
//
// 参数:
//   task_id — 必填，任务 ID（UUID，从 submit 返回）
//
// 返回:
//   task_id         — 任务 ID
//   audit_result    — 完整审核结果 JSON，包含:
//     storyboard           — 分镜拆解
//     viral_factors        — 爆款因子分析
//     content_audit        — 内容审核
//     benchmark_comparison — Benchmark 对标
//     suggestions          — 优化建议
//     scores               — 各维度评分
//     confidence           — 置信度
//     diagnosis_level      — 诊断等级
//     creator_metadata     — 达人元数据
//     video_metrics        — 视频表现数据
//   html_report_url — HTML 报告公开 URL（https://oss.creativault.tech/...），生成失败时为 null
//
// 错误码:
//   40001 — 任务不存在
//   40002 — 任务未完成（需等待 status=completed）
//   40003 — 审核结果不存在

import { callAPI, parseArgs, validateRequired } from './_api_client.mjs';

const params = parseArgs();
validateRequired(params, ['task_id']);

const result = await callAPI('/openapi/v1/video-script-audit/tasks/result', {
  task_id: params.task_id,
});

console.log(JSON.stringify(result, null, 2));
