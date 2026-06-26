---
name: config-diagnose
description: 智能配置诊断工具，帮助排查配置问题、环境变量、服务状态、文件搜索等。触发词：为什么不能、找不到配置、排查问题、诊断一下。
version: 1.0.0
metadata: 
  openclaw: 
    emoji: "🔍"
    category: "utility"
    version: "1.0.0"
    author: "小帽"
---

# 🔍 配置诊断 Skill

**一句话描述**：当用户遇到「为什么不能」「找不到配置」「不工作」等问题时，自动诊断并给出解决建议。

---

## 🎯 设计思路

### 核心理念
```
用户问题描述 → 关键词识别 → 执行诊断 → 返回结果 + 建议
```

### 诊断层级
```
L1: 快速检查（环境变量、文件存在性）
L2: 深度检查（网络连接、权限验证）
L3: 修复建议（具体操作步骤）
```

---

## 🔧 诊断能力

| 诊断类型 | 检查项 | 触发关键词 |
|---------|--------|-----------|
| **邮件诊断** | EMAIL_* 环境变量、IMAP/SMTP 连接 | 邮件、邮箱、mail、email |
| **API 诊断** | API Key 设置、连接测试、权限范围 | API、Key、Token、认证 |
| **服务诊断** | 端口占用、进程状态、配置文件 | 服务、端口、启动、运行 |
| **文件诊断** | 文件搜索、权限检查、格式验证 | 找不到、文件、not found |
| **技能诊断** | 技能安装、依赖检查、配置完整性 | 技能、skill、安装 |

---

## 📁 文件结构

```
config-diagnose/
├── SKILL.md              # 本文件
├── scripts/
│   ├── diagnose.sh       # 主诊断脚本
│   └── full-diagnose.sh  # 完整系统诊断
└── templates/
    └── report.md         # 诊断报告模板
```

---

## 💻 使用方法

### 命令行
```bash
# 邮件配置诊断
bash ~/.openclaw/workspace/skills/config-diagnose/scripts/diagnose.sh email

# API 配置诊断
bash ~/.openclaw/workspace/skills/config-diagnose/scripts/diagnose.sh api

# 服务状态诊断
bash ~/.openclaw/workspace/skills/config-diagnose/scripts/diagnose.sh service

# 文件搜索
bash ~/.openclaw/workspace/skills/config-diagnose/scripts/diagnose.sh file "token.json"

# 完整诊断
bash ~/.openclaw/workspace/skills/config-diagnose/scripts/full-diagnose.sh
```

### 对话触发
```
用户：为什么我的邮件读取不了？
AI：让我诊断一下邮件配置...
    [调用 diagnose.sh email]
    结果：EMAIL_PASSWORD 未设置
    建议：请设置应用专用密码...

用户：为什么找不到 outlook-cli 的 token.json？
AI：让我帮你搜索...
    [调用 diagnose.sh file "token.json"]
    结果：文件不存在
    建议：需要先运行 outlook-cli login 进行授权
```

---

## 🔄 诊断流程图

```
           用户描述问题
                │
                ▼
       ┌────────────────┐
       │  关键词识别    │
       │  确定诊断类型  │
       └────────────────┘
                │
                ▼
       ┌────────────────┐
       │  执行检查脚本  │
       │  - 环境变量    │
       │  - 文件搜索    │
       │  - 网络测试    │
       │  - 服务状态    │
       └────────────────┘
                │
                ▼
       ┌────────────────┐
       │  分析结果      │
       │  生成诊断报告  │
       └────────────────┘
                │
                ▼
       ┌────────────────┐
       │  提供解决建议  │
       │  可执行命令    │
       └────────────────┘
```

---

## 📋 常见问题诊断表

### 邮件问题

