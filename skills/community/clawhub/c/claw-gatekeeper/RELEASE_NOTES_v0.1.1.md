# Release v0.1.1

---

## 🛡️ Claw Gatekeeper v0.1.1

> Enhanced Security with Zero-Code Hardening Mode

---

## English

### 🚀 What's New in v0.1.1

This release introduces a **zero-code-change security hardening system** that enables maximum protection without modifying Guardian's core code. Perfect for users handling sensitive data or operating in compliance-regulated environments.

### ✨ New Features

#### 1. One-Click Security Hardening
```bash
./deploy-secure.sh --apply
```
Deploy maximum security mode with a single command:
- ✅ 100% human-in-the-loop approval (all risk levels)
- ✅ Enhanced blacklist with 20+ dangerous command patterns
- ✅ Expanded sensitive directory protection
- ✅ Secure audit logging with 30-day retention
- ✅ Automatic permission hardening

#### 2. Data Sanitization Tool
```bash
./sanitizer.sh --file conversation.txt > clean.txt
```
Pre-process content to remove sensitive data before Guardian analysis:
- **30+ detection patterns** covering credentials, tokens, PII
- Cloud provider keys (AWS, Azure, GCP)
- API keys (GitHub, OpenAI, Stripe, etc.)
- Cryptocurrency wallets
- Personal information (email, credit card, SSN)
- Security certificates (JWT, RSA, SSH keys)

#### 3. Human-in-the-Loop Mode
Achieve true human-in-the-loop security without code modifications:

| Risk Level | Default Mode | Hardened Mode |
|------------|--------------|---------------|
| 🔴 CRITICAL | Always confirm | Always confirm |
| 🟠 HIGH | Confirm | **Confirm** |
| 🟡 MEDIUM | Confirm | **Confirm** |
| 🟢 LOW | Auto-allow | **Confirm** |

#### 4. Enhanced Security Configurations
New `config.hardened.json` with:
- Stricter command blacklists (pipe execution, reverse shells)
- Extended path blacklists (container configs, shell histories)
- Network restrictions (private IP ranges)
- Fail-secure defaults

### 📦 Files Added

| File | Purpose | Lines |
|------|---------|-------|
| `config/config.hardened.json` | Maximum security configuration | ~150 |
| `scripts/deploy-secure.sh` | One-click hardening deployment | ~280 |
| `scripts/sanitizer.sh` | Sensitive data detection & redaction | ~260 |
| `SECURITY.md` | Comprehensive hardening guide | ~200 |

### 🔧 Usage Examples

**Deploy hardened mode:**
```bash
cd ~/.claw-gatekeeper/scripts
./deploy-secure.sh --apply
```

**Check security status:**
```bash
./deploy-secure.sh --check
```

**Sanitize sensitive data:**
```bash
./sanitizer.sh --check session.json --verbose
./sanitizer.sh --stdin < log.txt > clean.txt
```

**Restore default mode:**
```bash
./deploy-secure.sh --restore
```

### 🛡️ Security Improvements

| Metric | v0.1.0 | v0.1.1 | Improvement |
|--------|--------|--------|-------------|
| Human confirmation coverage | 40% | **100%** | +60% |
| Dangerous command patterns | 5 | **20+** | +300% |
| Protected directories | 4 | **10+** | +150% |
| Data sanitization | ❌ | **✅ 30+ patterns** | New |
| One-click hardening | ❌ | **✅** | New |

### 📊 Statistics

| Metric | Value |
|--------|-------|
| Total code lines | ~3,400 (core) + ~700 (security tools) |
| Documentation words | ~25,000 |
| Risk patterns | 100+ |
| Sensitive data patterns | 30+ |
| Security configurations | 3 modes (default, strict, hardened) |

---

## 中文

## 🛡️ OpenClaw Guardian v0.1.1

> 零代码改动的安全加固模式

---

### 🚀 v0.1.1 新增功能

本次发布引入了**无需修改代码的安全加固系统**，让用户能够以最高保护级别运行 Guardian。特别适合处理敏感数据或在合规要求严格的环境中使用。

### ✨ 新特性

#### 1. 一键安全加固
```bash
./deploy-secure.sh --apply
```
一条命令部署最高安全模式：
- ✅ 100% 人机回环确认（所有风险等级）
- ✅ 增强黑名单，包含 20+ 危险命令模式
- ✅ 扩展敏感目录保护
- ✅ 安全审计日志，30天自动清理
- ✅ 自动权限加固

