# adaptive-review

**Claude Code skill that routes code review to the cheapest model that can handle the job.**

Stop burning opus tokens on 3-line typo fixes. Stop sending 500-line refactors to haiku.

## The idea

Inspired by [Think Anywhere](https://arxiv.org/abs/2603.29957) — spend compute where uncertainty is highest. Not every token deserves the same amount of thinking, and not every diff deserves the same reviewer.

```
git diff → signal collection → route to appropriate model
               │
               ├─ trivial (<50 lines, 1 file, no risk) → haiku  (~95% cheaper)
               ├─ standard (moderate scope)             → sonnet (~80% cheaper)
               └─ complex (cross-module, security, big) → opus   (full power)
```

**Signals are free** — just `git diff --numstat` and a grep for security keywords. No LLM calls to decide which LLM to call.

## How it saves money

| Review depth | Model | Relative cost | When |
|-------------|-------|---------------|------|
| fast | haiku | ~5% of opus | typos, formatting, single-file fixes |
| medium | sonnet | ~20% of opus | standard features, bug fixes |
| deep | opus | 100% (baseline) | architecture, security, cross-module |

Real-world estimate: if 60% of your reviews are fast, 30% medium, 10% deep, you save **~85% on review costs** compared to always using opus.

## Install

### ClawHub (recommended)

```bash
clawhub install adaptive-review
```

### Manual

```bash
# Option 1: Direct copy
mkdir -p ~/.claude/skills/adaptive-review
cp SKILL.md ~/.claude/skills/adaptive-review/

# Option 2: Clone
git clone https://github.com/2233admin/adaptive-review.git ~/.claude/skills/adaptive-review
```

### Verify

In Claude Code, type `/adaptive-review` — it should appear in skill suggestions.

## Usage

```
/adaptive-review          # auto-detect depth from current diff
/adaptive-review --fast   # force fast (haiku) review
/adaptive-review --deep   # force deep (opus) review
```

## How it works

1. **Signal collection** — runs `git diff --numstat` to get lines/files/dirs changed, then greps code files (not docs) for security-sensitive patterns
2. **Routing** — maps signals to review depth via simple thresholds (no ML, no API calls)
3. **Dispatch** — spawns a code-review agent with the appropriate model
4. **Report** — shows what depth was chosen and why, so you can override if needed

### Routing thresholds

| Signal | Fast | Medium | Deep |
|--------|------|--------|------|
| lines_changed | < 50 | < 200 | >= 200 |
| files_changed | <= 1 | any | any |
| dirs_changed | any | <= 1 | >= 2 |
| risk_hits* | 0 | <= 2 | > 2 |

*risk_hits = grep matches for security/concurrency keywords (`auth`, `token`, `password`, `mutex`, `sql`, etc.) in **code files only** (excludes .md/.json/.yaml to avoid false positives from documentation).

## Customization

Edit the thresholds in `SKILL.md` to match your codebase. For example:
- Monorepo with many small packages? Raise `dirs_changed` threshold
- Security-critical project? Lower `risk_hits` threshold to 0 for deep review
- Budget-constrained? Raise line thresholds to route more to haiku

## Local LLM Version (OpenClaw Edition)

Don't have a Claude API key? Use `SKILL-openclaw.md` instead — same routing logic, but targets any OpenAI-compatible local endpoint (Ollama, vLLM, SGLang, LiteLLM, etc.).

```
fast   → qwen2.5:3b (or any <7B)     — free, runs on CPU
medium → qwen2.5-coder:14b (or 7-30B) — free, needs GPU
deep   → 70B+ or cloud proxy          — best available
```

Zero cloud cost. Full privacy. Works offline. See `SKILL-openclaw.md` for setup.

## Philosophy

This is the **Think Anywhere** pattern applied to dev tooling:

> Not all code changes are equally uncertain. Route expensive compute to where it matters — complex, cross-module, security-sensitive changes — and let cheap compute handle the rest.

The same principle applies to:
- **Memory retrieval** — simple lookups vs. graph traversal
- **Agent dispatch** — choosing which model runs each task
- **Test execution** — fast smoke tests vs. full integration suites

## License

MIT
