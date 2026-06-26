---
name: agent-sbti
description: AI Agent 性格配置系统 - 完成 SBTI 测试，生成性格报告，选择 Agent 类型（互补/同频/微调/自定义），一键配置 Agent SOUL.md。适用：人格测试、Agent 性格配置。触发词：SBTI测试、人格测试、Agent性格。
---

# 🎭 Agent-SBTI

让 AI Agent 适配你的性格。

## 功能
1. **SBTI 测试** - 20 道题，15 维度，5 种人格
2. **配置模式** - 互补/同频/微调/自定义
3. **一键配置** - 自动备份 + 修改 SOUL.md

## 5 种人格
| 类型 | 风格 |
|------|------|
| 💀 DEAD | 坦诚直接 |
| 🔥 FUCK | 热情似火 |
| 💰 ATM | 有求必应 |
| 🐒 MALO | 温和摸鱼 |
| 💩 SHIT | 毒舌真实 |

## 4 种配置
| 模式 | 说明 |
|------|------|
| 🔄 互补 | 补足弱点 |
| 📋 同频 | 复制风格 |
| ⚖️ 微调 | 80%相似 |
| 🎛️ 自定义 | 自己选 |

## 安全
- 修改前备份到 `~/.openclaw/workspace/backup/agent-sbti/`
- 展示变更，确认后修改
- 支持「恢复原配置」

## 触发
"做 SBTI 测试" / "人格测试" / "SBTI"

## 组成
- `test.js` - 答题系统
- `agent_config.js` - 配置生成
- `apply.js` - 备份/回滚
- `skill_handler.js` - 对话处理

*让 AI 更懂你，让 Agent 更像你。* 🎭
