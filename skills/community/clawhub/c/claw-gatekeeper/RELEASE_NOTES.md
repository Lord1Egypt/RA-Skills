# Release v0.1.0

---

## 🎉 Claw Gatekeeper v0.1.0

> A Safety Brake for OpenClaw with Session-Aware Risk Management

---

## English

### 🚀 What's New

OpenClaw Guardian is a comprehensive security control system for OpenClaw that intercepts high-risk operations and requires human confirmation before execution. This is our initial release with full feature set.

### ✨ Key Features

#### 1. Risk-Based Operation Control
- **🔴 CRITICAL (80-100)**: Always requires individual confirmation - no exceptions
- **🟠 HIGH (60-79)**: Requires confirmation, with optional session-level approval
- **🟡 MEDIUM (30-59)**: Suggests confirmation, with optional session-level approval  
- **🟢 LOW (0-29)**: Auto-allowed without interruption

#### 2. Session-Aware Approval System
- Approve MEDIUM/HIGH risk operations once, auto-approve similar operations for the entire session
- Session expires after 30 minutes of inactivity
- CRITICAL operations always require per-confirmation (no session approval)

#### 3. Comprehensive Audit Logging
- All MEDIUM+ operations logged to `Operate_Audit.log`
- Color-coded emoji indicators: 🔴 CRITICAL, 🟠 HIGH, 🟡 MEDIUM
- Timestamped entries with operation details and decisions

#### 4. Multiple Operation Modes
- **Standard Mode**: Balanced protection for daily use
- **Strict Mode**: Maximum security, all non-whitelisted operations require confirmation
- **Loose Mode**: Minimal interruptions, only CRITICAL requires confirmation
- **Emergency Mode**: Complete lockdown, everything requires confirmation

#### 5. Flexible Policy Management
- Whitelist/Blacklist support for paths, commands, domains, and skills
- Configuration import/export
- Automatic backup and restore
- Policy validation

### 📦 Installation

```bash
# Download and install
curl -L -o claw-gatekeeper.skill \
  https://github.com/stephenlzc/claw-gatekeeper/releases/download/v0.1.0/claw-gatekeeper.skill

openclaw skill install claw-gatekeeper.skill
openclaw skill persist claw-gatekeeper

# Initialize
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode standard
```

### 🔧 Core Scripts

| Script | Purpose | Lines |
|--------|---------|-------|
| `risk_engine.py` | Risk assessment engine | ~900 |
| `guardian_ui.py` | User interaction & session logic | ~600 |
| `session_manager.py` | Session state management | ~350 |
| `policy_config.py` | Policy configuration | ~700 |
| `audit_log.py` | Audit trail management | ~650 |

### 🛡️ Security Context

**Important**: This is a temporary security measure for OpenClaw, which has been identified with significant vulnerabilities including:
- CVE-2026-25253 (CVSS 8.8)
- CVE-2026-24763
- CVE-2026-25475
- And more...

Use this skill to add a layer of protection until official security improvements are released.

### 📁 Project Structure

```
claw-gatekeeper/
├── README.md                    # English documentation
├── README.zh-CN.md              # Chinese documentation
├── SKILL.md                     # Skill manifest
├── scripts/                     # Core Python scripts
│   ├── risk_engine.py
│   ├── guardian_ui.py
│   ├── session_manager.py
│   ├── policy_config.py
│   └── audit_log.py
└── references/                  # Documentation
    ├── risk_matrix.md
    └── user_guide.md
```

### 🔗 Links

- **Repository**: https://github.com/stephenlzc/claw-gatekeeper
- **Documentation**: https://raw.githubusercontent.com/stephenlzc/claw-gatekeeper/main/README.md
- **Issues**: https://github.com/stephenlzc/claw-gatekeeper/issues

### 🙏 Acknowledgments

Created in response to security warnings from China CNCERT/CC and the OpenClaw CVE database.

---

## 中文

## 🎉 OpenClaw Guardian v0.1.0

> OpenClaw 的安全刹车系统 - 具备会话感知能力的智能风险管理

---

### 🚀 新增功能

OpenClaw Guardian 是一个全面的 OpenClaw 安全控制系统，可以拦截高风险操作并在执行前要求人工确认。这是我们的初始版本，包含完整的功能集。

