# How to Use Ghostclaw

## Installation

```bash
pip install ghostclaw
```

Make sure you have an LLM API key if you plan to use `--use-ai`:

```bash
export GHOSTCLAW_API_KEY="your_key"
```

## Basic Analysis

Analyze the current directory:

```bash
ghostclaw analyze .
```

Produce JSON output for machine consumption:

```bash
ghostclaw analyze . --json
```

## Caching

Cache results to avoid re‑analysis of unchanged code:

```bash
ghostclaw analyze .            # cache on by default
ghostclaw analyze . --no-cache  # disable cache
```

Cache directory defaults to `~/.cache/ghostclaw` but can be changed:

```bash
ghostclaw analyze . --cache-dir /tmp/my-cache
```

Cache entries expire after a configurable TTL (7 days default). Set `cache_ttl_hours` in config or via `--cache-ttl` days (note: CLI flag is in days): `ghostclaw analyze . --cache-ttl 2` (2 days).

## Parallel Scanning

Large repositories benefit from parallel file discovery:

```bash
ghostclaw analyze . --no-parallel         # disable parallelism
ghostclaw analyze . --concurrency-limit 64  # increase from default (32)
```

Configure defaults via config: `parallel_enabled`, `concurrency_limit`.

## AI Integration

Use AI to generate a narrative synthesis:

```bash
ghostclaw analyze . --use-ai
```

You can select provider and model:

```bash
ghostclaw analyze . --use-ai --ai-provider anthropic --ai-model claude-3-opus
```

With `--json`, the AI synthesis is included in the JSON payload; streaming characters appear on stderr during generation.

## Plugin Management

List available plugins (internal and external):

```bash
ghostclaw plugins list
```

Enable or disable plugins (writes to project-local config `.ghostclaw/ghostclaw.json`):

```bash
ghostclaw plugins enable pyscn
ghostclaw plugins disable ai-codeindex
```

By default, all plugins are enabled. Set `plugins_enabled` in your config file to create a whitelist.

## Reliability & Strict Mode

If you want the analysis to treat adapter errors as fatal, use `--strict`:

```bash
ghostclaw analyze . --strict
```

Without `--strict`, errors from adapters are collected and reported, but the exit code is 0.

LLM API calls are automatically retried on transient failures (configurable via `retry_attempts`, `retry_backoff_factor`, `retry_max_delay`).

## Observability & Benchmarking

Show progress phases:

```bash
ghostclaw analyze . --verbose
```

Print timing benchmark after analysis:

```bash
ghostclaw analyze . --benchmark
```

This writes a small table (seconds) to stderr. Combine with cache stats.

## PR Creation

Create a GitHub PR with the report:

```bash
ghostclaw analyze . --create-pr
```

The report is temporarily written to the repository root, committed, and then cleaned up after PR creation. The PR title and body can be customized:

```bash
ghostclaw analyze . --create-pr --pr-title "Architecture Review" --pr-body "Please review the findings."
```

## Configuration

Ghostclaw can read a global config file (`~/.config/ghostclaw/ghostclaw.json`) and a project‑local config (`.ghostclaw/ghostclaw.json`). CLI arguments take precedence.

Example config snippet:

```json
{
  "cache_enabled": true,
  "cache_compression": true,
  "cache_ttl_hours": 168,
  "parallel_enabled": true,
  "concurrency_limit": 32,
  "retry_attempts": 3,
  "plugins_enabled": ["pyscn", "ai-codeindex"]
}
```

## Summary of Important CLI Flags

| Category | Flag | Description |
|----------|------|-------------|
| Caching | `--no-cache` | Disable caching |
| | `--cache-dir PATH` | Custom cache directory |
| | `--cache-ttl DAYS` | TTL in days |
| | `--cache-stats` | Show cache statistics |
| Parallel | `--no-parallel` | Disable parallel scanning |
| | `--concurrency-limit N` | Max concurrent operations (default 32) |
| LLM | `--use-ai` | Enable AI synthesis |
| | `--ai-provider PROVIDER` | e.g., `openrouter`, `anthropic`, `openai` |
| | `--ai-model MODEL` | Model identifier |
| Reliability | `--strict` | Exit non‑zero on adapter errors |
| Observability | `--benchmark` | Print timing breakdown |
| | `--verbose` | Increase output |
| PR | `--create-pr` | Create PR on GitHub |
| | `--pr-title TITLE` | Custom PR title |
| | `--pr-body BODY` | Custom PR body |
| Output | `--json` | JSON output to stdout |

That’s it! 🎯
