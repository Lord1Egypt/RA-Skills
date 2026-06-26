#!/usr/bin/env node

const text = `
Douyin Creator Ops Skill - quick usage

1. New agent preflight
   node scripts/bootstrap-openclaw.js --apply
   node scripts/preflight.js --online
   node scripts/agent-ready.js
   node scripts/openclaw-douyin-health.js --fix --restart-gateway

2. Feishu/OpenClaw single-entry loop
   In Feishu mode, agents should pass every Douyin user message to:
   douyin__douyin_feishu_route_text({ text: raw_user_message })

   This single entry owns:
   - 自动发布
   - 获取数据生成分析
   - 自动回复评论
   - 自动回复私信

3. Standalone Feishu watcher, only when OpenClaw gateway is not handling Feishu
   node scripts/feishu-reply-watcher.js poll --init
   node scripts/feishu-reply-watcher.js watch --since-seconds 1800 --interval-ms 1000 --page-size 50 --max-pages 10

4. Feishu user triggers
   发布抖音
   发送二维码
   已登录
   6位短信验证码
   发布视频
   更新数据 / 数据更新 / 更新数据 30天 / 数据报告 / 数据分析 / 查看数据
   自动回复 / 自动回复评论 / 自动回复私信
   定时任务 / 修改定时任务 自动回复 30分钟 / 修改定时任务 自动化营销 07:30

5. Fieldized passive publish input
   tags:#宠物险#保险
   "封面图片": "https://...png"
   标题："养宠不焦虑的秘诀？"
   "视频地址": "https://...mp4"

6. Local publish task
   node scripts/prepare-upstream-publish-task.js --input upstream.json --output publish-task.json
   node scripts/publish-task.js --task publish-task.json --execute
   OpenClaw/other agents: use douyin__douyin_publish_from_upstream_text, then poll douyin__douyin_publish_job_status

7. Data sync and report
   node scripts/sync-douyin-data-to-feishu-bitable.js --days 90 --notify
   node scripts/douyin-data-report-from-bitable.js --days 90 --notify

8. Comments and DMs
   node scripts/douyin-comment-reply.js list --unreplied --author-reply-check --pages 8
   node scripts/douyin-comment-reply.js reply --text "..." --index 0 --unreplied --author-reply-check --execute
   node scripts/douyin-dm-reply.js list
   node scripts/douyin-dm-reply.js reply --text "..." --execute

9. Auto reply by content
   node scripts/douyin-auto-reply.js both --limit 50 --max-scan 200
   node scripts/douyin-auto-reply.js both --limit 50 --max-scan 200 --execute
   飞书触发：自动回复 / 自动回复评论 / 自动回复私信

10. Scheduled tasks
   node scripts/douyin-schedule-manager.js install-default
   node scripts/douyin-schedule-manager.js status
   飞书触发：定时任务 / 修改定时任务 自动回复 30分钟 / 修改定时任务 自动化营销 07:30

Read SKILL.md for stability rules, login guardrails, and failure handling.
`.trim();

console.log(text);
