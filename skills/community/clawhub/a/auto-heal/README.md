# 🔧 Auto-Heal for OpenClaw

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/openclaw-community/auto-heal)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/openclaw-compatible-orange.svg)](https://openclaw.ai)

> **7x24 小时守护你的 OpenClaw，自动检测并修复卡死问题**

## ✨ 特性

- 🔍 **智能监控** - 每 5 分钟自动检查系统健康状态
- 🚀 **自动修复** - 检测到卡死自动重启，无需人工干预
- 💾 **内存保护** - 监控内存使用，防止 OOM
- 🧹 **会话清理** - 自动清理僵尸会话，释放资源
- 📝 **完整日志** - 详细记录所有操作，便于排查问题
- ⚡ **轻量级** - 几乎不占用系统资源

## 🚀 快速开始

### 安装

```bash
# 克隆到技能目录
cd ~/.openclaw/workspace/skills
git clone https://github.com/openclaw-community/auto-heal.git

# 进入目录
cd auto-heal

# 一键安装
npm install
```

### 使用

#### 方法1：Cron 定时任务（推荐）

```bash
# 编辑 crontab
crontab -e

# 添加每 5 分钟检查一次
*/5 * * * * cd ~/.openclaw/workspace/skills/auto-heal && npm run check
```

#### 方法2：持续监控模式

```bash
# 前台运行
npm start

# 或后台运行
nohup npm start > /dev/null 2>&1 &
```

#### 方法3：手动检查

```bash
npm run check
```

## ⚙️ 配置

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "skills": {
    "auto-heal": {
      "enabled": true,
      "checkInterval": 60,
      "autoFix": true,
      "memoryThreshold": 80,
      "zombieSessionAge": 30,
      "notifyChannel": "feishu",
      "logRetentionDays": 7
    }
  }
}
```

### 配置说明

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `enabled` | `true` | 是否启用自动修复 |
| `checkInterval` | `60` | 检查间隔（秒） |
| `autoFix` | `true` | 是否自动修复问题 |
| `memoryThreshold` | `80` | 内存告警阈值（%） |
| `zombieSessionAge` | `30` | 僵尸会话判定（分钟） |
| `notifyChannel` | `""` | 通知渠道（如 feishu） |
| `logRetentionDays` | `7` | 日志保留天数 |

## 📊 监控内容

### 1. Gateway 健康
- ✅ 检查 gateway 是否响应
- ✅ 自动重启无响应的 gateway
- ✅ 验证重启后状态

### 2. Agent 会话
- ✅ 检测卡死的会话
- ✅ 清理僵尸会话
- ✅ 释放占用资源

### 3. 系统资源
- ✅ 监控内存使用
- ✅ 清理旧日志文件
- ✅ 防止系统过载

## 📋 日志查看

```bash
# 实时查看日志
tail -f ~/.openclaw/workspace/skills/auto-heal/logs/auto-heal.log

# 查看最近 100 行
tail -n 100 ~/.openclaw/workspace/skills/auto-heal/logs/auto-heal.log

# 查看状态
cat ~/.openclaw/workspace/skills/auto-heal/state.json
```

## 🛠️ 故障排查

### 检查不生效？

1. 确认 OpenClaw CLI 可用：`which openclaw`
2. 检查配置文件权限：`ls -la ~/.openclaw/openclaw.json`
3. 查看日志错误：`tail -n 50 logs/auto-heal.log`

### 自动修复失败？

1. 检查是否有足够权限执行重启命令
2. 确认 gateway 进程可以被正常重启
3. 查看详细错误日志

## 🤝 贡献

欢迎提交 Issue 和 PR！

```bash
# Fork 项目
# 创建分支
git checkout -b feature/amazing-feature

# 提交更改
git commit -m 'Add amazing feature'

# 推送分支
git push origin feature/amazing-feature

# 创建 Pull Request
```

## 📄 许可证

[MIT](LICENSE) © OpenClaw Community

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - 强大的 AI 助手平台
- 所有贡献者和用户

---

**如果这个项目帮到了你，请给个 ⭐ Star！**
