# HEARTBEAT_prompt_example.md - OpenClaw 心跳定时任务模板

> 此模板用于配置 OpenClaw Agent 的 HEARTBEAT.md，实现周期性自动备份检查

---

## 📋 模板说明

**适用场景**：
- 周期性监控检查（约 30 分钟间隔）
- 不要求精确执行时间
- 可与其他周期性任务批量处理

**配置位置**：Agent 工作区的 `HEARTBEAT.md` 文件

**运行机制**：Gateway 每 N 分钟触发一次心跳轮次，Agent 执行检查清单

---

## 🔧 模板内容（复制到 HEARTBEAT.md）

```md
# HEARTBEAT.md - OpenClaw 数据自动备份心跳任务

---

## 心跳检查清单

每 N 分钟执行以下检查（N 由 `agents.defaults.heartbeat.every` 配置，默认 30m）：

---

### 一、定时备份检查

**检查逻辑**：

1. 获取当前时间（默认Asia/Shanghai 时区）
2. 判断是否到达预定的备份执行时间：
   - 默认执行时间：每天凌晨 03:00
   - 可自定义：修改下方 `BACKUP_TIME` 变量
3. 如果当前时间在预定时间前后 30 分钟内，执行备份

---

### 二、执行备份任务

**当需要执行备份时，按以下步骤操作**：

#### Step 1：执行备份命令

在 skill 脚本目录下执行：

```bash
# 备份脚本目录（请根据实际安装路径修改）
SKILL_DIR=~/.agents/skills/auto-backup-openclaw-user-data/scripts

# 执行全量备份
cd $SKILL_DIR && node -e "const {runCommand}=require('./cli');runCommand('backup_now',{full:true}).then(r=>console.log(JSON.stringify(r,null,2))).catch(e=>{console.error(e.message);process.exit(1)})"
```

#### Step 2：解析备份结果

从命令输出的 JSON 中提取：

| 字段 | 说明 |
|------|------|
| `success` | true/false（判断成功或失败） |
| `outputPath` | 备份文件完整路径 |
| `filesTotal` | 文件数量 |
| `sizeBytes` | 文件大小（字节） |
| `duration` | 执行耗时（毫秒） |
| `timestamp` | 执行完成时间 |
| `errors` | 错误信息数组（失败时） |

#### Step 3：格式化文件大小和耗时

- 文件大小：bytes → KB/MB/GB（自动选择合适单位）
- 执行耗时：ms → 秒/分钟（自动选择合适单位）

#### Step 4：推送备份报告

**推送顺序**：先飞书，后 Telegram（或其他配置渠道）

**飞书推送示例**：
```javascript
// 使用 feishu_im_user_message 工具
{
  action: "send",
  receive_id_type: "chat_id",
  receive_id: "oc_xxx", // 替换为实际群组 ID
  msg_type: "text",
  content: "{\"text\": \"备份报告内容\"}"
}
```

**Telegram 推送示例**：
```bash
curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\":<CHAT_ID>,\"text\":\"备份报告内容\",\"parse_mode\":\"Markdown\"}"
```

---

### 三、消息模板

#### 备份成功模板

```
✅ OpenClaw 数据备份成功

📦 备份文件：{从 outputPath 提取文件名}
📊 文件数量：{filesTotal} 个
📏 文件大小：{格式化后的 sizeBytes}
⏱️ 执行耗时：{格式化后的 duration}
🕐 执行时间：{YYYY-MM-DD HH:mm:ss}
📁 存储位置：{outputPath}
```

#### 备份失败模板

```
❌ OpenClaw 数据备份失败