### ✨ 核心特性

#### 1. 基于风险的操作控制
- **🔴 严重 (CRITICAL, 80-100)**: 始终需要单独确认，无例外
- **🟠 高 (HIGH, 60-79)**: 需要确认，可选择会话级批准
- **🟡 中 (MEDIUM, 30-59)**: 建议确认，可选择会话级批准
- **🟢 低 (LOW, 0-29)**: 自动允许，无需中断

#### 2. 会话感知批准系统
- 一次批准中等/高风险操作，整个会话内自动批准类似操作
- 会话在 30 分钟无活动后过期
- 严重风险操作始终需要单独确认（无会话批准）

#### 3. 全面的审计日志
- 所有中等及以上风险操作记录到 `Operate_Audit.log`
- 颜色编码的表情符号：🔴 严重、🟠 高、🟡 中
- 带时间戳的条目，包含操作详情和决策

#### 4. 多种操作模式
- **标准模式**: 日常使用，平衡保护
- **严格模式**: 最高安全性，所有非白名单操作需要确认
- **宽松模式**: 最少中断，仅严重风险需要确认
- **紧急模式**: 完全锁定，所有操作需要确认

#### 5. 灵活的策略管理
- 支持路径、命令、域名和 skill 的白名单/黑名单
- 配置导入/导出
- 自动备份和恢复
- 策略验证

### 📦 安装

```bash
# 下载并安装
curl -L -o claw-gatekeeper.skill \
  https://github.com/stephenlzc/claw-gatekeeper/releases/download/v0.1.0/claw-gatekeeper.skill

openclaw skill install claw-gatekeeper.skill
openclaw skill persist claw-gatekeeper

# 初始化
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode standard
```

### 🔧 核心脚本

| 脚本 | 用途 | 代码行数 |
|------|------|---------|
| `risk_engine.py` | 风险评估引擎 | ~900 |
| `guardian_ui.py` | 用户交互与会话逻辑 | ~600 |
| `session_manager.py` | 会话状态管理 | ~350 |
| `policy_config.py` | 策略配置 | ~700 |
| `audit_log.py` | 审计日志管理 | ~650 |

### 🛡️ 安全背景

**重要**: 这是一个针对 OpenClaw 的临时安全措施，OpenClaw 已被发现存在严重漏洞，包括：
- CVE-2026-25253 (CVSS 8.8)
- CVE-2026-24763
- CVE-2026-25475
- 以及更多...

在官方安全改进发布之前，请使用本 skill 增加一层保护。

### 📁 项目结构

```
claw-gatekeeper/
├── README.md                    # 英文文档
├── README.zh-CN.md              # 中文文档
├── SKILL.md                     # Skill 清单
├── scripts/                     # 核心 Python 脚本
│   ├── risk_engine.py
│   ├── guardian_ui.py
│   ├── session_manager.py
│   ├── policy_config.py
│   └── audit_log.py
└── references/                  # 文档
    ├── risk_matrix.md
    └── user_guide.md
```

### 🔗 链接

- **代码仓库**: https://github.com/stephenlzc/claw-gatekeeper
- **文档**: https://raw.githubusercontent.com/stephenlzc/claw-gatekeeper/main/README.md
- **问题反馈**: https://github.com/stephenlzc/claw-gatekeeper/issues

### 🙏 致谢

本项目创建是为了应对中国国家计算机网络应急技术处理协调中心 (CNCERT/CC) 的安全警告以及 OpenClaw CVE 数据库。

---

## 📊 Statistics / 统计

| Metric / 指标 | Value / 数值 |
|---------------|--------------|
| Total Code Lines / 总代码行数 | ~3,400 |
| Documentation Words / 文档字数 | ~20,000 |
| Risk Patterns / 风险检测模式 | 100+ |
| Config Options / 配置选项 | 30+ |

---

## 📝 Changelog / 更新日志

- Initial release with full feature set / 初始版本，包含完整功能集
- Session-aware approval system / 会话感知批准系统
- Risk-based operation control / 基于风险的操作控制
- Comprehensive audit logging / 全面的审计日志
- Multi-language documentation (EN/CN) / 多语言文档（英文/中文）

---

**Full Changelog**: https://github.com/stephenlzc/claw-gatekeeper/commits/v0.1.0
