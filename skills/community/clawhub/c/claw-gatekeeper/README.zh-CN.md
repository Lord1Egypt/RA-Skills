# 🛡️ OpenClaw Guardian

> OpenClaw 的安全刹车系统 - OpenClaw Guardian - 具备会话感知能力的智能风险管理

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![中文](https://img.shields.io/badge/语言-中文-red.svg)](README.zh-CN.md)
[![English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)

**[English](README.md) | [中文](README.zh-CN.md)**

---

## ⚠️ 重要声明

**这是一个临时安全措施。**

OpenClaw Guardian 是为了解决 OpenClaw 当前在自主决策能力方面的安全缺陷而创建的。一旦 OpenClaw 实现了全面的内置安全控制，本项目可能会停止维护。

**当前状态**：截至 2026 年 3 月，OpenClaw 已被发现存在严重的安全漏洞，包括多个 CVE 和国家安全机构的警告。在官方安全改进发布之前，请使用本 skill 增加一层保护。

---

## 🎯 什么是 Claw-Gatekeeper？

OpenClaw Guardian 是 OpenClaw 的**持久化安全层**，可以拦截潜在的危险操作，并根据风险级别进行智能管理，支持会话感知的批准机制。

### 基于风险的行为控制

| 风险级别 | 分数 | 默认行为 | 会话批准 |
|----------|------|----------|----------|
| 🔴 **严重 (CRITICAL)** | 80-100 | 每次都需要单独确认 | ❌ 不可用 |
| 🟠 **高 (HIGH)** | 60-79 | 首次确认后，可批准整个会话 | ✅ 可用 |
| 🟡 **中 (MEDIUM)** | 30-59 | 首次确认后，可批准整个会话 | ✅ 可用 |
| 🟢 **低 (LOW)** | 0-29 | 自动允许，无需中断 | N/A |

### 会话感知批准机制

**核心创新**：在首次确认一个中等或高风险操作后，您可以选择**批准整个会话**。相似的操作将在以下情况前自动获得批准：
- 会话过期（30 分钟无活动）
- 您明确撤销批准
- OpenClaw 重启

**严重风险操作始终需要单独确认** - 为了最大程度的安全，不提供会话批准。

---

## 📦 安装

### 给人类用户

复制粘贴这段提示给你的 LLM 代理（Claude Code、Cursor、Cline 等）：

```
按照这里的说明安装和配置 Claw-Guardian： https://raw.githubusercontent.com/stephenlzc/claw-gatekeeper/main/README.zh-CN.md ，将其设置为常驻 skill，并使用标准模式。或者继续阅读本 README，但说真的，让代理来做吧。人类容易把配置搞砸。
```

### 给 LLM 代理

获取并执行安装：

```bash
# 下载并安装
curl -L -o claw-gatekeeper.skill https://github.com/stephenlzc/claw-gatekeeper/releases/latest/download/claw-guardian.skill
openclaw skill install claw-guardian.skill
openclaw skill persist claw-guardian

# 初始化配置
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode standard
```

### 跳过本 README

我们已经过了阅读文档的时代。直接粘贴这段给你的代理：

> 阅读并设置 Claw-Guardian 作为 OpenClaw 的持久化安全层：  
> https://raw.githubusercontent.com/stephenlzc/claw-gatekeeper/main/README.zh-CN.md

---

## 🚀 快速开始

### 基本使用

安装为常驻 skill 后，Claw-Guardian 会自动管理操作：

```
[OpenClaw] 我要删除旧的临时文件

[Claw-Guardian] 🟡 中等风险
============================================================
📋 操作：📁 文件操作
📝 详情：删除 ~/temp/ (45 个文件)
🟡 风险级别：中等
📊 风险评分：45/100

⚠️ 风险分析：
   1. 批量操作 (45 个文件)
   2. 目录删除

选择操作：
   [y] ✅ 仅允许这次
   [s] ✅📅 允许本次会话 ⭐ 推荐
   [Y] ✅✅ 总是允许（加入白名单）
   [n] ❌ 拒绝这次
   [N] ❌❌ 总是拒绝（加入黑名单）

您的选择：s

✅ 已批准本次会话
📌 类似操作将自动批准
```

后续类似操作：
```
[OpenClaw] 删除更多临时文件

[Claw-Guardian] 🟡 中等风险 - 会话已批准 ✅
           自动允许（无需提示）
```

### 查看会话状态

```bash
# 检查当前会话
python3 ~/.claw-gatekeeper/scripts/guardian_ui.py session

# 查看活跃批准
python3 ~/.claw-gatekeeper/scripts/session_manager.py list

# 查看审计日志
python3 ~/.claw-gatekeeper/scripts/session_manager.py check --lines 50
```

---

## 📝 Operate_Audit.log 审计日志

所有中等及以上风险的操作都会记录到 `~/.claw-guardian/sessions/Operate_Audit.log`：

```
[2026-03-12 14:30:25.123] [🟠 HIGH] [skill] allow_session: 从 github 安装 data-processor
[2026-03-12 14:31:10.456] [🟡 MEDIUM] [file] allow_session: 删除 ~/temp/cache
[2026-03-12 14:32:05.789] [🔴 CRITICAL] [shell] allow_once: rm -rf ~/Projects/test
[2026-03-12 14:35:15.234] [🟠 HIGH] [skill] deny_once: 拒绝安装来自未知源的 suspicious-tool
```

### 日志格式

```
[时间戳] [表情 风险级别] [操作类型] 决策: 操作详情
```

### 查看日志

```bash
# 最近 100 条记录
python3 ~/.claw-gatekeeper/scripts/session_manager.py check --lines 100

# 导出到文件
python3 ~/.claw-gatekeeper/scripts/session_manager.py check --lines 1000 > audit.txt
```

---

## ⚙️ 配置说明

### 操作模式

```bash
# 标准模式（推荐）
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode standard

# 严格模式（最高安全性）
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode strict

# 宽松模式（最少中断）
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode loose

# 紧急模式（所有操作都需要确认）
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode emergency
```

### 会话超时设置

默认：30 分钟无活动后过期

修改 `~/.claw-guardian/config.json`：
```json
{
  "session_timeout": 3600
}
```

### 白名单管理

```bash
# 添加信任路径
python3 ~/.claw-gatekeeper/scripts/policy_config.py add whitelist paths ~/Projects

# 添加信任命令
python3 ~/.claw-gatekeeper/scripts/policy_config.py add whitelist commands "git status"

# 添加信任 skill
python3 ~/.claw-gatekeeper/scripts/policy_config.py add whitelist skills docx
```

---

## 📁 项目结构

```
claw-guardian/
├── README.md                    # 英文文档
├── README.zh-CN.md              # 中文文档（本文件）
├── SKILL.md                     # Skill 主文档
├── scripts/                     # 5个核心脚本
│   ├── risk_engine.py          # 风险评估引擎
│   ├── guardian_ui.py          # 用户交互 + 会话逻辑
│   ├── session_manager.py      # 会话状态管理
│   ├── policy_config.py        # 策略配置
│   └── audit_log.py            # 审计日志管理
└── references/
    ├── risk_matrix.md          # 风险评分参考
    └── user_guide.md           # 详细用户指南
```

### 重要文件位置

- **配置**：`~/.claw-guardian/config.json`
- **会话状态**：`~/.claw-guardian/sessions/current_session.json`
- **审计日志**：`~/.claw-guardian/sessions/Operate_Audit.log`
- **备份**：`~/.claw-guardian/backups/`

---

## 🔒 安全背景

### 为什么需要会话级批准？

传统的安全工具会中断每个有风险的操作，导致：
- **工作流程中断** - 开发过程中不断弹窗
- **警报疲劳** - 用户开始忽略警告
- **规避行为** - 用户为了省事把所有操作加入白名单

**会话级批准提供：**
- ✅ **安全性**：首次操作始终需要确认
- ✅ **便利性**：会话内相似操作自动批准
- ✅ **可控性**：无活动后会话过期
- ✅ **可审计性**：所有操作记录到 Operate_Audit.log

### 严重风险与会话批准

**严重风险（80-100 分）** - 不提供会话批准：
- `rm -rf /` 或系统目录删除
- 磁盘格式化
- 访问凭证文件
- 系统配置更改

**中等/高风险（30-79 分）** - 提供会话批准：
- 用户目录中的文件删除
- Skill 安装
- 网络请求
- Shell 命令执行

---

## 🔗 快速链接

- **代码仓库**：https://github.com/stephenlzc/claw-gatekeeper
- **发布版本**：https://github.com/stephenlzc/claw-gatekeeper/releases
- **问题反馈**：https://github.com/stephenlzc/claw-gatekeeper/issues
- **原始文档**：https://raw.githubusercontent.com/stephenlzc/claw-gatekeeper/main/README.zh-CN.md

---

## 🤝 参与贡献

欢迎在以下方面贡献：
- 额外的风险检测模式
- 会话管理改进
- 文档完善
- 安全增强

---

## 📄 许可证

MIT 许可证 - 详见 LICENSE 文件。

---

## 🙏 致谢

本项目创建是为了应对：
- [中国国家计算机网络应急技术处理协调中心 (CNCERT/CC) 安全警告](https://www.chinadaily.com.cn/)
- [OpenClaw CVE 数据库](https://cve.mitre.org/)
- 社区对 AI 代理安全的担忧

**免责声明**：这是一个社区创建的安全工具，不是 OpenClaw 官方产品。使用风险自负。

---

<div align="center">

**OpenClaw Guardian** - 安全为本，便利为辅 🛡️

*信任，但验证。对于严重风险，再验证一次。*

[English](README.md) | [中文](README.zh-CN.md)

</div>