🚨 错误信息：{errors 数组 join('; ')}
🕐 失败时间：{timestamp}
💡 建议：请检查日志文件 ~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/backup.log
```

---

### 四、心跳响应约定

- **需要执行备份时**：执行备份 → 推送报告 → 回复 `HEARTBEAT_OK`（如果无其他事项）
- **不需要执行备份时**：直接回复 `HEARTBEAT_OK`（不做任何消息发送）
- **备份执行后**：无论成功或失败，推送报告后都回复 `HEARTBEAT_OK`

---

## ⚙️ 配置变量（请根据实际情况修改）

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `BACKUP_TIME` | 预定备份时间（HH:MM 格式） | `03:00` |
| `SKILL_DIR` | skill 脚本目录路径 | `~/.agents/skills/auto-backup-openclaw-user-data/scripts` |
| `FEISHU_CHAT_ID` | 飞书推送群组 ID | 需配置 |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | 需配置 |
| `TELEGRAM_CHAT_ID` | Telegram 聊天 ID | 需配置 |

---

## 📝 重要约束

1. ✅ 消息内容必须基于备份命令的**实际执行结果**，不得杜撰
2. ✅ 所有推送渠道的内容必须**完全一致**
3. ✅ 消息格式为**纯文本 + emoji**（不使用 Markdown 加粗）
4. ✅ 推送顺序：飞书 → Telegram
5. ✅ 只在预定的备份时间前后 30 分钟内执行（避免频繁执行）
6. ✅ 同一天内只执行一次（通过 lastRun 判断）
7. ✅ 执行完成后回复 `HEARTBEAT_OK`（遵循心跳响应约定）

---

## 🚀 快速配置步骤

### 1. 复制模板内容

将上述模板内容复制到你的 Agent 工作区的 `HEARTBEAT.md` 文件中。

### 2. 修改配置变量

根据你的实际情况，修改以下配置：

- `BACKUP_TIME`：你希望的备份执行时间
- `SKILL_DIR`：skill 实际安装路径
- `FEISHU_CHAT_ID`：飞书群组 ID（格式：`oc_xxx`）
- `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID`：Telegram 推送配置

### 3. 配置心跳间隔

在 `openclaw.json` 中配置心跳间隔：

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",  // 每 30 分钟检查一次
        target: "last",  // 推送到最后使用的渠道
      },
    },
  },
}
```

### 4. 启动 Gateway

确保 Gateway 正在运行：

```bash
openclaw gateway start
```

---

## 🔍 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 心跳没有执行 | Gateway 未运行 | `openclaw gateway start` |
| 备份命令执行失败 | skill 路径错误 | 检查 `SKILL_DIR` 配置 |
| 没有收到推送 | 推送目标 ID 错误 | 检查飞书群 ID / Telegram ID |
| 备份频繁执行 | 时间判断逻辑错误 | 检查 `BACKUP_TIME` 和检查逻辑 |
| HEARTBEAT_OK 被发送 | 正常行为 | 无需处理，这是心跳确认 |

---

## 📚 相关文档

- [OpenClaw 心跳文档](/gateway/heartbeat)
- [心跳 vs Cron 对比](/automation/cron-vs-heartbeat)
- [本项目 README.md](README.md)
- [本项目 USAGE.md](USAGE.md)

---

_模板版本：v1.1.0.20260414 | 更新日期：2026-04-14_
```

---

## 💡 使用建议

### HEARTBEAT 适用场景

| 场景 | 推荐使用 |
|------|----------|
| 每日凌晨备份 | ✅ 适合（配合时间判断逻辑） |
| 周期性监控检查 | ✅ 非常适合 |
| 精确时间执行 | ❌ 建议使用 Cron 定时任务 |
| 需要独立上下文 | ❌ 建议使用 Cron 定时任务 |

### 与 Cron 定时任务对比

| 特性 | HEARTBEAT | Cron |
|------|-----------|------|
| 定时精度 | 约 30 分钟漂移 | 精确到分钟 |
| 运行上下文 | 主会话（共享） | 隔离会话 |
| 配置复杂度 | 较简单 | 需要 CLI 配置 |
| 推送控制 | 需手动实现 | 内置支持 |

---

_如果需要精确时间执行，请参考 `cron_prompt_example.md` 使用 Cron 定时任务方案。_