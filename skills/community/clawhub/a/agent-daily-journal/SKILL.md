---
name: agent-daily-journal
description: Write a daily journal from the agent's own activity.
version: 0.1.1
author: alexhuiyi
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [journal, diary, daily, memory, digest, activity, local-first, cron]
---

# Agent Daily Journal Skill

Writes a daily journal from what the agent actually did. A zero-token collector turns Hermes'
`state.db` plus workspace mtimes into a compact per-day digest; the agent then writes one short
first-person entry per digest block. A linter proves the entry covers every event before it lands.

Two rules carry the whole design:

- **The digest is material, the writer owns the voice.** No prose templates in the collector.
- **Coverage is checked, not trusted.** A rich digest easily produces a thin entry that reads fine.
  `scripts/journal_lint.py` compares the entry against the digest's `###` headings and fails on a
  missing event.

Everything runs locally. The only tokens spent are the writer's.

## When to Use

- A recurring journal/diary of the agent's own work, cron-driven or manual.
- Backfilling entries for past days, or re-voicing existing ones.
- Do not use for: work logs or commit summaries (the entry is deliberately not a report), or for
  anything the user wants in structured form — this produces prose.

## Prerequisites

- Hermes with `state.db` at `$HERMES_HOME/state.db` (`HERMES_HOME` defaults to
  `%LOCALAPPDATA%/hermes` on Windows, `~/.hermes` elsewhere). Override with `--state-db`.
- Python 3.10+ (stdlib only for both scripts).
- Optional, for cheaper and smarter digests: a local [Ollama](https://ollama.com) with
  `qwen3-embedding:0.6b` (prompt dedupe) and `qwen3:1.7b` (per-session compression). Both are
  detected at runtime; without them the collector falls back to character-overlap dedupe and raw
  prompts. Set `JOURNAL_LOCAL=off` to skip the probe entirely.
- The writer needs a journal file with a header; nothing else. Example:
  `memory/journal/journal.md` starting with `# 日记` and two `>` lines.

## How to Run

Collect what is owed (one digest per unmarked 04:00→04:00 window):

```bash
python scripts/journal_collect.py --config config/journal.json
```

Machine-readable, and forced to one window (this is how the tests and the linter get input):

```bash
python scripts/journal_collect.py --config config/journal.json --only 2026-10-25 --json
```

Write the entry with `write_file`/`patch` (append only), then lint it:

```bash
python scripts/journal_lint.py --digest digest.md --journal memory/journal/journal.md
```

Exit code 1 means an event is missing, the marker is absent, or the entry is over the ceiling.
`--strict` additionally fails on imagery, abstract wrap-ups and near-verbatim reuse.

## Procedure

1. **Collect.** Run the collector. It prints either `Nothing owed ...` (stop, report that one line)
   or a digest with a `## Window <date>` block per owed window and one `### <session>` block per
   session. Completion criterion: you know the `###` count per window.
2. **Write.** For each window, oldest first: read the style file, then write one entry that names
   **every** `###` block in one inventory clause, spends the rest on feeling, and ends with
   `<!-- window:YYYY-MM-DD -->`. Append, never rewrite. Completion criterion: one new entry per
   window, each with a marker.
3. **Lint.** Run `scripts/journal_lint.py --journal <journal>` against the digest markdown you
   collected. Completion criterion: exit 0 and `coverage N/N` equals the digest's `###` count.
4. **Report.** One line per window: date, character count, coverage.

Wire it to a schedule with `cronjob_manage(action='create', ...)`: a `file`-toolset job whose
`script` is the collector and whose prompt is the writer contract in
`references/writer-and-prompt.md`. The 04:00 tick plus a catch-up run is in
`references/deployment.md`.

## Quick Reference

| Task | Command |
|---|---|
| What is owed? | `python scripts/journal_collect.py --config config/journal.json` |
| One window as JSON | `... --only 2026-10-25 --json` |
| Lint the newest entry | `python scripts/journal_lint.py --digest d.md --journal journal.md` |
| Lint, strict | `... --strict` |
| Skip embeddings | `python scripts/journal_lint.py ... --no-semantic` |
| Tests | `python -m unittest discover -s tests` |
| Publish gate | `python scripts/check_package.py` |

## Pitfalls

- **"Summarize what happened in one sentence" destroys coverage.** Measured on a 4-session day: a
  prompt saying *"one sentence about what was done"* produced **0 of 4** events named; the same
  digest with an explicit per-`###` coverage rule produced 4 of 4. If entries feel thin, fix the
  prompt's structure, not the character ceiling — entries usually sit far below it.
- **Examples get cloned.** A sample sentence in the prompt or style file reappears near-verbatim in
  later entries for weeks and homogenises the journal. Encode shape as fill-in slots and list
  banned tones instead.
- **Style duplicated in two places always drifts.** The style file is the single authority on
  voice; the cron prompt carries flow and coverage only.
- **The ladder is coverage > feeling > length.** Written down, or the writer trades events for
  brevity every time. Ceilings: 1–2 events 300 chars, 3–5 events 420, and no floor — a quiet day is
  one line.
- **`invented_time` warnings are advisory**, not failures: they cannot know whether the digest
  clock earns a "傍晚". Everything else in `--strict` is trustworthy.
- **`--only` ignores the coverage ledger on purpose.** Use it for tests and re-linting, never in
  the cron prompt, or every run rewrites windows that are already marked.
- **A second writer breaks `write_file`.** If a cron job appends to the journal, the file changes
  under you; append with `patch` on the last marker, or write a temp file and move it into place.

## Verification

```bash
python -m unittest discover -s tests          # 28 tests, no network, no real state.db
python scripts/check_package.py               # publish gate: frontmatter, links, no local paths
python scripts/journal_collect.py --config config/journal.json --only 2026-10-25 --json | \
  python -c "import json,sys; d=json.load(sys.stdin); print([len(w['events']) for w in d['windows']])"
```

The fixtures under `tests/fixtures/` are synthetic: a four-session digest (`digest_2026-03-14`), an
entry that names all four events (`entry_good`), and one that narrates a single event (`entry_thin`).
The linter must pass the first and fail the second — if that pair ever stops behaving that way, the
check has rotted. They are deliberately disjoint from any real journal, so the repo ships no user
data; if you change them, keep the event headings' vocabulary distinct enough for lexical matching.

## Files

| Path | Role |
|---|---|
| `scripts/journal_collect.py` | digest collector (read-only on state.db) |
| `scripts/journal_lint.py` | coverage/voice/length linter |
| `scripts/check_package.py` | pre-publish checks for this package |
| `config/journal.example.json` | English config, all keys documented |
| `config/journal.zh.example.json` | Chinese labels |
| `assets/style.example.md` | writer style file, English |
| `assets/style.zh.example.md` | writer style file, Chinese |
| `references/collector-design.md` | queries, window math, env knobs |
| `references/writer-and-prompt.md` | writer contract, prompt shape, regeneration, A/B method |
| `references/deployment.md` | cron wiring, catch-up, troubleshooting |
