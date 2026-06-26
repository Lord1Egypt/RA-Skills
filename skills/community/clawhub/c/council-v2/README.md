# Council v2 — Multi-Model Review System for OpenClaw

A hardened, multi-model council review skill for [OpenClaw](https://github.com/openclaw/openclaw).

Spawns 3-5 independent AI reviewers across different providers, collects structured JSON verdicts, and applies **mechanical synthesis** — the vote count is the verdict, not the orchestrator's opinion.

## Features

- **Two tiers:** Standard (3 reviewers) and Full (5 reviewers)
- **5 providers, 5 training biases:** Anthropic, OpenAI, xAI, DeepSeek, Google
- **Mechanical synthesis:** Majority vote decides. Critical findings auto-block. Synthesizer cannot override.
- **Anti-consensus check:** Unanimous votes are flagged — agreement is hypothesis, not proof.
- **Minority reports preserved:** Strongest dissent is always surfaced.
- **Monthly retro:** Track past decisions against outcomes for continuous calibration.

## Install

```bash
clawhub install council-v2
```

Or manually:
```bash
git clone https://github.com/zurbrick/council-v2.git ~/.openclaw/workspace/skills/council-v2
```

## Quick Start

```bash
bash scripts/council.sh review code src/auth.py
bash scripts/council.sh review plan proposal.md --tier full
bash scripts/council.sh review architecture design.md --tier full
bash scripts/council.sh review decision options.md --options "SQLite,Postgres,Cloud SQL"
```

For the full workflow, review types, synthesis rules, and operational details, see `SKILL.md`.

## Model Access

The council's strength comes from **model diversity** — different providers catch different blind spots. You have two options:

### Option A: OpenRouter (recommended for most users)
One API key, all 5 models. Sign up at [openrouter.ai](https://openrouter.ai).

```json5
// openclaw.json — models.providers
"openrouter": {
 "baseUrl": "https://openrouter.ai/api/v1",
 "apiKey": "${OPENROUTER_API_KEY}",
 "api": "openai-completions"
}
```

Then reference models as `openrouter/anthropic/claude-opus-4`, `openrouter/openai/gpt-5.4`, `openrouter/x-ai/grok-4`, `openrouter/deepseek/deepseek-r1`, `openrouter/google/gemini-3.1-pro`.

### Option B: Direct provider subscriptions
If you have separate subscriptions (Anthropic, OpenAI, xAI, etc.), configure each provider individually. See [OpenClaw model docs](https://docs.openclaw.ai/concepts/models).

> **Tip:** The specific models matter less than the diversity. What you want is different providers with different training data and different biases reviewing the same decision. Swap in whatever top-tier models you have access to.

## Council Tiers

### Standard (3 reviewers)
| Role | Default Model | Provider |
|------|--------------|----------|
| Architecture Synthesizer | Opus | Anthropic |
| Adversarial Critic | GPT-5.4 | OpenAI |
| Security & Risk | Grok 4 | xAI |

### Full (5 reviewers)
| Role | Default Model | Provider |
|------|--------------|----------|
| Architecture Synthesizer | Opus | Anthropic |
| Adversarial Critic | GPT-5.4 | OpenAI |
| Security & Risk | Grok 4 | xAI |
| First Principles | DeepSeek R1 | DeepSeek |
| Structural Verifier | Gemini 3.1 Pro | Google |

## Repository Contents

| File | Purpose |
|------|---------|
| `SKILL.md` | Operational skill — workflow, when to use, interpreting results |
| `references/review-types.md` | Review type definitions and tier recommendations |
| `references/role-prompts.md` | Reviewer role prompts and shared output instructions |
| `references/schema.md` | JSON schemas for reviewer and synthesis output |
| `references/synthesis-rules.md` | Mechanical synthesis protocol and edge cases |
| `scripts/council.sh` | Orchestration script |
| `scripts/synthesize.py` | Mechanical synthesis engine |
| `scripts/retro.sh` | Monthly retrospective template generator |

## Origin

Built by [Don Zurbrick](https://github.com/zurbrick) — battle-tested across plugin evaluations, security audits, architecture reviews, and one memorable session where the council reviewed itself and called out its own biases.

## License

MIT
