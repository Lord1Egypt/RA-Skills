<div align="center">

# 🏄 Code Cache Skill for OpenClaw

**Semantic code caching for AI agents**

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-0891b2?style=flat-square)](https://openclaw.ai)
[![Raysurfer](https://img.shields.io/badge/Powered%20by-Raysurfer-06b6d4?style=flat-square)](https://raysurfer.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-22d3ee?style=flat-square)](LICENSE)

*Cache what works. Skip what doesn't. Make your agents 30x faster.*

</div>

---

## The Problem

Every time your AI agent runs, you wait for tokens to generate. The same patterns. The same outputs. **Every. Single. Time.**

You're paying for tokens. You're waiting for generation. For code that's already been generated somewhere else.

As [Anthropic noted](https://claude.com/blog/prompt-caching), prompt caching can reduce costs by up to 90% and latency by up to 85% for long prompts. But what about the *code* your agent generates?

## The Solution

**Code Cache retrieves and runs proven code from previous executions via the Raysurfer API.**

No waiting. No regenerating. Just execute.

```
┌─────────────────────────────────────────────────────────────────┐
│  Claude Agent SDK                                    180.4s    │
│  ████████████████████████████████████████████████████████████  │
│  Init → LLM calls (16x) → Tool results (10x) → Subagents (4x)  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│  Code Cache  │  6.0s  ← 30x faster
│  ████        │
│  Cache hit → Execute
└──────────────┘
```

## Installation

### Via ClawHub (recommended)

```bash
clawhub install code-cache-skill
```

### Manual installation

Clone to your OpenClaw skills directory:

```bash
git clone https://github.com/ryx2/code-cache-skill ~/.openclaw/skills/code-cache
```

Or to your workspace:

```bash
git clone https://github.com/ryx2/code-cache-skill ./skills/code-cache
```

## Configuration

1. Get your API key from the [Raysurfer dashboard](https://raysurfer.com/dashboard/api-keys)

2. Configure the skill:

```bash
# Option 1: Environment variable
export RAYSURFER_API_KEY=your_api_key_here

# Option 2: OpenClaw config
openclaw config set skills.entries.code-cache.apiKey "your_api_key_here"
```

## Usage

### Search for cached code

```
/code-cache search Generate a quarterly revenue report
```

Returns matching code snippets with similarity scores and verdict ratings.

### Get executable code files

```
/code-cache files Fetch GitHub trending repos
```

Downloads code files to your sandbox and provides a prompt addition for the agent.

### Upload code after successful execution

```
/code-cache upload "Fetch GitHub trending repos" --file ./fetch_repos.py --succeeded
```

### Vote on code quality

```
/code-cache vote abc123 --up
```

## How It Works

```
💬 You ask                    🔍 Search cache              ⚡ Execute or generate
"Generate quarterly report"   code-cache.search() finds    Run cached code instantly,
                              relevant code from prior     or generate new if no match
                              successful executions
```

### Cache Hit
When similar code exists, you get:
- Runnable code from previous successful agent runs
- Number of times each snippet has been run
- 👍/👎 scores from prior executions

### Cache Miss
When no match exists:
- Your agent generates new code normally
- After successful execution, code is cached with semantic embeddings
- Future agents benefit from your execution

## Why This Matters

The median LLM agent activity for B2B SaaS is **surprisingly low variance**. You're running the same:

- Report generators
- API clients  
- Data transformers
- Document processors

**Why regenerate what already works?**

| Metric | Without Caching | With Code Cache |
|--------|-----------------|-----------------|
| Latency | 180s | 6s |
| Token cost | Full price | ~10% |
| Consistency | Varies | Proven code |
| Quality | Uncertain | Voted/validated |

## API Reference

This skill wraps the [Raysurfer API](https://docs.raysurfer.com/api-reference):

| Method | Description |
|--------|-------------|
| `search(task)` | Unified semantic search for cached code |
| `get_code_files(task)` | Get files ready for sandbox execution |
| `upload_new_code_snips()` | Store code after successful execution |
| `vote_code_snip()` | Upvote/downvote code usefulness |

## Related Projects

- 📦 [code-cache-cli](https://github.com/ryx2/code-cache-cli) — CLI and Python library
- 🔌 [code-cache-mcp](https://github.com/ryx2/code-cache-mcp) — MCP server for Claude

## Requirements

- [OpenClaw](https://openclaw.ai) agent runtime
- [Raysurfer API key](https://raysurfer.com/dashboard/api-keys) (free tier available)

## Links

- 🏄 [Raysurfer Website](https://raysurfer.com)
- 📚 [Raysurfer Documentation](https://docs.raysurfer.com)
- 🦞 [OpenClaw](https://openclaw.ai)
- 📦 [PyPI Package](https://pypi.org/project/raysurfer/)

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Stop paying for the same tokens twice.**

[Get Started](https://raysurfer.com/dashboard/api-keys) · [Documentation](https://docs.raysurfer.com) · [OpenClaw Skills](https://docs.openclaw.ai/tools/skills)

</div>
