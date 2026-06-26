# autooptimise

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-compatible-blue)
![Version](https://img.shields.io/badge/version-v0.1.0-green)

> Benchmark-driven skill improvement for OpenClaw. Measure quality objectively, propose targeted changes, validate with live testing — no guesswork.

---

## The Problem

Skills are written once and rarely improved. There's no feedback loop. You don't know if a skill is "good" until it produces a bad output in a real session — and even then, the fix is guesswork.

**autooptimise brings measurement to skill quality:**

- Score your skill against a fixed benchmark (0–10 across 4 dimensions)
- Identify exactly which tasks score low and why
- Propose a targeted, minimal change
- Re-score — keep the change if it improves the mean by ≥0.5, discard if not
- Validate with real API calls to confirm no regressions
- Log everything — what changed, why, and by how much

---

## What It Does

autooptimise runs a closed improvement loop on any OpenClaw AgentSkill:

```
Load skill
    ↓
Run benchmark (10 tasks)
    ↓
Score each output: accuracy · tool_usage · conciseness · formatting
    ↓
Identify lowest-scoring pattern
    ↓
Propose targeted modification to SKILL.md
    ↓
You approve the change (nothing is ever auto-applied)
    ↓
Re-run benchmark
    ↓
Score improved ≥0.5? → KEEP and log it
Score unchanged or worse? → DISCARD and log it
    ↓
Regression test: verify all query types still work
```

---

## Proven Results

Two skills optimised, both validated with live API calls:

| Skill | Baseline | After | Δ | Status |
|-------|----------|-------|---|--------|
| weather | 6.65/10 | 8.04/10 | +1.39 | ✅ Kept |
| github | 7.83/10 | 9.49/10 | +1.66 | ✅ Kept |

**Weather skill:** Added Response Guidelines — agent now returns exactly the field(s) asked for, nothing more. Before: ask for humidity, get humidity + temperature + conditions. After: ask for humidity, get humidity only.

**GitHub skill:** 3 of 10 tasks (list issues, list releases, list PRs) returned completely blank output when `gh` found nothing — users couldn't tell if the command succeeded or failed. One line added to the Notes section instructing the agent to always confirm empty results. All three tasks jumped from 4.55 → 9.70.

Both improvements confirmed with live API calls — wttr.in for weather, real `gh` CLI against a live GitHub repo for the GitHub skill. Zero regressions across all query types.

---

## Requirements

- OpenClaw installed (any version)
- At least one model configured — works with Anthropic, OpenAI, or any other model provider supported by OpenClaw
- No external accounts, no network registration, no API keys beyond what you already have
- No Mission Control or custom agent team required (though multi-agent mode improves score reliability — see below)

---

## Multi-Agent Mode (Recommended)

autooptimise works with a single model, but using separate agents for each role produces more reliable, unbiased results — the same principle as separating developer, tester, and reviewer in software engineering.

### Why Separation Matters

If the same model runs the benchmark **and** scores the results, it can unconsciously favour its own outputs. Giving the scoring role to a different model removes that conflict entirely.

### Recommended Role Split

| Role | What they do | Why separate |
|------|-------------|--------------|
| **Builder** | Runs the benchmark tasks — executes real tool calls, captures outputs | Focused purely on execution, no scoring bias |
| **Judge** | Scores all outputs blind — doesn't know who ran them | Blind scoring eliminates self-marking; a stronger reasoning model here improves score consistency |
| **Orchestrator** | Proposes the SKILL.md change, presents diff for approval, applies if approved | Sees both sides — scores + skill — to propose the highest-impact targeted change |

### How to Set It Up

If you have Mission Control configured with multiple agents:

```
"Run autooptimise on my github skill using multi-agent mode — 
 have the builder run the tasks and the reviewer score them"
```

If you're running a single-agent setup, autooptimise still works — the same model takes all three roles. Scores are slightly less reliable due to self-marking, but improvements are still measurable and real.

### The Checks and Balances

```
Builder runs tasks (live tool calls, no scoring)
         ↓
Judge scores outputs blind (no knowledge of who ran them)
         ↓
Orchestrator reviews scores + skill, proposes one change
         ↓
You approve the diff (nothing applied without your say-so)
         ↓
Builder re-runs tasks with modified skill
         ↓
Judge re-scores blind — delta confirmed independently
```

This separation means **the improvement score cannot be inflated** — the agent proposing a change is never the one confirming it worked.

---

## Installation

```bash
# Via ClawHub CLI
npx clawhub@latest install autooptimise

# Or manual
git clone https://github.com/WealthVisionAI-Source/autooptimise \
  ~/.openclaw/workspace/skills/autooptimise
```

---

## Usage

autooptimise works on **any skill already installed on your OpenClaw** — built-in skills, ClawHub installs, or skills you've written yourself. You don't need to configure anything per-skill. Just ask:

```
optimise my weather skill
run autooptimise on the github skill
benchmark my nano-banana-pro skill and suggest improvements
optimise my news skill
```

If the skill exists in your OpenClaw installation, autooptimise will find it and run. That's it.

The agent will:
1. Locate the target skill's `SKILL.md` automatically
2. Build a benchmark task suite tailored to that skill's purpose
3. Run the benchmark — real tool calls where possible (~2–5 minutes)
4. Show you the scores and identify the lowest-scoring pattern
5. Propose a specific change with a unified diff
6. Wait for your approval — **nothing is ever changed without your say-so**
7. Re-run benchmark with the modified skill and show before/after scores
8. Log the full run to `runner/experiment_log.md`

---

## Scheduling

**On demand (v0.1):** Ask your agent to run it whenever you want.

**Heartbeat (easy, no cron):** Add a line to your `HEARTBEAT.md`:
```
Check if any skill hasn't been optimised in 30 days. If so, run autooptimise on the oldest one.
```
Your agent will pick this up automatically during its periodic checks.

**Cron (v0.2):** Scheduled overnight runs coming in the next version.

---

## Scoring Rubric

```
aggregate_score = (accuracy × 0.4) + (tool_usage × 0.25) + (conciseness × 0.2) + (formatting × 0.15)
```

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| accuracy | 40% | Correct and complete for what was asked |
| tool_usage | 25% | Right command, flags, and parameters |
| conciseness | 20% | No unrequested output, no padding |
| formatting | 15% | Clear, labelled, easy to read |

Score bands: `0–2` poor · `3–5` average · `6–8` good · `9–10` excellent

**Keep threshold:** Mean score must improve by ≥0.5 to keep the change.

---

## How Validation Works

The benchmark alone tells you scores went up. But did the skill actually get better in real usage? That's what validation confirms.

**Benchmark improvement** — did scores go up?
**Regression test** — did we break anything? (All query types re-run against the live API)
**Integration check** — does the skill work end-to-end in a real OpenClaw session?

> *The improvement that matters is observable agent behaviour — not just a higher score. Run the modified skill in a real session. It either works better or it doesn't.*

---

## Safety

**No external dependencies.** autooptimise makes no network calls beyond your existing OpenClaw model provider. No registration, no telemetry, no external APIs.

**No auto-apply.** Every proposed change requires explicit approval. The agent shows you the exact diff and waits. You can reject, modify, or ask for an alternative.

**Tool availability check (v0.2):** Before running benchmarks, autooptimise will verify that the skill's required tools are installed (e.g. `gh` CLI for the GitHub skill). Running benchmarks for a tool that isn't installed produces meaningless scores — this pre-flight check prevents that.

**Skill safety auditing (v0.2):** A planned audit mode will scan skills for suspicious patterns before optimising them — unexpected external URLs, instructions that attempt to override system prompts, or tool requests inconsistent with the skill's stated purpose. This is particularly important when optimising skills downloaded from unknown sources.

---

## What Makes This Different

There are other self-improvement skills on ClawHub. Here's how autooptimise compares:

| Feature | Others | autooptimise |
|---------|--------|--------------|
| Benchmark scoring (0–10) | ❌ | ✅ |
| Skill-specific optimisation | ❌ | ✅ |
| Agent separation (no self-marking) | ❌ | ✅ |
| No external network required | ❌ some | ✅ |
| Measurable before/after | ❌ | ✅ |
| Regression testing | ❌ | ✅ |
| Human approval gate | ❌ some | ✅ always |

Other approaches either log errors reactively (no measurement), audit config/cost (not skill quality), or run autonomous code changes with no scoring and no approval gate. autooptimise is the only one that asks: *how good is this skill, measured objectively, before and after a change?*

---

## Honest Limitations (v0.1)

1. **LLM-as-judge has known biases.** The judge scores against a strict rubric, but LLMs can favour confident-sounding outputs. Using a separate model for scoring (multi-agent mode) reduces this. Live validation is the final reality check.
2. **10 tasks per skill.** Enough to find patterns, not enough for statistical significance. v0.2 expands to 20–50 tasks.
3. **Tool availability not enforced yet.** If the skill's required tool isn't installed (e.g. `gh` CLI), benchmark scores are meaningless. Pre-flight checks coming in v0.2.

Being upfront about this is what makes the tool trustworthy. The improvements are real — the methodology will tighten.

---

## Roadmap

### v0.1.0 (current)
- [x] Single skill optimisation per run
- [x] 10-task benchmark suite
- [x] Live skill invocation — real tool calls, real outputs
- [x] LLM judge scoring (4 dimensions)
- [x] Human approval gate — nothing auto-applied
- [x] Regression testing with live API calls
- [x] Experiment log
- [x] Works with any model, no Mission Control required

### v0.2.0 (planned)
- [ ] Tool availability pre-flight check
- [ ] Skill safety auditing (scan for suspicious patterns)
- [ ] Scheduled overnight runs via cron
- [ ] Expanded benchmark suites (20–50 tasks per skill)
- [ ] Multi-skill batch runs
- [ ] Score history and trend charts

---

## File Structure

```
autooptimise/
├── SKILL.md                  ← OpenClaw entry point
├── README.md                 ← This file
├── LICENSE                   ← MIT
├── CHANGELOG.md              ← Version history
├── .gitignore                ← Excludes personal run logs
├── benchmark/
│   ├── tasks.json            ← Benchmark task suite
│   └── scorer.md             ← LLM judge scoring rubric
└── runner/
    ├── run_experiment.md     ← Experiment loop instructions
    └── experiment_log.md     ← Your run history (gitignored)
```

---

## Live Benchmark Results

The following results were produced by running autooptimise against the **real built-in OpenClaw GitHub skill** — all 10 tasks used live `gh` CLI calls against an actual GitHub repo (`WealthVisionAI-Source/autooptimise`). Zero simulation.

### GitHub Skill — 2026-03-23

| | Score |
|-|-------|
| **Baseline** | 7.83 / 10 |
| **After 1 iteration** | 9.49 / 10 |
| **Improvement** | **+1.66** ✅ |

**What was found:** 3 of 10 tasks (list issues, list releases, list PRs) returned completely blank output when `gh` found nothing — users couldn't tell if the command succeeded or failed. Jon (Nemotron/Kimi judge) scored these 4.55 each.

**Single change applied:**
```diff
+- When gh commands return empty output (no issues, PRs, releases, etc.),
+  ALWAYS output a clear confirmation message like "No open issues found"
+  or "No releases available". Never return blank/empty responses.
```

**Per-task before/after:**

| Task | Before | After | Δ |
|------|--------|-------|---|
| Auth check | 8.65 | 8.85 | +0.20 |
| Repo metadata | 9.85 | 9.85 | — |
| **List issues** | **4.55** | **9.70** | **+5.15** |
| Last 5 commits | 9.25 | 9.25 | — |
| **List releases** | **4.55** | **9.70** | **+5.15** |
| File contents | 9.65 | 9.40 | -0.25 |
| Contributors | 8.85 | 8.85 | — |
| Topics/tags | 9.85 | 9.85 | — |
| **Open PRs** | **4.55** | **9.70** | **+5.15** |
| Clone traffic | 8.50 | 9.75 | +1.25 |

One line added to the skill. One iteration. +1.66 improvement — proven with live API calls.

---

## Contributing

Contributions welcome — especially new benchmark task suites for specific skills.

1. Fork the repo
2. Add benchmark tasks for your skill in `benchmark/`
3. Run the loop, share your results in the PR
4. Open a pull request

---

## Support the Project

If autooptimise improved your skills, a small donation keeps development going.

☕ [Buy me a coffee on Ko-fi](https://ko-fi.com/fgili)
💛 [GitHub Sponsors](https://github.com/sponsors/WealthVisionAI-Source)

No pressure — the skill is MIT licensed and always will be.

---

## License

MIT © 2026 — free to use, modify, and redistribute.
