---
name: expertpack-eval
description: "Measure ExpertPack EK (Esoteric Knowledge) ratio and run automated quality evals. Use when: (1) Measuring what percentage of a pack's content frontier LLMs cannot produce on their own, (2) Running automated eval sets against a pack-powered agent with LLM-as-judge scoring. Requires OpenRouter API key (auto-resolved from OpenClaw auth or OPENROUTER_API_KEY env var). Companion to the main expertpack skill. Triggers on: 'EK ratio', 'measure EK', 'blind probe', 'eval expertpack', 'pack quality eval', 'run eval', 'esoteric knowledge ratio'. Note: packs are Obsidian-compatible — eval results (ek_score) can be added to file frontmatter and queried in Obsidian via Dataview."
metadata:
  openclaw:
    homepage: https://expertpack.ai
    requires:
      bins:
        - python3
---

# ExpertPack Eval

Measure and evaluate ExpertPack quality. Companion to the core [expertpack](https://clawhub.ai/skills/expertpack) skill.

**Note:** This skill makes external API calls to OpenRouter for blind probing and LLM-as-judge scoring. Requires an API key.

## 1. Measure EK Ratio

Blind-probe frontier models to measure what percentage of a pack's propositions they cannot answer without the pack loaded:

```bash
python3 {skill_dir}/scripts/eval-ek.py <pack-path> [--models model1,model2] [--sample N] [--output FILE]
```

- **Default models:** GPT-4.1-mini, Claude Sonnet 4.6, Gemini 2.0 Flash (via OpenRouter)
- **API key:** Auto-resolves from OpenClaw auth profiles or `OPENROUTER_API_KEY` env var
- **Judge model:** Claude Sonnet (GPT-4.1-mini is unreliable as judge — defaults to "partial")
- **Output:** YAML with per-proposition scores and aggregate ratio

**Interpretation:**

| EK Ratio | Meaning |
|----------|---------|
| 0.80+ | Exceptional — almost entirely esoteric |
| 0.60–0.79 | Strong — majority esoteric |
| 0.40–0.59 | Mixed — significant GK padding |
| 0.20–0.39 | Weak — most content already in weights |
| < 0.20 | Minimal value-add |

Add measured ratio to `manifest.yaml`:

```yaml
ek_ratio:
  value: 0.72
  measured: "2026-03-12"
  models: ["gpt-4.1-mini", "claude-sonnet-4-6", "gemini-2.0-flash"]
  propositions_tested: 142
```

## 2. Run Quality Eval

Automated eval against a pack-powered agent endpoint:

```bash
python3 {skill_dir}/scripts/run-eval.py \
  --questions <eval-set.yaml> \
  --endpoint <ws://host:port/path> \
  --output <results.yaml> \
  --label "baseline"
```

- Build eval set: 30+ questions (basic, intermediate, advanced, out-of-scope)
- Fix one dimension at a time: structure → agent training → model
- Re-run after each change to verify improvement

**Learn more:** [expertpack.ai](https://expertpack.ai) · [GitHub](https://github.com/brianhearn/ExpertPack)
