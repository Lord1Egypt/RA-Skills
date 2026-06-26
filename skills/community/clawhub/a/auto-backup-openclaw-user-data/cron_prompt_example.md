# cron_prompt_example.md - OpenClaw Cron 定时任务模板

> 此模板用于配置 OpenClaw Cron 定时任务，实现精确时间自动备份

---

## 📋 模板说明

**适用场景**：
- 需要精确定时执行（如每天凌晨 3:20）
- 独立会话运行（不影响主会话上下文）
- 可指定不同模型执行
- 支持一次性提醒和周期性任务

**配置位置**：
- `~/.openclaw/cron/jobs.json`（定时任务配置文件）
- 或通过 CLI：`openclaw cron add`

**运行机制**：Cron 调度器在精确时间触发，在隔离会话中执行任务

---

## 🔧 配置示例（jobs.json 格式）

```json
{
  "version": 1,
  "jobs": [
    {
      "id": "backup-openclaw-daily",
      "agentId": "secretary",
      "name": "OpenClaw 数据备份 - 每日凌晨",
      "enabled": true,
      "schedule": {
        "kind": "cron",
        "expr": "20 3 * * *",
        "tz": "Asia/Shanghai"
      },
      "sessionTarget": "isolated",
      "wakeMode": "now",
      "payload": {
        "kind": "agentTurn",
        "message": "请执行 OpenClaw 数据备份任务，完成后推送备份结果报告。\n\n【第一步：执行备份】\n在目录 <SKILL_DIR> 下执行以下命令：\nnode -e \"const {runCommand}=require('./cli');runCommand('backup_now',{full:true}).then(r=>console.log(JSON.stringify(r,null,2))).catch(e=>{console.error(e.message);process.exit(1)})\"\n\n解析命令输出的 JSON 结果，提取以下字段用于填充消息模板：\n- success: true/false（判断成功或失败）\n- outputPath: 备份文件完整路径\n- filesTotal: 文件数量\n- sizeBytes: 文件大小（字节）\n- duration: 执行耗时（毫秒）\n- timestamp: 执行完成时间\n- errors: 错误信息数组（失败时）\n\n【第二步：推送备份报告】\n\n📌 推送顺序：先飞书，后 Telegram\n\n📌 飞书推送（feishu_im_user_message）：\n- action: send\n- receive_id_type: chat_id\n- receive_id: <FEISHU_CHAT_ID>\n- msg_type: text\n- content: JSON字符串 {\"text\": \"消息内容\"}\n\n📌 Telegram推送（curl）：\ncurl -X POST \"https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/sendMessage\" -H \"Content-Type: application/json\" -d \"{\\\"chat_id\\\":<TELEGRAM_CHAT_ID>,\\\"text\\\":\\\"消息内容\\\",\\\"parse_mode\\\":\\\"Markdown\\\"}\"\n\n【消息模板 - 备份成功时填入】\n✅ OpenClaw 数据备份成功\n\n📦 备份文件：{从outputPath提取文件名}\n📊 文件数量：{filesTotal} 个\n📏 文件大小：{按KB/MB/GB格式化sizeBytes}\n⏱️ 执行耗时：{按秒/分格式化duration}\n🕐 执行时间：{格式：YYYY-MM-DD HH:mm:ss}\n📁 存储位置：{outputPath}\n\n【消息模板 - 备份失败时填入】\n❌ OpenClaw 数据备份失败\n\n🚨 错误信息：{errors数组.join('; ')}\n🕐 失败时间：{timestamp}\n💡 建议：请检查日志文件 ~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/backup.log\n\n【重要约束】\n- ✅ 消息内容必须基于备份命令的实际执行结果，不得杜撰\n- ✅ 两个渠道推送内容必须完全一致\n- ✅ 消息格式为纯文本 + emoji\n- ✅ 推送顺序：飞书 → Telegram\n- ✅ 备份完成后关闭所有临时文件/页面",
        "timeoutSeconds": 600
      },
      "delivery": {
        "mode": "none",
        "channel": "last"
      }
    }
  ]
}
```

---

## ⚙️ 配置变量说明

| 变量 | 说明 | 示例值 |
|------|------|--------|
| `<SKILL_DIR>` | skill 脚本目录路径 | `~/.agents/skills/auto-backup-openclaw-user-data/scripts` |
| `<FEISHU_CHAT_ID>` | 飞书群组 ID | `oc_xxxxxxxxxxxxxxxxxxxxxxxx` |
| `<TELEGRAM_BOT_TOKEN>` | Telegram Bot Token | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `<TELEGRAM_CHAT_ID>` | Telegram 聊天 ID | `123456789` |

---

## 📝 Cron 表达式说明

### 格式

```
分钟 小时 日 月 星期
```

### 常用示例

| 表达式 | 说明 |
|--------|------|
| `20 3 * * *` | 每天凌晨 03:20 |
| `0 4 * * *` | 每天凌晨 04:00 |
| `0 3 * * 0` | 每周日凌晨 03:00 |
| `0 3 1 * *` | 每月 1 日凌晨 03:00 |
| `30 8,12,18 * * *` | 每天 08:30、12:30、18:30 |
| `0 */6 * * *` | 每 6 小时一次 |

---

## 🚀 CLI 配置命令

### 添加定时任务

```bash
openclaw cron add \
  --name "OpenClaw 数据备份 - 每日凌晨" \
  --cron "20 3 * * *" \
  --tz "Asia/Shanghai" \
  --agent secretary \
  --session isolated \
  --message "请执行 OpenClaw 数据备份任务..." \
  --timeout 600
```

### 查看定时任务

```bash
openclaw cron list
```

