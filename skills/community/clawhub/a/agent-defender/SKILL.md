---
name: agent-defender
description: Agent Defender - AI智能体安全防护平台。静态扫描+运行时防护+DLP脱敏。触发：(1)扫描Skill (2)启动防护 (3)DLP检测 (4)安全审计
---

# Agent Defender

AI智能体安全防护平台 - 静态扫描 + 运行时防护 + DLP脱敏

## 功能

| 模块 | 功能 |
|------|------|
| 静态扫描 | YARA规则 + AST分析 + 权限检测 |
| 运行时防护 | 系统监控 + 行为拦截 |
| DLP | 敏感数据识别 + 脱敏 + 阻断 |

## 使用

```bash
# 扫描Skill
python3 ~/.openclaw/workspace/skills/agent-defender/scanner/scan.py <skill_path>

# 运行时防护
python3 ~/.openclaw/workspace/skills/agent-defender/runtime/monitor.py

# DLP检测
python3 ~/.openclaw/workspace/skills/agent-defender/dlp/check.py <data>

# 完整扫描
python3 ~/.openclaw/workspace/skills/agent-defender/defender.py scan <path>
```

## 配置

编辑 `config.json` 配置规则阈值、敏感数据类型等。

详细说明见各模块目录。
