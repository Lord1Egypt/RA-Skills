---
name: agent-security-scanner
version: 5.5.1
category: security
author: Agent Security Team
description: AI Agent 安全扫描器 - 通用恶意代码检测 + 多语言支持 + CLI 工具
license: MIT
repository: 
  primary: https://gitee.com/caidongyun/agent-security-skill-scanner (中国大陆推荐)
  mirror: https://github.com/caidongyun/agent-security-skill-scanner (海外推荐)
  note: 双仓库源，根据网络情况选择
homepage: https://gitee.com/caidongyun/agent-security-skill-scanner
bugs: https://gitee.com/caidongyun/agent-security-skill-scanner/issues
required_env_vars: []
optional_env_vars:
  - LLM_API_KEY
  - LLM_API_URL
  - FEISHU_WEBHOOK
  - ALERT_EMAIL
  - ENABLE_LLM_ANALYSIS
persistence:
  daemon: optional
  cron: optional
  network_calls: optional
---

# Agent Security Scanner v5.5.1

**通用 AI Agent 安全扫描器** - 支持多语言检测、CLI 工具、恶意代码识别

---

## 🎯 核心能力

| 能力 | 说明 | 状态 |
|------|------|------|
| **CLI 工具** | asc-scan 命令行扫描器 | ✅ v5.5 |
| **多语言检测** | Python/JavaScript/YAML/Go/Shell | ✅ |
| **183+ 检测规则** | 覆盖 10+ 攻击类型 | ✅ |
| **智能识别** | 自动识别 Skill/文件/NPM/GitHub | ✅ |
| **分层输出** | 默认/高级/JSON | ✅ |
| **白名单机制** | 降低误报率 | ✅ |

---

## 📊 性能指标

| 指标 | 值 | 说明 |
|------|-----|------|
| **检测率** | **99%+** | 基于基准测试 |
| **误报率** | **<1%** | 白名单机制优化 |
| **扫描速度** | **>100 文件/分钟** | 单文件<100ms |
| **支持语言** | **5 种** | Python/JS/YAML/Go/Shell |

---

## 🚀 快速开始

### 安装方式 1: 从 Gitee (中国大陆推荐)

```bash
# 克隆仓库
git clone https://gitee.com/caidongyun/agent-security-skill-scanner.git
cd agent-security-skill-scanner/release/v5.1.0

# 安装 CLI 工具
chmod +x asc-scan
sudo ln -sf $(pwd)/asc-scan /usr/local/bin/asc-scan

# 或使用安装脚本
./install.sh
```

### 安装方式 2: 从 GitHub (海外推荐)

```bash
# 克隆仓库
git clone https://github.com/caidongyun/agent-security-skill-scanner.git
cd agent-security-skill-scanner/release/v5.1.0

# 安装 CLI 工具
chmod +x asc-scan
sudo ln -sf $(pwd)/asc-scan /usr/local/bin/asc-scan
```

### 安装方式 3: 从 npm (待发布)

```bash
npm install -g asc-scan
```

---

## 🔧 基本使用

### 扫描 Skill

```bash
# ClawHub 技能
asc-scan agent-reach

# 本地 Skill
asc-scan ./local-skill
```

### 扫描文件

```bash
# Python 文件
asc-scan ./suspicious.py

# JavaScript 文件
asc-scan ./malicious.js

# YAML 配置
asc-scan ./deployment.yaml
```

### 详细输出

```bash
asc-scan <目标> --verbose
# 或
asc-scan <目标> --json
```

---

## 📋 环境变量说明

### 可选环境变量

| 名称 | 说明 | 必需 | 安全提示 |
|------|------|------|---------|
| `LLM_API_KEY` | LLM API 密钥 | 否 | 建议使用隔离的 API 密钥，不要使用主密钥 |
| `LLM_API_URL` | LLM API 地址 | 否 | 优先使用本地/离线模型端点 |
| `FEISHU_WEBHOOK` | 飞书告警 Webhook | 否 | 仅用于告警通知 |
| `ALERT_EMAIL` | 告警邮箱 | 否 | 仅用于邮件告警 |
| `ENABLE_LLM_ANALYSIS` | 启用 LLM 分析 | 否 | 默认 false，建议先在隔离环境测试 |

### 使用示例

```bash
# 启用 LLM 分析 (可选)
export ENABLE_LLM_ANALYSIS=true
export LLM_API_KEY=your_api_key  # 建议使用测试密钥
export LLM_API_URL=https://api.example.com/v1

# 运行扫描
asc-scan ./suspicious.py --verbose
```

**安全提示**:
- ⚠️ 不要使用生产环境的 API 密钥
- ⚠️ 优先使用本地/离线模型
- ⚠️ 在隔离环境测试后再启用

---

## ⚠️ 持久化行为声明

### 后台守护进程 (可选)

本技能提供**可选**的后台扫描守护进程：