### 启用/禁用定时任务

```bash
openclaw cron enable <job-id>
openclaw cron disable <job-id>
```

### 删除定时任务

```bash
openclaw cron delete <job-id>
```

---

## 📋 Prompt 内容模板（完整版）

以下是可以直接复制到 `payload.message` 的完整 Prompt 内容：

---

**请执行 OpenClaw 数据备份任务，完成后推送备份结果报告。**

**【第一步：执行备份】**

在目录 `{SKILL_DIR}` 下执行以下命令：

```bash
node -e "const {runCommand}=require('./cli');runCommand('backup_now',{full:true}).then(r=>console.log(JSON.stringify(r,null,2))).catch(e=>{console.error(e.message);process.exit(1})"
```

解析命令输出的 JSON 结果，提取以下字段用于填充消息模板：

| 字段 | 说明 |
|------|------|
| `success` | true/false（判断成功或失败） |
| `outputPath` | 备份文件完整路径 |
| `filesTotal` | 文件数量 |
| `sizeBytes` | 文件大小（字节） |
| `duration` | 执行耗时（毫秒） |
| `timestamp` | 执行完成时间 |
| `errors` | 错误信息数组（失败时） |

**【第二步：推送备份报告】**

📌 **推送顺序**：先飞书，后 Telegram

📌 **飞书推送（feishu_im_user_message）**：

```javascript
{
  action: "send",
  receive_id_type: "chat_id",
  receive_id: "{FEISHU_CHAT_ID}",
  msg_type: "text",
  content: '{"text": "消息内容"}'
}
```

📌 **Telegram推送（curl）**：

```bash
curl -X POST "https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{"chat_id":{TELEGRAM_CHAT_ID},"text":"消息内容","parse_mode":"Markdown"}'
```

**【消息模板 - 备份成功时填入】**

```
✅ OpenClaw 数据备份成功

📦 备份文件：{从outputPath提取文件名}
📊 文件数量：{filesTotal} 个
📏 文件大小：{按KB/MB/GB格式化sizeBytes}
⏱️ 执行耗时：{按秒/分格式化duration}
🕐 执行时间：{格式：YYYY-MM-DD HH:mm:ss}
📁 存储位置：{outputPath}
```

**【消息模板 - 备份失败时填入】**

```
❌ OpenClaw 数据备份失败

🚨 错误信息：{errors数组.join('; ')}
🕐 失败时间：{timestamp}
💡 建议：请检查日志文件 ~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/backup.log
```

**【重要约束】**

- ✅ 消息内容必须基于备份命令的**实际执行结果**，不得杜撰
- ✅ 两个渠道推送内容必须**完全一致**
- ✅ 消息格式为**纯文本 + emoji**
- ✅ 推送顺序：飞书 → Telegram
- ✅ 备份完成后关闭所有临时文件/页面

---

## 💡 快速配置步骤

### 1. 准备配置信息

收集以下信息：

| 信息 | 获取方式 |
|------|----------|
| skill 脚本目录 | skill 安装位置，通常为 `~/.agents/skills/auto-backup-openclaw-user-data/scripts` |
| 飞书群组 ID | 飞书群设置中查看（格式：`oc_xxx`） |
| Telegram Bot Token | 创建 Telegram Bot 时获取 |
| Telegram Chat ID | 将 @userinfobot 添加到群组获取 |

### 2. 编辑 jobs.json

打开 `~/.openclaw/cron/jobs.json`，将上述配置示例添加到 `jobs` 数组中。

### 3. 替换变量

将 `<SKILL_DIR>`、`<FEISHU_CHAT_ID>`、`<TELEGRAM_BOT_TOKEN>`、`<TELEGRAM_CHAT_ID>` 替换为实际值。

### 4. 修改执行时间

根据需要修改 `schedule.expr` 的 cron 表达式：

```json
"schedule": {
  "kind": "cron",
  "expr": "20 3 * * *",  // 每天凌晨 03:20
  "tz": "Asia/Shanghai"
}
```

### 5. 重启 Gateway

```bash
openclaw gateway restart
```

---

## 🔍 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 定时任务未执行 | Gateway 未运行 | `openclaw gateway start` |
| 任务执行失败 | skill 路径错误 | 检查 `SKILL_DIR` 配置 |
| 没有收到推送 | 推送配置错误 | 检查飞书/Telegram ID |
| 任务超时 | timeoutSeconds 过小 | 增加 timeout 配置 |
| 任务被跳过 | enabled: false | 设置 `enabled: true` |

---

## 📊 与 HEARTBEAT 对比

| 特性 | Cron 定时任务 | HEARTBEAT |
|------|---------------|-----------|
| 定时精度 | ✅ 精确到分钟 | 约 30 分钟漂移 |
| 运行上下文 | ✅ 隔离会话 | 主会话共享 |
| 配置方式 | jobs.json / CLI | HEARTBEAT.md |
| 推送控制 | ✅ 内置支持 | 需手动实现 |
| 模型覆盖 | ✅ 可指定模型 | 使用默认模型 |
| 一次性任务 | ✅ 支持 `--at` | 不支持 |

**建议**：需要精确时间执行时，优先使用 Cron 定时任务。

---

## 📚 相关文档

- [OpenClaw Cron 定时任务文档](/automation/cron-jobs)
- [心跳 vs Cron 对比](/automation/cron-vs-heartbeat)
- [本项目 README.md](README.md)
- [本项目 USAGE.md](USAGE.md)
- [HEARTBEAT 模板](HEARTBEAT_prompt_example.md)

---

_模板版本：v1.1.0.20260414 | 更新日期：2026-04-14_