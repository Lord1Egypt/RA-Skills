---
name: OpenClaw Gateway Guardian
description: OpenClaw 看门狗 - 自动监控 Gateway 状态，宕机时自动重启，支持配置守护和模型故障转移
homepage: https://github.com/zhangss110/openclaw-watchdog
metadata: {"openclaw":{"emoji":"🛡️","requires":{"bins":["python","openclaw"],"env":[]}}}
tags: latest=1.1.0,watchdog=1.1.0,gateway=1.1.0,monitoring=1.1.0,backup=1.1.0,devops=1.1.0,infrastructure=1.1.0
---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/OpenClaw-2026.3%2B-green?style=for-the-badge" alt="OpenClaw">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

<h1 align="center">🛡️ OpenClaw Gateway Guardian / OpenClaw 看门狗</h1>

<p align="center">
  <strong>自动监控 OpenClaw Gateway 状态，宕机时自动重启，支持配置守护和模型故障转移</strong><br>
  <em>Automatically monitor OpenClaw Gateway status, auto-restart on crash, with config guardian and model failover support.</em>
</p>

---

## ✨ 功能特点 / Features

| 功能 | 说明 |
|------|------|
| 🏥 **Gateway 监控** | 自动检测 Gateway 状态（每 15 秒） |
| 🔄 **自动重启** | 宕机 30 秒后自动重启（最多 3 次重试） |
| 🛡️ **配置守护** | 监控配置文件变更，自动备份 |
| 🔀 **模型故障转移** | 主模型失败时自动切换备用模型 |
| 📱 **飞书通知** | 宕机/恢复/配置变更实时通知 |
| 🚀 **开机自启动** | 通过 Windows 计划任务自动运行 |
| 💾 **配置备份** | 自动备份配置文件，支持一键恢复 |

---

## 📦 安装 / Installation

### 方式一：安装脚本（推荐）

```bash
# 直接运行安装脚本
.\scripts\install.bat
```

### 方式二：手动安装

```bash
# 1. 创建看门狗目录
mkdir %USERPROFILE%\.openclaw\watchdog

# 2. 复制文件
copy scripts\* %USERPROFILE%\.openclaw\watchdog\

# 3. 配置（可选）
# 编辑 config.json 设置飞书 Webhook 等

# 4. 启动
python %USERPROFILE%\.openclaw\watchdog\watchdog_simple.py
```

---

## ⚙️ 配置 / Configuration

### 完整配置项

```json
{
  "openclaw": {
    "exePath": "%USERPROFILE%\\AppData\\Roaming\\npm\\openclaw.cmd",
    "dataDir": "%USERPROFILE%\\.openclaw",
    "gatewayPort": 18789
  },
  "watchdog": {
    "checkIntervalMs": 15000,
    "maxDowntimeMs": 30000,
    "maxRetries": 3,
    "stopFlagPath": "%USERPROFILE%\\.openclaw\\stop.flag",
    "logDir": "%USERPROFILE%\\.openclaw\\watchdog\\logs"
  },
  "configGuardian": {
    "enabled": true,
    "checkIntervalSec": 60,
    "alertOnChange": true
  },
  "modelFailover": {
    "enabled": false,
    "primaryModel": "baiduqianfancodingplan/qianfan-code-latest",
    "fallbackModel": "custom-qianfan-baidubce-com/deepseek-v3.2"
  },
  "feishu": {
    "webhookUrl": "YOUR_FEISHU_WEBHOOK_URL"
  }
}
```

### 配置说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `openclaw.exePath` | string | `%USERPROFILE%\AppData\Roaming\npm\openclaw.cmd` | OpenClaw 程序路径 |
| `openclaw.gatewayPort` | number | 18789 | Gateway 端口 |
| `watchdog.checkIntervalMs` | number | 15000 | 检查间隔（毫秒） |
| `watchdog.maxDowntimeMs` | number | 30000 | 最大宕机时间（毫秒） |
| `watchdog.maxRetries` | number | 3 | 最大重试次数 |
| `configGuardian.enabled` | boolean | true | 启用配置守护 |
| `modelFailover.enabled` | boolean | false | 启用模型故障转移 |

### 飞书 Webhook 配置

1. 打开 https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDM14CM4ATN
2. 创建自定义机器人
3. 复制 Webhook URL 到配置文件中

---

## 📖 使用方法 / Usage

### 自动模式（默认）

看门狗会自动监控 Gateway，宕机后自动重启。

```bash
# 启动看门狗
python watchdog_simple.py
```

### 命令行操作

```bash
# 查看状态
python watchdog_simple.py status
# 输出: Gateway Port 18789: UP

# 手动备份
python watchdog_simple.py backup

# 手动恢复
python watchdog_simple.py restore
```

### 手动控制

| 操作 | 命令 |
|------|------|
| 停止自动重启 | `type nul > %USERPROFILE%\.openclaw\stop.flag` |
| 恢复自动重启 | `del %USERPROFILE%\.openclaw\stop.flag` |

---

## 📁 文件结构 / File Structure

```
openclaw-watchdog/
├── SKILL.md                    # 技能说明文档
└── scripts/
    ├── watchdog_simple.py      # 主程序
    ├── config.json             # 配置文件
    └── install.bat             # 安装脚本
```

---

## 📊 日志 / Logs

- **主日志**: `%USERPROFILE%\.openclaw\watchdog\logs\guardian_YYYYMMDD.log`
- **配置备份**: `%USERPROFILE%\.openclaw\watchdog\backup\`

---

## 🔧 开机自启动 / Auto-start on Boot

安装时自动创建 Windows 计划任务：

```cmd
schtasks /create /tn "OpenClaw Gateway Guardian" /tr "python %USERPROFILE%\.openclaw\watchdog\watchdog_simple.py" /sc onlogon /rl limited
```

---

## 🗑️ 卸载 / Uninstall

```cmd
# 删除计划任务
schtasks /delete /tn "OpenClaw Gateway Guardian" /f

# 删除文件（可选）
rmdir /s %USERPROFILE%\.openclaw\watchdog
```

---

## 📝 更新日志 / Changelog

### v1.1.0 (2026-03-26)
- ✨ 新增配置守护功能（监控配置文件变更）
- ✨ 新增模型故障转移支持
- ✨ 优化日志输出格式
- ✨ 增加更多标签（devops, monitoring, infrastructure）
- 🐛 修复多项 Bug

### v1.0.0 (2026-03-20)
- 🎉 初始版本
- ✅ 基本的 Gateway 监控和自动重启
- ✅ 飞书通知支持
- ✅ 配置文件备份/恢复

---

## 📋 依赖 / Dependencies

- Python 3.8+
- OpenClaw 2026.3.22+

---

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证 / License

MIT License

---

<p align="center">🦐 感谢使用！有问题随时提问。</p>
<p align="center">Thanks for using! Feel free to ask questions.</p>
