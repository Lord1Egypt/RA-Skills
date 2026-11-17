# Fork & Skill Scanner — TinkerClaw

> One of dozens of skills and plugins in **[TinkerClaw](https://github.com/globalcaos/tinkerclaw)** — a self-improving OpenClaw fork that's been running 24/7 for months.

A thousand forks of the same repo. Which one quietly fixed the bug you've been chasing?

Reading them by hand is a weekend you'll never get back — and the good change is buried on page forty.

There's a faster way to find the one fork, and the one skill, that actually matter.

This is your scout. Every run it triages a thousand GitHub forks, throws out the dead and the duplicate ones, and hands the survivors to a fan of sub-agents that read them in parallel — so you get back the handful with real changes instead of a wall of noise. Twice a week, on a Monday and Thursday cron, it also scores the top skills on ClawHub, so you see what's trending before everyone else does. You wake up to a short report of what's worth your attention, not a tab graveyard.

**Part of [TinkerClaw](https://github.com/globalcaos/tinkerclaw)** — real-time token tracking, self-improving crons, persistent cognitive memory. This is one piece of that stack; the repo has dozens more.

👉 **https://github.com/globalcaos/tinkerclaw**

_Clone it. Fork it. Break it. Make it yours._

## Setup

This is a written workflow, not a program. To use it, implement the phases below
in your own agent: scan the forks of a repository you care about, and review the
top skills on a registry. Automate the runs with cron once you have something that
works.

## What's in this package

Two documents and an empty directory. There is no code here:

- `README.md` — this file: the workflow, and what it does and does not do.
- `SKILL.md` — the same workflow stated for an agent, including the plain warning
  that there is nothing here to execute.
- `data/` — an empty directory held open by a `.gitkeep`, a place for *you* to put
  scan output. Nothing in this package writes to it, or to anywhere else.

## Key Phases

### Fork Scanner

1. **Bash Pre-Filter:** Triage 1,000 forks, discard non-active.
2. **Sub-Agent Fan-Out:** Distribute candidate analysis for parallel processing.
3. **Main Agent Assembly:** Finalize report and insights.
4. **Scheduled Runs:** Mon/Thu.

### Skill Scanner

1. **Evaluate 10 Skills:** Score by functionality, relevance, and maintenance.
2. **In-Depth Author Scan:** Check top author's other skills.
3. **Compile Insights:** Lay practical improvement steps.

## Keeping your interests current

The "interests" this workflow tracks are **your** list of what to watch — the repos,
authors and topics you care about — kept in a file you own and edit. Refining that
list between runs is the point of running it repeatedly.

Stating it plainly, because "continuous improvement" inside an agent skill reads the
wrong way otherwise: **this skill does not modify itself.** It has no code, no
installer, no update step, and no write path to its own files or to your agent's
configuration. The only thing that changes between runs is the note *you* keep about
what you want scanned next.

## What it touches

Read-only, and only once you implement it: public GitHub repository data and public
registry listings. No credentials are requested or stored. Nothing is written outside
the output directory you choose. There is no write access to GitHub, to any registry,
or to any skill — including this one.