| 问题 | 诊断结果 | 解决建议 |
|------|---------|---------|
| EMAIL_ADDRESS 未设置 | `✗ 未设置` | `export EMAIL_ADDRESS="your@email.com"` |
| EMAIL_PASSWORD 未设置 | `✗ 未设置` | Gmail 需生成应用专用密码 |
| IMAP 连接失败 | `✗ 不可达` | 检查网络或服务器地址 |

### 服务问题

| 问题 | 诊断结果 | 解决建议 |
|------|---------|---------|
| 端口被占用 | `✓ 已使用` | `kill $(lsof -t -i:PORT)` |
| 服务未启动 | `− 未启动` | `npm start` 或对应启动命令 |
| 配置文件缺失 | `✗ 缺失` | 检查配置路径或重新安装 |

### 文件问题

| 问题 | 诊断结果 | 解决建议 |
|------|---------|---------|
| 文件不存在 | `未找到文件` | 检查是否需要先安装/创建 |
| 权限不足 | `Permission denied` | `chmod +x` 或 `sudo` |
| 路径错误 | `路径不存在` | 检查拼写或使用 find 搜索 |

---

## 🎨 输出格式

### 成功
```
✓ 配置完整
✓ 服务运行中
✓ 文件存在
```

### 警告
```
⚠ 未设置（使用默认值）
⚠ 服务未启动
⚠ 文件权限不完整
```

### 错误
```
✗ 未设置（必须配置）
✗ 服务异常
✗ 文件缺失
```

---

## 🔗 与其他 Skill 配合

| 配合技能 | 场景 |
|---------|------|
| `openclaw-email` | 诊断邮件配置后配置邮箱 |
| `deploy` | 部署前诊断配置是否完整 |
| `healthcheck` | 系统健康检查 + 配置诊断 |
| `clawhub` | 诊断技能安装问题 |

---

## 📝 更新日志

### v1.0.0 (2026-03-19)
- 初始版本
- 支持邮件、API、服务、文件、技能诊断
- 完整系统诊断功能
- 彩色输出和建议生成

---

## 🔄 触发模式

### 模式一：被动响应（默认）
用户提问时触发，不主动打扰。

```
用户：为什么我的邮件读取不了？
AI：让我诊断一下... [调用诊断]
```

### 模式二：主动监控（集成 heartbeat）
在定时心跳检查中集成关键诊断，发现严重问题主动提醒。

**检查项**（仅关键问题）：
- Gateway 服务崩溃
- 核心配置文件丢失
- 关键端口服务停止

**触发条件**：
```bash
# 在 HEARTBEAT.md 中添加
- 检查 Gateway 状态
- 检查关键服务端口
- 发现问题 → 主动通知用户
```

### 模式三：智能触发
根据上下文自动判断是否需要诊断。

```
用户：帮我发封邮件
AI：[检测到邮件配置问题] 
    ⚠️ 检测到邮件配置不完整，让我先诊断一下...
    [自动执行邮件诊断]
```

---

## 📋 主动提醒的优先级

| 级别 | 问题类型 | 是否主动提醒 |
|------|---------|-------------|
| 🔴 严重 | Gateway 崩溃、配置丢失 | ✅ 立即提醒 |
| 🟡 警告 | 服务端口停止、依赖缺失 | ✅ 定时提醒 |
| 🔵 信息 | 环境变量未设置 | ❌ 按需触发 |

---

## 🛠️ Heartbeat 集成示例

```bash
# 添加到 heartbeat 检查脚本
check_critical() {
    # 检查 Gateway
    if ! pgrep -f "openclaw gateway" >/dev/null; then
        echo "🔴 严重：Gateway 服务已停止"
        return 1
    fi
    
    # 检查配置文件
    if [ ! -f "/root/.openclaw/openclaw.json" ]; then
        echo "🔴 严重：配置文件丢失"
        return 1
    fi
    
    return 0
}
```

---

## 👤 作者

小帽 (OpenClaw)

## 📅 创建时间

2026-03-19

## 📜 许可证

MIT
