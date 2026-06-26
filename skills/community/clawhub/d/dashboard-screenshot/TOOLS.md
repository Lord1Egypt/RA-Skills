# 📸 Dashboard Screenshot Skill Tools

## Overview
This skill provides automated OpenClaw dashboard screenshot capture and status reporting.

---

## 🔧 Tool Configuration

### 1. Check Service Status
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null
```
**Expected output:** `200` if running

### 2. Start Service (if needed)
```bash
cd ~/.openclaw/OpenClaw-bot-review && npm run dev
```
**Flags:**
- `background: true` - Run in background
- `yieldMs: 8000` - Wait 8 seconds for service startup

### 3. Open Browser
```json
{
  "action": "open",
  "url": "http://localhost:3000"
}
```
**Returns:** `targetId` for subsequent operations

### 4. Wait for Page Load
```json
{
  "action": "snapshot",
  "targetId": "<targetId>",
  "timeoutMs": 5000
}
```
**Verification:**
- Check for "OPENCLAW BOT DASHBOARD" title
- Verify robot cards are visible
- Confirm navigation menu is present

### 5. Capture Full Page
```json
{
  "action": "screenshot",
  "targetId": "<targetId>",
  "fullPage": true,
  "type": "png"
}
```
**Key settings:**
- `fullPage: true` - Capture entire scrollable page
- `type: "png"` - PNG format for quality
- **Auto-saves to:** `~/.openclaw/media/browser/<uuid>.png`

### 6. Send to User
```json
{
  "action": "send",
  "channel": "qqbot",
  "target": "90A776272DF32E657A3242BADFAC5662",
  "media": "~/.openclaw/media/browser/<uuid>.png"
}
```
**Includes:**
- Screenshot image
- Status summary text

---

## 📊 Status Summary Structure

### Robot Cards (每个机器人)
```
呆黄 (main)
├── 状态：空闲/工作中/在线
├── 模型：qwen3.5-plus (api_key) ✅
├── 平台：飞书、Discord、iMessage、QQBot、微信
├── 会话数：19 | 消息数：688 | Token: 23.0k
├── 最近活跃：23 分钟前
└── 平均响应：70.4s ⬆️
```

### Agent Tasks
```
📋 Agent 任务追踪
├── xiaohuang - 执行中
│   ├── 无进行中的子任务
│   └── 无定时任务活动
└── 时间：13:30
```

### Global Stats
```
📈 全局统计趋势
├── 总 Input Token：144.1k
├── 总 Output Token：3.7k
├── 总消息数：731
└── Token 消耗趋势：[图表]
```

### Gateway Health
```
🦞 Gateway 运行正常 ✅
更新于：13:30:56
刷新频率：10 秒
```

---

## 🎯 Trigger Keywords (in SKILL.md)
- "查看仪表盘"
- "dashboard"
- "仪表盘状态"
- "机器人状态"
- "截图仪表盘"

---

## ⚠️ Important Notes

1. **Port 3000** - Default dashboard port
2. **8s wait** - Gives service time to fully initialize
3. **fullPage=true** - Essential for capturing all scrollable content
4. **Background npm** - Prevents blocking subsequent operations
5. **Error handling** - Each step has fallback logic
6. **Browser cleanup** - Close browser after screenshot to free resources

---

## 📁 File Paths

| Resource | Path |
|----------|------|
| Project root | `~/.openclaw/OpenClaw-bot-review/` |
| Config | `package.json` |
| Screenshot output | `~/.openclaw/media/browser/<uuid>.png` |
| Skill definition | `~/.openclaw/workspace/skills/dashboard-screenshot/` |

---

## 🔒 Prerequisites

- OpenClaw Gateway running (port 18789)
- Dashboard app installed (`~/.openclaw/OpenClaw-bot-review/`)
- Browser available (OpenClaw browser or user browser)
- QQBot channel connected
- Port 3000 available (or willing to change)

---

## 🚀 Usage Example

**User says:** "查看仪表盘" or "dashboard"

**Agent responds with:**
1. Progress updates (optional)
2. Complete dashboard screenshot
3. Key statistics summary
4. Confirmation message

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 3000 busy | Kill process or use different port |
| Browser timeout | Increase `timeoutMs` or check browser status |
| Screenshot not saving | Check write permissions to media folder |
| Message not sent | Verify QQBot channel connection |
| Dashboard crashed | Check npm error logs, verify Node.js version |

---

## 📈 Future Improvements

- [ ] Add port configuration option
- [ ] Support multiple robots in one screenshot
- [ ] Add filtering options (show only specific robot)
- [ ] Generate PDF report alongside screenshot
- [ ] Add trend analysis overlay
- [ ] Support WebSocket push updates

---

*Last updated: 2026-03-28*