#### 2. 数据脱敏工具
```bash
./sanitizer.sh --file conversation.txt > clean.txt
```
在 Guardian 分析前预处理内容，移除敏感数据：
- **30+ 检测模式**，覆盖凭证、令牌、个人信息
- 云服务商密钥（AWS、Azure、GCP）
- API 密钥（GitHub、OpenAI、Stripe 等）
- 加密货币钱包地址
- 个人信息（邮箱、信用卡、SSN）
- 安全证书（JWT、RSA、SSH 密钥）

#### 3. 人机回环模式
无需修改代码即可实现真正的人机回环安全：

| 风险等级 | 默认模式 | 加固模式 |
|---------|---------|---------|
| 🔴 严重 (CRITICAL) | 始终确认 | 始终确认 |
| 🟠 高 (HIGH) | 需要确认 | **需要确认** |
| 🟡 中 (MEDIUM) | 需要确认 | **需要确认** |
| 🟢 低 (LOW) | 自动允许 | **需要确认** |

#### 4. 增强安全配置
新增 `config.hardened.json`，包含：
- 更严格的命令黑名单（管道执行、反向 shell）
- 扩展路径黑名单（容器配置、shell 历史）
- 网络限制（私有 IP 段）
- 故障安全默认设置

### 📦 新增文件

| 文件 | 用途 | 代码行数 |
|------|------|---------|
| `config/config.hardened.json` | 最高安全配置 | ~150 |
| `scripts/deploy-secure.sh` | 一键加固部署脚本 | ~280 |
| `scripts/sanitizer.sh` | 敏感数据检测与脱敏 | ~260 |
| `SECURITY.md` | 详细加固指南 | ~200 |

### 🔧 使用示例

**部署加固模式：**
```bash
cd ~/.claw-gatekeeper/scripts
./deploy-secure.sh --apply
```

**检查安全状态：**
```bash
./deploy-secure.sh --check
```

**脱敏敏感数据：**
```bash
./sanitizer.sh --check session.json --verbose
./sanitizer.sh --stdin < log.txt > clean.txt
```

**恢复默认模式：**
```bash
./deploy-secure.sh --restore
```

### 🛡️ 安全改进

| 指标 | v0.1.0 | v0.1.1 | 提升 |
|------|--------|--------|------|
| 人机确认覆盖率 | 40% | **100%** | +60% |
| 危险命令检测模式 | 5 | **20+** | +300% |
| 受保护目录 | 4 | **10+** | +150% |
| 数据脱敏 | ❌ | **✅ 30+ 模式** | 新增 |
| 一键加固 | ❌ | **✅** | 新增 |

### 📊 统计数据

| 指标 | 数值 |
|------|------|
| 总代码行数 | ~3,400（核心）+ ~700（安全工具） |
| 文档字数 | ~25,000 |
| 风险检测模式 | 100+ |
| 敏感数据检测模式 | 30+ |
| 安全配置模式 | 3种（默认、严格、加固） |

---

## 📝 Changelog / 更新日志

### Added / 新增
- Hardened security configuration (`config.hardened.json`) / 加固安全配置
- One-click deployment script (`deploy-secure.sh`) / 一键部署脚本
- Data sanitization tool (`sanitizer.sh`) / 数据脱敏工具
- Comprehensive security documentation (`SECURITY.md`) / 安全文档
- 100% human-in-the-loop mode without code changes / 零代码改动人机回环模式
- 30+ sensitive data detection patterns / 30+ 敏感数据检测模式
- Automatic audit log rotation setup / 自动审计日志轮转设置

### Improved / 改进
- Enhanced blacklist with 20+ dangerous command patterns / 增强黑名单
- Extended sensitive directory protection / 扩展敏感目录保护
- Security section in README.md / README.md 安全章节

---

## 🔗 Links / 链接

- **Repository**: https://github.com/stephenlzc/claw-gatekeeper
- **Documentation**: https://github.com/stephenlzc/claw-gatekeeper/blob/main/README.md
- **Security Guide**: https://github.com/stephenlzc/claw-gatekeeper/blob/main/SECURITY.md
- **Full Changelog**: https://github.com/stephenlzc/claw-gatekeeper/compare/v0.1.0...v0.1.1

---

**Upgrade from v0.1.0**: Simply download the new release and run `./deploy-secure.sh --apply` for enhanced security.

**从 v0.1.0 升级**: 下载新版本后运行 `./deploy-secure.sh --apply` 即可获得增强安全保护。
