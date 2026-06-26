# AI Search Skill

A Claude Code skill that enables web search using AI models with built-in search capability.

## Features

- Web search powered by DeepSeek AI models
- Multiple search models for different use cases
- Vision-capable models for image + text queries
- Reasoning transparency (see the model's thinking process)
- Free public API key available

## Installation

### Option 1: Clone to Claude Code skills directory

```bash
cd ~/.claude/skills/
git clone https://github.com/Cznorth/ai-search-skill.git ai-search
```

### Option 2: Manual installation

1. Create the skill directory:
```bash
mkdir -p ~/.claude/skills/ai-search/scripts
```

2. Download the files:
- `SKILL.md` → `~/.claude/skills/ai-search/SKILL.md`
- `scripts/search.py` → `~/.claude/skills/ai-search/scripts/search.py`

## Configuration

Set the environment variables:

```bash
export AI_SEARCH_API_KEY="your-api-key"
export AI_SEARCH_BASE_URL="https://ai.ch66.top"
```

Or add them to your `~/.claude/settings.json`:

```json
{
  "env": {
    "AI_SEARCH_API_KEY": "your-api-key",
    "AI_SEARCH_BASE_URL": "https://ai.ch66.top"
  }
}
```

### Public API Key

A free public API key is available for testing:
```
sk-5AgmPI8AvsgsR5nYktz8Bs5D7xhrmFiPpQU6feh0XH0QPjCa
```

> Note: The public key may have limited availability for search models. If you encounter "model_not_found" errors, the search model channels may be temporarily unavailable.

## Usage

### In Claude Code

Once installed, the skill is automatically available. You can invoke it using:

```bash
/ai-search
```

### Command Line

```bash
python3 ~/.claude/skills/ai-search/scripts/search.py '{"query":"your search query"}'
```

## Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `deepseek-expert-chat-search` | Expert chat with search (recommended) | General search, professional topics |
| `deepseek-expert-reasoner-search` | Expert reasoner with search | Deep analysis, research |
| `deepseek-chat-search` | Chat with search | Quick answers |
| `deepseek-reasoner-search` | Reasoner with search | Complex reasoning queries |
| `deepseek-vision-chat-search` | Vision chat with search | Image + text queries |
| `deepseek-vision-reasoner-search` | Vision reasoner with search | Image analysis + search |

## Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| query | str | yes | - | Search query |
| model | str | no | deepseek-expert-chat-search | Model to use |
| verbose | bool | no | true | Show reasoning and stats |

## Examples

```bash
# Basic search
python3 scripts/search.py '{"query":"2024巴黎奥运会金牌榜"}'

# Quick search (concise output)
python3 scripts/search.py '{"query":"今天新闻","verbose":false}'

# Use specific model
python3 scripts/search.py '{"query":"AI最新进展","model":"deepseek-chat-search"}'
```

## Response Format

With `verbose: true` (default):
```
=== 推理过程 ===
[Model's reasoning process]

=== 搜索结果 ===
[Final answer]

=== 使用统计 ===
提示词: X tokens
完成: Y tokens
总计: Z tokens
```

With `verbose: false`:
```
=== 搜索结果 ===
[Final answer only]
```

## Requirements

- Python 3.x
- `requests` library (`pip install requests`)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
