---
name: agent-security-skill-scanner
title: Agent Security Scanner
description: Enterprise AI Agent Security Scanner - 846 rules, three-layer detection architecture, risk tier classification. Detects prompt injection, credential theft, data exfiltration, and attack chains.
version: 6.2.0
---

# AI Agent Security Scanner v6.2.0

企业级 AI Agent 安全扫描工具，检测恶意代码、供应链攻击、凭据窃取和攻击链。

## 🎯 核心指标

| 指标 | v6.2.0 |
|------|--------|
| 规则数 | 846 |
| 检测架构 | 三层 (PatternEngine → HybridRuleEngine → LLMEngine) |
| 扫描速度 | ~385 文件/秒 |
| 风险分级 | 5 级 (CRITICAL/HIGH/MEDIUM/LOW/INFO) |

## 🔥 v6.2.0 新特性

### 风险分级体系
- **Curl 风险分级**: 白名单域名 + 敏感参数检测
- **凭据窃取检测**: 攻击链识别 (诱导→混淆→外传)
- **5 级风险体系**: CRITICAL/HIGH/MEDIUM/LOW/INFO

### 单 Skill 熔断机制
- 默认阈值: 500 文件/目录
- 防止恶意软件塞入大量文件拖慢扫描

### 规则库优化
- 去重 88 条规则 (928 → 846)
- 新增 6 条凭据攻击链规则 (CRED-CHAIN-001~006)
- 419 条 severity 统一为大写

## 💻 使用

### 命令行
```bash
# 扫描目录
python3 scanner.py /path/to/skills/

# 并发扫描 (8 worker)
python3 scanner.py /path/to/skills/ --workers 8

# 输出 JSON 报告
python3 scanner.py /path/to/skills/ --output json --output-file report.json

# 单 Skill 熔断阈值
python3 scanner.py /path/to/skills/ --skill-max-files 500
```

### npm
```bash
npm install -g @caidongyun/security-scanner
agent-scanner /path/to/skills/
```

## 📦 安装

```bash
# pip
pip install -r requirements.txt

# npm
npm install -g @caidongyun/security-scanner
```

## 📁 文件结构

```
├── scanner.py                  # 主扫描器
├── whitelist_filter.py         # 白名单过滤
├── config_detector.py          # 配置文件检测
├── context_aware_filter.py     # 上下文感知过滤
├── credential_theft_classifier.py  # 凭据窃取攻击链检测
├── curl_risk_classifier.py     # Curl 风险分级
├── risk_tier_classifier.py     # 5 级风险体系
├── security_tool_detector.py   # 安全工具识别
├── scan                        # CLI 入口
├── src/engines/                # 8 个检测引擎
├── rules/dist/all_rules.json   # 846 条规则
├── package.json                # npm 配置
├── README.md                   # 使用文档
└── RELEASE_NOTES.md            # 发布说明
```

## 🔗 链接

- **Gitee**: https://gitee.com/caidongyun/agent-security-skill-scanner
- **GitHub**: https://github.com/caidongyun/agent-security-skill-scanner
- **NPM**: @caidongyun/security-scanner@6.2.0

---

**v6.2.0** | **846 Rules** | **Three-Layer Detection** | **Risk Tier Classification** | **Attack Chain Detection**
