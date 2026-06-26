# SKILL.md - EXWIND 监控

## 描述
监控 [EXWIND](https://exwind.net/) 网站的更新，每 10 分钟检查一次。

## 触发方式
- **定时**: 每 10 分钟自动执行
- **手动**: 用户说"检查 EXWIND 更新"

## Cron 任务
```bash
openclaw cron list | grep exwind

# 任务配置
ID: 99f28379-aed3-42c1-b33a-e75f5432f90f
Name: exwind-monitor
Schedule: */10 * * * * @ Asia/Shanghai
Delivery: none
```

## 执行脚本
```bash
python3 ~/.openclaw/workspace/skills/exwind-monitor/scripts/exwind_monitor.py
```

---

## 🚨 Agent 执行步骤

### Step 1: 运行监控脚本
```bash
python3 ~/.openclaw/workspace/skills/exwind-monitor/scripts/exwind_monitor.py
```

### Step 2: 检查输出

**如果没有更新：**
```json
{"empty": true}
```
→ 不做任何操作

**如果有更新：**
```json
{
  "empty": false,
  "timestamp": "2026-03-12T17:57:00",
  "message": "## 🔍 EXWIND 更新...",
  "need_send": true
}
```

### Step 3: 发送飞书消息
使用 `message` tool 发送 `message` 字段的内容到飞书。

**发送文字内容，不是文档链接！**

---

## 输出格式

### 消息格式
```markdown
## 🔍 EXWIND 更新 (17:57)

### 📘 蓝帖: 前夕补丁大秘境评分奖励0.1%头衔
📅 2026-03-12 11:10
🔗 https://exwind.net/post/blue/29049483

有玩家因为在正式补丁上线前达到的史诗钥石评分而获得了头衔成就...

---

### 🔧 热修: 3月12日在线修正
📅 2026-03-12 09:01
🔗 https://exwind.net/post/hotfixes/xxx

...
```

### 类型图标
| 类型 | 图标 |
|------|------|
| 蓝帖 | 📘 |
| 热修 | 🔧 |
| 新闻 | 📰 |

---

## 状态文件
- **位置**: `/tmp/exwind_state.json`
- **内容**: 已推送的文章 ID 列表
- **限制**: 最多保留 500 条记录

---

## 故障排除
| 问题 | 解决方案 |
|------|----------|
| 页面打开失败 | 检查 agent-browser |
| 无新文章 | 正常，等待下次检查 |
| 重复推送 | 删除 /tmp/exwind_state.json |

---

## 相关文件
```
~/.openclaw/workspace/skills/exwind-monitor/
├── SKILL.md
└── scripts/
    └── exwind_monitor.py
```

## 更新记录
| 日期 | 变更 |
|------|------|
| 2026-03-12 | 修改为发送飞书消息，不是文档链接 |
| 2026-03-12 | 创建 skill |
