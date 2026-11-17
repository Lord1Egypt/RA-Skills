---
name: fn2
description: Research stocks, markets, and the economy with FN2's grounded AI, and create, schedule, and manage research agents.
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - FN2_API_KEY
    primaryEnv: FN2_API_KEY
    envVars:
      - name: FN2_API_KEY
        required: true
        description: FN2 API key used to authenticate research and agent requests.
      - name: FN2_API_BASE
        required: false
        description: Optional FN2 API base URL override for self-hosted or staging environments.
    homepage: https://fn2.ai
---

# FN2 — market research & research agents

[FN2](https://fn2.ai) is an AI research platform for stocks, markets, and the
economy. It answers questions with **grounded, sourced** analysis (live prices,
earnings transcripts, SEC filings, economic data, prediction markets) and lets
you run **agents** that research on a schedule and report back.

This skill calls FN2 through a small bundled CLI at
`python3 {baseDir}/scripts/fn2.py` (Python 3 standard library only — nothing
to install). Run it with the `exec` tool.

## When to use this skill

Reach for FN2 whenever the user asks about:

- A stock or ticker — price action, "how did NVDA do this week and why", fundamentals
- Earnings, guidance, or what management said on a call
- The market or macro picture — the S&P/Nasdaq, the Fed, inflation, rates, jobs
- Comparing companies, screening, or "what's moving and why"
- Setting up **recurring research** — a daily brief, a weekly recap, an
  earnings-day monitor — that runs automatically

For one-off questions, use `research`. For anything recurring or that should keep
running on its own, create an **agent**.

## Setup (once)

The CLI authenticates with the `FN2_API_KEY` environment variable.

**If the user isn't connected to FN2 yet** (no key set), the CLI prints a sign-up
link — surface it to them as the next step. Don't try to work around a missing
key; getting one is the onboarding:

> You'll need a free FN2 account to use this. Create one and grab an API key here
> (it takes a minute): **https://fn2.ai/api-keys?ref=openclaw**
> Then run: `export FN2_API_KEY=fn2_...`

The `?ref=openclaw` link takes them straight to key creation. Once they've
exported the key, retry their request.

## How to use it

Run the bundled CLI with `exec`. Add `--json` to any command when you want
machine-readable output to parse.

### Research (the most common use)

```bash
python3 {baseDir}/scripts/fn2.py research "How did NVDA do this week, and what drove it?"
python3 {baseDir}/scripts/fn2.py research "What's the macro backdrop into the next Fed meeting?"
python3 {baseDir}/scripts/fn2.py research "Summarize Apple's latest earnings call" --model z-ai/glm-5.2
```

A research call can take 30–120 seconds because FN2 pulls live data and reads
sources. The answer comes back as Markdown.

### Agents — schedule recurring research

```bash
# Run once, right now:
python3 {baseDir}/scripts/fn2.py agents create --prompt "Deep dive on AMD vs NVDA in AI accelerators"

# Every weekday morning:
python3 {baseDir}/scripts/fn2.py agents create --name "Macro Brief" \
  --prompt "Morning macro brief: overnight moves, key data, what to watch" \
  --every weekdays --timezone America/New_York

# A specific cron schedule (Mondays at 9am):
python3 {baseDir}/scripts/fn2.py agents create --name "Weekly Tech Recap" \
  --prompt "Recap the week in big-cap tech and call out next week's catalysts" \
  --cron "0 9 * * 1" --timezone America/New_York
```

### Manage agents and read their results

```bash
python3 {baseDir}/scripts/fn2.py agents list                  # see your agents
python3 {baseDir}/scripts/fn2.py agents run <agent-id>        # trigger a run now
python3 {baseDir}/scripts/fn2.py runs list <agent-id>         # list that agent's runs
python3 {baseDir}/scripts/fn2.py runs get <agent-id> <run-id> # read a run's full answer
python3 {baseDir}/scripts/fn2.py agents pause <agent-id>       # pause / resume
python3 {baseDir}/scripts/fn2.py agents resume <agent-id>
python3 {baseDir}/scripts/fn2.py agents delete <agent-id>      # delete it and its history
```

### Account & models

```bash
python3 {baseDir}/scripts/fn2.py models # which models you can use (★ = your default)
python3 {baseDir}/scripts/fn2.py usage  # your plan and token usage
```

## Good habits

- Quote the user's question closely in `research` — FN2 does the interpreting.
- After creating a scheduled agent, confirm its `id` and schedule back to the user.
- A run started with `agents run` is asynchronous: poll `runs get` until its
  status is `completed`, then share the result text.
- A `403 Missing scope` means the user's key needs the relevant scope (`chat` for
  research, `agents` for agents, `models` for the model list) — they can edit it
  at https://fn2.ai.
- A `429` is a quota limit — show `python3 {baseDir}/scripts/fn2.py usage`.

See [`references/api.md`](references/api.md) for the full command and endpoint
reference.
