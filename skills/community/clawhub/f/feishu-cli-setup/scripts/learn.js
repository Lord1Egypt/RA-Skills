#!/usr/bin/env node
/**
 * feishu-cli-setup — learn.js
 * PROMPT GENERATOR ONLY — no outbound network requests.
 * Outputs an agent prompt with a hands-on first-steps guide for lark-cli.
 * Teaches users the three-layer command system through real examples.
 *
 * Usage:
 *   node scripts/learn.js
 *   node scripts/learn.js --lang en
 *   node scripts/learn.js --domain calendar   # focus on one domain
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';
const domainIdx = args.indexOf('--domain');
const domain = domainIdx !== -1 ? args[domainIdx + 1] : null;

if (lang === 'en') {
  console.log(`=== Feishu CLI Setup — First Steps Guide ===

Guide the user through their first lark-cli commands.
Use --dry-run for write operations so the user can preview safely.
Explain each command before running it.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UNDERSTANDING THE THREE-LAYER SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

lark-cli has three ways to run commands:

  Layer 1 — Shortcuts (+prefix): easiest, AI-friendly, smart defaults
    lark-cli calendar +agenda

  Layer 2 — API Commands (auto-generated): precise, maps to platform API
    lark-cli calendar calendars list

  Layer 3 — Raw API (full coverage): any of 2500+ Lark APIs
    lark-cli api GET /open-apis/calendar/v4/calendars

Start with Layer 1 (shortcuts). Move to Layer 2/3 for advanced needs.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${domain ? `DOMAIN FOCUS: ${domain.toUpperCase()}` : 'HANDS-ON TOUR — 5 DOMAINS'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${!domain || domain === 'calendar' ? `
📅 CALENDAR — Check your schedule
  # Today's agenda (most useful first command)
  lark-cli calendar +agenda

  # This week's schedule
  lark-cli calendar +agenda --days 7

  # Create an event (preview first)
  lark-cli calendar +create --title "Team Sync" --start "2026-04-06T10:00" --end "2026-04-06T11:00" --dry-run
` : ''}${!domain || domain === 'im' ? `
💬 MESSAGING — Send and read messages
  # Send a message (replace oc_xxx with a real chat ID, --dry-run for preview)
  lark-cli im +messages-send --chat-id oc_xxx --text "Hello from lark-cli!" --dry-run

  # View recent messages in a chat
  lark-cli im +messages-list --chat-id oc_xxx

  # Search messages
  lark-cli im +messages-search --query "meeting notes"

  # Get chat ID: find a chat by name
  lark-cli im +chats-list | grep "your-chat-name"
` : ''}${!domain || domain === 'docs' ? `
📄 DOCUMENTS — Create and read docs
  # Create a document (--dry-run to preview)
  lark-cli docs +create --title "My First Doc" --markdown "# Hello\\n\\nContent here." --dry-run

  # Search for documents
  lark-cli docs +search --query "weekly report"

  # Read a document (replace doc_xxx with real ID)
  lark-cli docs +read --document-id doc_xxx
` : ''}${!domain || domain === 'task' ? `
✅ TASKS — Manage your todos
  # List your tasks
  lark-cli task +list

  # Create a task (--dry-run first)
  lark-cli task +create --title "Review PR" --due "2026-04-07" --dry-run

  # Complete a task
  lark-cli task +complete --task-id <task-id> --dry-run
` : ''}${!domain || domain === 'contact' ? `
👤 CONTACTS — Find people
  # Search by name
  lark-cli contact +search --name "Alice"

  # Search by email
  lark-cli contact +search --email "alice@example.com"

  # Get your own user ID
  lark-cli contact +me
` : ''}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USEFUL FLAGS TO KNOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  --dry-run          Preview the request without executing it (always safe)
  --format table     Human-readable table output
  --format json      Full JSON response (for agents/scripting)
  --format csv       CSV output (for spreadsheets)
  --page-all         Auto-paginate through all results
  --as user          Act as your user identity (default)
  --as bot           Act as the bot identity

SCHEMA INSPECTION (when you don't know the params):
  lark-cli schema                          # list all services
  lark-cli schema calendar.events.create  # see params for this endpoint
  lark-cli schema im.messages.delete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENT GUIDANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ask the user what they'd like to do. Suggested prompts to offer:
  • "Show me today's calendar agenda"
  • "Send a test message to a chat"
  • "Create a task for me"
  • "Search my documents for ..."
  • "Find a contact by name"

For any domain the user wants, use lark-cli <service> --help to discover commands.
`);
} else {
  console.log(`=== 飞书 CLI 安装向导 — 上手第一步指南 ===

引导用户运行他们的第一批 lark-cli 命令。
对写入操作使用 --dry-run，让用户安全预览效果。
运行每条命令之前先向用户解释它的作用。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
了解三层命令体系
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

lark-cli 有三种使用方式：

  第一层 — 快捷命令（+ 前缀）：最简单，AI 友好，智能默认值
    lark-cli calendar +agenda

  第二层 — API 命令（自动生成）：精确，与平台 API 一一对应
    lark-cli calendar calendars list

  第三层 — 原始 API（完整覆盖）：可调用 2500+ 飞书 API
    lark-cli api GET /open-apis/calendar/v4/calendars

新手从第一层（快捷命令）开始，进阶需求再用第二/三层。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${domain ? `专注域：${domain.toUpperCase()}` : '上手体验 — 5 个常用域'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${!domain || domain === 'calendar' ? `
📅 日历 — 查看你的日程
  # 今日日程（最常用的第一条命令）
  lark-cli calendar +agenda

  # 本周日程
  lark-cli calendar +agenda --days 7

  # 创建活动（先预览）
  lark-cli calendar +create --title "团队周会" --start "2026-04-06T10:00" --end "2026-04-06T11:00" --dry-run
` : ''}${!domain || domain === 'im' ? `
💬 消息 — 发送和查看消息
  # 发送消息（替换 oc_xxx 为真实 chat ID，先用 --dry-run 预览）
  lark-cli im +messages-send --chat-id oc_xxx --text "你好，来自 lark-cli！" --dry-run

  # 查看群聊最近消息
  lark-cli im +messages-list --chat-id oc_xxx

  # 搜索消息
  lark-cli im +messages-search --query "会议纪要"

  # 获取 chat ID：按名称查找群聊
  lark-cli im +chats-list | grep "你的群名称"
` : ''}${!domain || domain === 'docs' ? `
📄 文档 — 创建和阅读文档
  # 创建文档（先 --dry-run 预览）
  lark-cli docs +create --title "我的第一个文档" --markdown "# 你好\\n\\n内容在这里。" --dry-run

  # 搜索文档
  lark-cli docs +search --query "周报"

  # 阅读文档（替换 doc_xxx 为真实 ID）
  lark-cli docs +read --document-id doc_xxx
` : ''}${!domain || domain === 'task' ? `
✅ 任务 — 管理你的待办
  # 查看我的任务
  lark-cli task +list

  # 创建任务（先 --dry-run）
  lark-cli task +create --title "审查 PR" --due "2026-04-07" --dry-run

  # 完成任务
  lark-cli task +complete --task-id <task-id> --dry-run
` : ''}${!domain || domain === 'contact' ? `
👤 通讯录 — 查找联系人
  # 按姓名搜索
  lark-cli contact +search --name "张三"

  # 按邮箱搜索
  lark-cli contact +search --email "zhangsan@example.com"

  # 查看自己的用户信息
  lark-cli contact +me
` : ''}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
常用标志
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  --dry-run          预览请求，不实际执行（始终安全）
  --format table     人类可读的表格输出
  --format json      完整 JSON 响应（适合脚本/agent）
  --format csv       CSV 输出（适合导入表格）
  --page-all         自动翻页，获取全部结果
  --as user          以用户身份执行（默认）
  --as bot           以机器人身份执行

Schema 查询（不确定参数时使用）：
  lark-cli schema                           # 列出所有服务
  lark-cli schema calendar.events.create   # 查看此接口的参数
  lark-cli schema im.messages.delete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent 引导提示
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

询问用户想要做什么。可主动提供以下选项：
  • "查看今天的日历日程"
  • "向某个群发送一条测试消息"
  • "为我创建一个任务"
  • "搜索我的文档"
  • "按姓名查找一个联系人"

对于用户感兴趣的任何域，使用 lark-cli <service> --help 发现更多命令。
`);
}
