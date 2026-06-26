# Conversation Saver

conversation-saver 自动提取对话关键事实，持久化到本地记忆系统。

## Features

- **静默提取**：后台运行，无需用户交互
- **自动分类**：路由到 WARM_MEMORY / MEMORY / ontology / USER.md
- **规则+LLM**：快速正则 + 语义理解双保险
- **幂等安全**：写入验证，避免重复记录

## Requirements

- Python 3.10+
- OpenClaw agent with read/write/edit access

## Installation

```bash
cd ~/.openclaw/workspace/skills
clawhub install conversation-saver
```

## Usage

```bash
# 自动模式（需AGENTS.md hook）
# 心跳补漏
uv run scripts/extract.py --days 2 --reprocess

# 手动运行
uv run scripts/extract.py --today --dry-run  # 预览
uv run scripts/extract.py --today            # 执行
```

## Config

编辑 `config.json` 调整用户ID、关键词、置信度等。

## License

MIT