```bash
# 启动守护进程 (可选，默认不启用)
nohup python3 lingshun_scanner_daemon.py > logs/daemon.log 2>&1 &

# 停止守护进程
pkill -f lingshun_scanner_daemon.py
```

**注意**:
- ⚠️ 守护进程会持续运行
- ⚠️ 可能发起网络调用 (LLM API/告警通知)
- ⚠️ 默认不启用，需手动启动
- ⚠️ 可通过 `kill` 命令停止

### 定时任务 (可选)

本技能提供**可选**的定时扫描任务：

```bash
# 添加 cron 任务 (可选，默认不启用)
crontab -e
# 每小时扫描一次
0 * * * * python3 /path/to/scanner.py
```

**注意**:
- ⚠️ 定时任务会定期执行
- ⚠️ 默认不启用，需手动配置
- ⚠️ 可通过 `crontab -r` 删除

### 网络调用 (可选)

本技能**可能**发起网络调用：

| 调用类型 | 目的地 | 用途 | 是否必需 |
|---------|--------|------|---------|
| LLM API | 用户配置的 LLM_API_URL | LLM 深度分析 | 否 |
| 告警通知 | 用户配置的 FEISHU_WEBHOOK | 告警通知 | 否 |
| 告警通知 | 用户配置的 ALERT_EMAIL | 邮件告警 | 否 |

**注意**:
- ⚠️ 所有网络调用都是可选的
- ⚠️ 目的地由用户配置
- ⚠️ 可在代码中审查网络调用逻辑

---

## 🏗️ 仓库源说明

### 双仓库源策略

为确保全球用户都能正常访问，本技能提供双仓库源：

| 仓库 | URL | 适用地区 | 状态 |
|------|-----|---------|------|
| **Gitee (主)** | https://gitee.com/caidongyun/agent-security-skill-scanner | 中国大陆 | ✅ 推荐 |
| **GitHub (镜像)** | https://github.com/caidongyun/agent-security-skill-scanner | 海外 | ✅ 备用 |

**选择建议**:
- 🇨🇳 中国大陆用户：优先使用 Gitee (访问速度更快)
- 🌏 海外用户：优先使用 GitHub (访问更稳定)
- 🔄 如遇网络问题：切换到另一仓库源

**验证官方仓库**:
```bash
# 验证 Gitee 仓库
git remote -v
# 应显示：https://gitee.com/caidongyun/agent-security-skill-scanner

# 验证 GitHub 仓库
git remote -v
# 应显示：https://github.com/caidongyun/agent-security-skill-scanner
```

---

## 📊 风险等级说明

| 等级 | 分数范围 | 建议 |
|------|---------|------|
| 🟢 低风险 | 0-19 分 | 可以安装/执行 |
| 🟡 中等风险 | 20-49 分 | 谨慎使用，审查代码 |
| 🔴 高风险 | 50-100 分 | 建议拒绝/删除 |

---

## ⚠️ 安全提示

### 安装前

1. **验证官方仓库**
   - 检查仓库 URL 是否匹配
   - 查看提交历史和作者
   - 验证 Release 标签

2. **审查代码**
   - 检查网络调用代码
   - 检查敏感数据处理
   - 移 除 Unicode 控制字符

3. **隔离测试**
   - 在 VM/容器中测试
   - 限制网络访问
   - 监控日志

### 使用时

1. **环境变量安全**
   - 使用隔离的 API 密钥
   - 不要使用生产密钥
   - 定期轮换密钥

2. **持久化行为**
   - 默认不启用守护进程
   - 谨慎配置定时任务
   - 定期审查运行状态

3. **网络调用**
   - 审查网络调用目的地
   - 使用防火墙限制
   - 监控网络流量

---

## 📝 更新日志

### v5.5.1 (2026-04-10)

**修复**:
- ✅ 添加环境变量声明
- ✅ 添加持久化行为声明
- ✅ 添加双仓库源声明
- ✅ 清理 Unicode 控制字符
- ✅ 统一仓库 URL

**新增**:
- ✅ asc-scan CLI 工具
- ✅ 智能目标识别
- ✅ 分层输出 (默认/高级/JSON)

### v5.5.0 (2026-04-10)

**新增**:
- ✅ 通用 CLI 扫描器
- ✅ 支持 Skill/文件/NPM/GitHub
- ✅ 183+ 检测规则

---

## 📞 反馈与支持

### 报告问题

- Gitee Issues: https://gitee.com/caidongyun/agent-security-skill-scanner/issues
- GitHub Issues: https://github.com/caidongyun/agent-security-skill-scanner/issues

### 贡献代码

欢迎提交 Pull Request！

### 安全审计

如需第三方安全审计，请联系：agent-security@example.com

---

**版本**: v5.5.1  
**更新日期**: 2026-04-10  
**许可**: MIT  
**作者**: Agent Security Team
