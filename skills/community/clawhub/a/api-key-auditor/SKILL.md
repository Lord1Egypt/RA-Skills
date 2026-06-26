---
name: api-key-auditor
description: 扫描 ~/.openclaw/workspace/skills 目录下所有文件中的硬编码 API Key、Token、Secret，检查是否已集成到 openclaw.json env.vars，并可自动将未集成的凭证迁移进去。Use when user asks to audit/check/scan for hardcoded API keys or tokens in skills, or wants to migrate credentials to openclaw.json. Triggers on phrases like "检查API Key暴露", "审计凭证", "扫描硬编码密钥", "api key 集成", "check for hardcoded keys".
---

# API Key 审计器

扫描 skills 目录下的硬编码凭证，并输出集成情况报告。

## 运行方式

```bash
# 仅审计（只读，不修改任何文件）
python3 ~/.openclaw/workspace/skills/api-key-auditor/scripts/audit.py

# 自动迁移：将未集成的 key 写入 openclaw.json
python3 ~/.openclaw/workspace/skills/api-key-auditor/scripts/audit.py --fix
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--skills-dir` | `~/.openclaw/workspace/skills` | 扫描目录 |
| `--openclaw-json` | `~/.openclaw/openclaw.json` | 目标配置文件 |
| `--fix` | 否 | 自动写入未集成的 key 到 env.vars |

## 报告输出含义

| 状态标记 | 含义 |
|----------|------|
| ✅ 已集成到 openclaw.json | 凭证已注册为环境变量，安全 |
| 🔧 mcporter 管理（无需迁移） | 该 key 在 `~/.mcporter/mcporter.json` 中，由 mcporter 统一管理 MCP server 连接，不需要抽取 |
| ⚠️ 未集成 | 凭证硬编码在文件中，建议迁移 |

## 迁移工作流

1. 运行审计，查看 ⚠️ 未集成项
2. 运行 `--fix`，脚本自动将 key 写入 `openclaw.json` env.vars，并给出需要手动替换的文件位置
3. 在对应文件中将硬编码值替换为环境变量引用：
   - Python：`os.environ.get('VAR_NAME')`
   - Shell：`$VAR_NAME` 或 `${VAR_NAME}`
4. 重启 OpenClaw 使环境变量生效（`openclaw gateway restart`）
5. 再次运行审计确认 ✅

## 设计说明

- **mcporter key 不抽取**：`~/.mcporter/mcporter.json` 里的 MCP server URL 中的 `?key=` 参数，已由 mcporter 统一管理，不属于需要抽取的硬编码凭证
- **占位符自动过滤**：`your-api-key-here`、`REPLACE_ME` 等示例值不会误报
- **只读模式安全**：不加 `--fix` 时，脚本不修改任何文件
