#!/usr/bin/env node
/**
 * feishu-cli-setup — verify.js
 * PROMPT GENERATOR ONLY — no outbound network requests.
 * Outputs an agent prompt to verify lark-cli setup is complete and summarize
 * which of the 20 Agent Skills are now usable.
 *
 * Usage:
 *   node scripts/verify.js
 *   node scripts/verify.js --lang en
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';

if (lang === 'en') {
  console.log(`=== Feishu CLI Setup — Step 4: Verify & Summary ===

Verify the complete lark-cli installation and summarize what the user can now do.
Run all checks and present results in a user-friendly summary.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERIFICATION CHECKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHECK 1 — CLI version
  lark-cli --version
  → Expected: v1.0.4 (or higher)
  → ✓ if version string printed  ✗ if command not found

CHECK 2 — Authentication status
  lark-cli auth status
  → Expected: shows user name/email and list of granted scopes
  → ✓ if authenticated  ✗ if "not logged in"

CHECK 3 — List all authenticated identities
  lark-cli auth list
  → Shows all users/bots available (user identity and/or bot identity)

CHECK 4 — Quick smoke test (calendar agenda)
  lark-cli calendar +agenda --dry-run 2>/dev/null || lark-cli auth check calendar:calendar:readonly
  → If dry-run succeeds or auth check exits 0: calendar scope is active
  → This confirms the CLI can actually reach the Feishu API

CHECK 5 — Available Agent Skills
  npx skills list 2>/dev/null | grep lark || echo "skills not listed"
  → Count how many lark-* skills appear

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRESENT THE SUMMARY TO THE USER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After running the checks, present this friendly summary to the user:

---
✅ lark-cli is set up and ready!

📋 Status:
  • Version: <version>
  • Logged in as: <name / email>
  • Scopes granted: <N> (covers <domains list>)

🤖 20 Agent Skills now available:

  Core:
  • lark-shared      — auth, config, identity switching (always active)

  Communication:
  • lark-im          — send/reply messages, manage group chats
  • lark-mail        — browse, search, send/reply emails

  Productivity:
  • lark-calendar    — view agenda, create events, check availability
  • lark-task        — create tasks, subtasks, set reminders
  • lark-doc         — create, read, update documents (Markdown)
  • lark-drive       — upload/download files, manage permissions
  • lark-sheets      — read/write/search spreadsheets
  • lark-base        — tables, records, views, dashboards
  • lark-wiki        — knowledge spaces and nodes

  People:
  • lark-contact     — search users by name/email/phone

  Meetings:
  • lark-vc          — meeting records and minutes
  • lark-minutes     — meeting AI summaries, todos, transcripts

  Advanced:
  • lark-event       — real-time WebSocket event subscriptions
  • lark-whiteboard  — whiteboard/chart rendering
  • lark-openapi-explorer — browse 2500+ Lark APIs
  • lark-skill-maker — create custom skills

  Workflows:
  • lark-workflow-meeting-summary  — structured meeting reports
  • lark-workflow-standup-report   — standup summaries

  Approval:
  • lark-approval    — query, approve/reject tasks and instances

💡 Try these first commands:
  lark-cli calendar +agenda               # today's calendar
  lark-cli im +messages-send --chat-id oc_xxx --text "Hello" --dry-run
  lark-cli task +list                     # your tasks

🔐 Security reminder:
  • Use --dry-run before commands that modify data
  • Only add the Feishu bot to private chats, not public groups
  • Run lark-cli auth scopes to review granted permissions

Run: node scripts/learn.js for a hands-on first-steps guide.
---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESULT REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Report:
  CLI installed:      ✓ <version> | ✗
  Authenticated:      ✓ <user> | ✗
  Smoke test:         ✓ | ✗
  Skills available:   <N>/20
  Overall:            FULLY_READY | PARTIAL | FAILED

If FAILED: identify which check failed and direct user back to the appropriate step.
If FULLY_READY: suggest running node scripts/learn.js for first commands.
`);
} else {
  console.log(`=== 飞书 CLI 安装向导 — 第 4 步：验证与总结 ===

验证 lark-cli 安装是否完整，并向用户总结现在可以做什么。
运行所有检查，以友好方式呈现结果。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
验证检查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

检查 1 — CLI 版本
  lark-cli --version
  → 预期：v1.0.4（或更高）
  → ✓ 打印版本号  ✗ 命令未找到

检查 2 — 认证状态
  lark-cli auth status
  → 预期：显示用户姓名/邮箱及已授权的 scope 列表
  → ✓ 已认证  ✗ "未登录"

检查 3 — 列出所有认证身份
  lark-cli auth list
  → 显示所有可用的用户/机器人身份

检查 4 — 快速冒烟测试（日历日程）
  lark-cli calendar +agenda --dry-run 2>/dev/null || lark-cli auth check calendar:calendar:readonly
  → 如 dry-run 成功或 auth check 退出码为 0：日历 scope 已激活
  → 确认 CLI 可以实际访问飞书 API

检查 5 — 可用 Agent Skills
  npx skills list 2>/dev/null | grep lark || echo "skills not listed"
  → 统计出现了多少个 lark-* 技能

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
向用户展示安装完成总结
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

完成检查后，向用户展示以下友好摘要：

---
✅ lark-cli 已准备就绪！

📋 状态：
  • 版本：<版本号>
  • 已登录为：<姓名 / 邮箱>
  • 已授权 scope：<N> 个（覆盖 <域列表>）

🤖 现已可用的 20 个 Agent Skills：

  核心：
  • lark-shared      — 认证、配置、身份切换（始终激活）

  沟通：
  • lark-im          — 发送/回复消息，管理群聊
  • lark-mail        — 浏览、搜索、发送/回复邮件

  效率：
  • lark-calendar    — 查看日程、创建活动、检查空闲时间
  • lark-task        — 创建任务、子任务、设置提醒
  • lark-doc         — 创建、阅读、更新文档（Markdown）
  • lark-drive       — 上传/下载文件、管理权限
  • lark-sheets      — 读写搜索电子表格
  • lark-base        — 多维表格、记录、视图、仪表盘
  • lark-wiki        — 知识空间和节点

  联系人：
  • lark-contact     — 按姓名/邮箱/手机搜索用户

  会议：
  • lark-vc          — 会议记录和纪要
  • lark-minutes     — 会议 AI 摘要、待办、逐字稿

  进阶：
  • lark-event       — 实时 WebSocket 事件订阅
  • lark-whiteboard  — 白板/图表渲染
  • lark-openapi-explorer — 浏览 2500+ 飞书 API
  • lark-skill-maker — 创建自定义 skill

  工作流：
  • lark-workflow-meeting-summary  — 结构化会议报告
  • lark-workflow-standup-report   — 每日站会摘要

  审批：
  • lark-approval    — 查询、审批/拒绝任务和审批实例

💡 推荐先试这几个命令：
  lark-cli calendar +agenda               # 今日日程
  lark-cli im +messages-send --chat-id oc_xxx --text "你好" --dry-run
  lark-cli task +list                     # 我的任务

🔐 安全提醒：
  • 对有副作用的命令先用 --dry-run 预览
  • 飞书机器人只加入私聊，不要加入公开群
  • 运行 lark-cli auth scopes 查看已授权权限

运行：node scripts/learn.js 查看上手第一步指南。
---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
结果报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

报告：
  CLI 已安装：    ✓ <版本> | ✗
  已认证：        ✓ <用户> | ✗
  冒烟测试：      ✓ | ✗
  Skills 可用：   <N>/20
  总体状态：      FULLY_READY | PARTIAL | FAILED

如果 FAILED：找出哪项检查失败，引导用户回到对应步骤。
如果 FULLY_READY：建议运行 node scripts/learn.js 开始使用。
`);
}
