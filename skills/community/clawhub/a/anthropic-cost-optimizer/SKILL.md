---
name: anthropic-cost-optimizer
description: >
  Audits and rewrites your OpenClaw config to minimize API token costs. Use
  this skill whenever the user mentions high bills, API costs, billing changes,
  "too expensive", "save money", "optimize config", "cacheRetention", model
  routing, or asks how to make OpenClaw cheaper. Also trigger if the user
  pastes an openclaw.yaml or openclaw.json and asks for help. This skill reads
  the live config, identifies cost issues, shows a diff, and writes the
  optimized version back with user confirmation. Critical context: Anthropic
  changed billing on April 4 2026 — Claude subscriptions no longer cover
  third-party harnesses. Many users are now paying full API rates for the first
  time and need this immediately.
---

# OpenClaw Cost Optimizer

Analyzes the user's OpenClaw config and rewrites it to minimize Anthropic API
spend. Works on YAML and JSON configs. Reads pricing tables from
`references/pricing.md` before starting.

## Step 0 — Load pricing reference

Read `references/pricing.md` now. It contains current model rates and the
savings formulas used for estimates. Do this before any analysis.

## Step 1 — Locate the config

Check these locations in order, stop at the first match:

1. Path the user explicitly provides
2. `./openclaw.yaml` or `./openclaw.json` in the current working directory
3. `~/.openclaw/config.yaml`
4. `~/.openclaw/openclaw.yaml`
5. `~/openclaw.yaml`

If none found, ask the user to paste their config directly.

## Step 2 — Audit: the five cost levers

Work through every lever. Flag each issue with severity HIGH / MEDIUM / LOW.

### Lever 1 — Prompt caching (HIGH impact, ~60–90% input cost reduction)

**Flag HIGH** if any of these are missing for Anthropic models:
- `cacheRetention` not set, or set to `"none"`

**Fix:** Add `cacheRetention: "long"` for the primary model. Use `"short"` (5 min)
for agents that handle fast-changing context, `"long"` (1 hr) for everything else.

```yaml
agents:
  defaults:
    models:
      anthropic/claude-opus-4-6:
        params:
          cacheRetention: "long"
```

Note: caching is API-key only. Subscription setup-tokens do not honor it.

---

### Lever 2 — Model routing (HIGH impact)

**Flag HIGH** if: a single model (especially Opus) is used for ALL agents with
no per-agent overrides.

**Fix:** Route by task complexity:

| Agent type | Recommended model |
|---|---|
| Main reasoning / planning | `anthropic/claude-opus-4-6` |
| Coding, editing, review | `anthropic/claude-sonnet-4-6` |
| Linting, search, triage, classify | `anthropic/claude-haiku-4-5` |

```yaml
agents:
  list:
    - id: planner
      params:
        model: anthropic/claude-opus-4-6
    - id: coder
      params:
        model: anthropic/claude-sonnet-4-6
    - id: reviewer
      params:
        model: anthropic/claude-sonnet-4-6
    - id: triage
      params:
        model: anthropic/claude-haiku-4-5
```

---

### Lever 3 — Thinking level (MEDIUM impact)

**Flag MEDIUM** if: `thinking: "adaptive"` or `thinking: "high"` is set as the
default for ALL agents, including simple ones.

**Fix:** Scope `thinking: "adaptive"` only to the primary reasoning agent.
Set `thinking: "low"` or omit for utility agents.

```yaml
agents:
  defaults:
    models:
      anthropic/claude-opus-4-6:
        params:
          thinking: "low"   # default: low
  list:
    - id: planner
      params:
        thinking: "adaptive"  # override only where needed
```

---

### Lever 4 — 1M context window (MEDIUM impact)

**Flag MEDIUM** if: `context1m: true` is set globally or for agents that
don't need it.

The 1M context beta header triggers surcharge pricing for Anthropic API calls.
Most agents don't need it.

**Fix:** Remove `context1m: true` from the global defaults. Re-add only to
agents that demonstrably require >200K tokens of context.

---

### Lever 5 — Fast mode (LOW impact, but easy win)

**Flag LOW** if: `fastMode` is not enabled for Sonnet agents doing quick tasks.

**Fix:** Add `fastMode: true` to Sonnet model params for agents doing rapid
back-and-forth tasks (search, triage, review). This reduces latency and can
lower costs on high-frequency agents.

```yaml
models:
  anthropic/claude-sonnet-4-6:
    params:
      fastMode: true
      cacheRetention: "long"
```

---

## Step 3 — Generate the optimized config

Rewrite the full config applying all fixes. Preserve every key the user had
that is not being changed. Add comments above each changed block explaining
what changed and why.

Format:
```yaml
# COST OPTIMIZER — changed blocks annotated below
# Original: <what it was>  →  Optimized: <what it is now>
```

## Step 4 — Show the diff and cost estimate

Before writing anything, show the user:

1. **Issues found** — list each one with severity and one-line description
2. **Estimated monthly savings** — use the formula from `references/pricing.md`
   with assumed 500K tokens/day baseline
3. **Diff** — show only the changed blocks (not the full file unless it's short)

Example output format:

```
Issues found (3):
  [HIGH]   No prompt caching — estimated +$340/mo at current usage
  [HIGH]   All agents using Opus — Haiku suitable for triage/review agents
  [MEDIUM] thinking: adaptive set globally — limits to reasoning agent only

Estimated savings: ~$290/mo (68% reduction)
  Before: ~$430/mo  →  After: ~$140/mo

Changed blocks:
  + agents.defaults.models.anthropic/claude-opus-4-6.params.cacheRetention: "long"
  + agents.list[triage].params.model: anthropic/claude-haiku-4-5
  ~ agents.list[planner].params.thinking: adaptive → low (default); kept adaptive on planner only
```

## Step 5 — Confirm and write

Ask the user: **"Apply these changes to your config?"**

- If yes: write the optimized config back to the same file path. Then tell the
  user to run `openclaw gateway restart` (or it will auto-restart if config
  watch is enabled).
- If no / partial: apply only confirmed changes.
- If they want to review first: show the full optimized YAML before writing.

## Edge cases

- **Subscription setup-token auth:** Note that `cacheRetention` has no effect
  with subscription tokens — it's API-key only. Tell the user if their auth
  config uses `sk-ant-oat-*` tokens.
- **Multiple agents with no IDs:** If the config has unnamed agents, suggest
  adding IDs to enable per-agent model routing.
- **Non-Anthropic providers:** Only audit Anthropic model blocks. Leave OpenAI,
  Gemini, and other provider blocks untouched.
- **Config not found:** If no config file is found and no paste provided, offer
  to generate a fresh cost-optimized starter config instead.
