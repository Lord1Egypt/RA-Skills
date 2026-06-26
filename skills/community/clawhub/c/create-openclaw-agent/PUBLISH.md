# create-agent

**一键创建新的 OpenClaw Agent - 交互式向导 + 命令行模式**

---

## 快速开始

```bash
# 交互式模式（推荐）
python3 scripts/create_agent.py

# 命令行模式
python3 scripts/create_agent.py --id "dev-fe" --name "前端工程师" --role "dev-fe"

# 预览不执行
python3 scripts/create_agent.py --id "test" --name "测试" --dry-run
```

---

## 功能

- ✅ 8 个预设角色模板（dev-tl/fs/qa/ops, writer, analyst, researcher, custom）
- ✅ 自动生成身份文件（IDENTITY.md, SOUL.md, AGENTS.md, USER.md）
- ✅ 自动更新 openclaw.json（agents.list + bindings + channel accounts）
- ✅ 自动更新 TEAM.md（团队架构唯一事实来源）
- ✅ 支持 telegram/飞书 Channel 配置
- ✅ 交互式向导 + 命令行两种模式
- ✅ dry-run 安全预览

---

## 预设角色

| Role | 说明 | 默认模型 |
|------|------|----------|
| `dev-tl` | 技术负责人 + 产品设计 | `openai-codex/gpt-5.3-codex` |
| `dev-fs` | 全栈工程师 | `openai-codex/gpt-5.3-codex` |
| `dev-qa` | 测试工程师 | `openai-codex/gpt-5.3-codex` |
| `dev-ops` | 运维工程师 | `openai-codex/gpt-5.3-codex` |
| `writer` | 写作与分享助手 | `bailian/qwen3.5-plus` |
| `analyst` | 数据分析师 | `bailian/qwen3.5-plus` |
| `researcher` | 研究员 | `bailian/qwen3.5-plus` |
| `custom` | 自定义角色 | `bailian/qwen3.5-plus` |

---

## 示例

### 创建写作 Agent

```bash
python3 scripts/create_agent.py \
  --id "inkflow" \
  --name "写作与分享助手" \
  --role "writer" \
  --channel "telegram" \
  --emoji "🖋️"
```

### 创建前端工程师

```bash
python3 scripts/create_agent.py \
  --id "dev-fe" \
  --name "前端工程师" \
  --role "dev-fe" \
  --emoji "💻"
```

---

## 自动化内容

### 生成的文件

```
~/.openclaw/agents/<id>/agent/
├── IDENTITY.md
├── SOUL.md
├── AGENTS.md
├── USER.md
└── auth.json

~/.openclaw/workspace-<id>/
├── AGENTS.md
├── SOUL.md
├── USER.md
├── IDENTITY.md
└── memory/
```

### 自动配置

1. **openclaw.json** - 添加 agent + binding + channel 账号
2. **TEAM.md** - 更新团队架构

---

## 创建后步骤

```bash
# 1. 配置 Channel Token（如需要）
# 编辑 openclaw.json: channels.telegram.accounts.<id>.botToken

# 2. 重启 Gateway
openclaw gateway restart

# 3. 验证
openclaw agents list --bindings
```

---

## 基于实战经验

本 skill 基于 2026-02-28 创建 InkFlow agent 的完整流程总结，采用**单一事实来源**架构设计。

---

## 许可证

MIT License

---

**作者:** 大总管  
**版本:** 1.0.0  
**创建日期:** 2026-02-28
