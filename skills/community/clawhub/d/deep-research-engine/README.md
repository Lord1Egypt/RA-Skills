# Deep Research Agent 🔬

An autonomous AI research agent that performs **deep, multi-step web research** with sub-agent delegation, full-page content analysis, and structured report generation.

## Features

- 🧠 **Autonomous planning** — breaks research questions into focused sub-tasks
- 🔍 **Deep web search** — Tavily-powered search with full-page content extraction
- 👥 **Sub-agent delegation** — parallel research units with isolated context
- 📄 **Structured reports** — generates cited, professional-quality reports
- ⚡ **Configurable** — supports multiple LLM backends and search depths

## Architecture

```
User Query
    │
    ▼
┌──────────────────────┐
│  Orchestrator Agent  │   ← Plans, delegates, synthesizes
├──────────────────────┤
│  tavily_search       │   ← Discovers URLs + fetches full content
│  write_todos         │   ← Task planning
│  read/write_file     │   ← Persistent findings
├──────────────────────┤
│  Sub-Agent: Research │   ← Parallel topic-level research
└──────────────────────┘
    │
    ▼
/final_report.md (cited output)
```

## Usage

### With This OpenClaw Skill

Just say: *"帮我深度研究一下 [主题]"* — the agent will automatically use this skill.

### Standalone (Python)

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Set API keys
export TAVILY_API_KEY="your_key"         # https://tavily.com/
export ANTHROPIC_API_KEY="your_key"      # or GOOGLE_API_KEY

# Run research
python backend/agent.py "Compare Grok 3 vs Claude Sonnet 4 for coding"
```

### CLI Options

```bash
python backend/agent.py "Your topic" \
    --model "anthropic:claude-sonnet-4-5-20250929" \
    --output "my_report.md"
```

## LLM Backends

This agent supports multiple models via LangChain:

| Model | Env Var | Identifier |
|-------|---------|------------|
| **Claude Sonnet 4.5** | `ANTHROPIC_API_KEY` | `anthropic:claude-sonnet-4-5-20250929` |
| **Claude Sonnet 4** | `ANTHROPIC_API_KEY` | `anthropic:claude-sonnet-4-20250514` |
| **GPT-4o** | `OPENAI_API_KEY` | `openai:gpt-4o` |
| **Gemini 2.0 Flash** | `GOOGLE_API_KEY` | `google:gemini-2.0-flash` |
| **Qwen (Groq)** | `GROQ_API_KEY` | `groq:qwen-2.5` |

Set via `--model` flag or `DRA_MODEL` env var.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TAVILY_API_KEY` | ✅ | Web search (free tier: 1000 queries/mo) |
| `ANTHROPIC_API_KEY` | one of | LLM backend (recommended) |
| `GOOGLE_API_KEY` | one of | LLM backend (alternative) |
| `DRA_MODEL` | ❌ | Override default model |
| `TAVILY_MAX_RESULTS` | ❌ | Results per search (default: 5) |

## Tech Stack

- **LangChain DeepAgents** — Hierarchical multi-agent research framework
- **Tavily** — AI-optimized web search
- **httpx + markdownify** — Full-page content extraction

## License

MIT
