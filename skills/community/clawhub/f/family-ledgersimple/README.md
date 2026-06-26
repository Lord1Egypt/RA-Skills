# family-record

家庭账本 —— 一个基于 [Agent Skills](https://agentskills.io) 标准的智能家庭支出记录工具。

用自然语言记账，支持 [Claude Code](https://claude.ai/code)、[OpenClaw](https://openclaw.ai)、[Hermes Agent](https://hermes-agent.nousresearch.com) 等多种 AI 助手。

## 亮点：Agent Skill

本项目的核心是一个符合 [Agent Skills](https://agentskills.io/specification) 标准的 Skill，让你可以通过自然语言与账本交互。

### 安装

将 skill 目录复制到你的 AI 助手的 skills 目录即可：

```bash
# Claude Code
cp -r skills/family-ledger ~/.claude/commands/

# OpenClaw / Hermes Agent（使用 agentskills.io 标准）
cp -r skills/family-ledger ~/.agentskills/
```

### 使用方式

在支持 Agent Skills 的 AI 助手中直接用自然语言交互：

```
# Claude Code
/family-ledger 爸爸支出100买菜

# OpenClaw / Hermes Agent
family-ledger 妈妈花了200买衣服
```

### Skill 支持的操作

| 意图 | 示例输入 |
|------|---------|
| 记录支出 | `爸爸支出100买菜`、`妈妈花了200买衣服` |
| 查询记录 | `查看最近记录`、`爸爸本月支出` |
| 月度汇总 | `这个月花了多少`、`2026-05 汇总` |
| 年度汇总 | `2026年汇总`、`年度统计` |
| 删除记录 | `删除第3条` |
| 查看角色 | `有哪些角色`、`角色列表` |

Skill 会自动识别意图、解析参数，调用底层 CLI 工具并返回结果。

## CLI 直接使用

也可以不依赖 AI 助手，直接通过命令行操作：

```bash
# 记录
python3 ledger.py add --role 爸爸 --amount 100 --note "买菜"

# 查询
python3 ledger.py list --role 妈妈 --month 2026-05

# 汇总
python3 ledger.py summary --year 2026

# 删除
python3 ledger.py delete --id 3

# 角色列表
python3 ledger.py roles
```

## 环境要求

- Python 3.6+
- SQLite3（Python 内置）
- 任一支持 Agent Skills 的 AI 助手（可选）

## 数据存储

数据保存在同目录下的 `ledger.db`（SQLite 数据库），无需配置，开箱即用。

## 项目结构

```
record-family/
├── ledger.py                        # CLI 主程序
├── skills/
│   └── family-ledger/
│       └── SKILL.md                 # Agent Skills 标准格式
├── .claude/
│   └── commands/
│       └── family-ledger.md         # Claude Code 格式
├── ledger.db                        # 数据库文件（自动生成，已 gitignore）
└── README.md
```

## 兼容性

本项目的 Skill 遵循 [Agent Skills 开放标准](https://agentskills.io/specification)，兼容以下 AI 助手：

| AI 助手 | Skill 格式 | 安装位置 |
|---------|-----------|---------|
| [Claude Code](https://claude.ai/code) | `.claude/commands/*.md` | `~/.claude/commands/` |
| [OpenClaw](https://openclaw.ai) | `SKILL.md` | `~/.agentskills/` |
| [Hermes Agent](https://hermes-agent.nousresearch.com) | `SKILL.md` | `~/.agentskills/` |
| [Codex](https://openai.com/codex) | `SKILL.md` | `~/.agentskills/` |
| [Gemini CLI](https://ai.google.dev/gemini-api/docs) | `SKILL.md` | `~/.agentskills/` |

## License

MIT
