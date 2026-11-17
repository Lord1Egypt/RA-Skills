# The writer side — prompt contract, linting, regeneration, A/B

`scripts/journal_collect.py` decides *what the writer sees*. This file covers *what the writer is
told*, how to prove the entry is complete, and how to change either side without wrecking the
journal.

## Why an entry can be thin when the digest is rich

The collector rarely loses a session; the writer drops events. Mechanisms seen for real:

- A prompt line like "summarize in one sentence what was done" collapses a 4-session day into the
  single event with the most emotional pull. Measured on a real digest: **0 of 4** events named in
  the entry, and the entry still read perfectly fine.
- Voice rules duplicated in the cron prompt overrode the style file the prompt told the writer to
  read: the closer, more concrete copy wins.
- An example sentence in the prompt (or in the style file) gets reproduced near-verbatim for weeks.
  Both copies must go; deleting it from only one leaves the tap open.
- The character ceiling is almost never the binding constraint — real entries ran around 60 chars
  against a 300 ceiling. Adding headroom does nothing; changing the sentence structure does.
- Pushing for "feeling" without saying *concrete* produces imagery the style bans anyway, plus
  abstract wrap-ups ("it feels good to be trusted") that repeat verbatim across entries.

## Prompt contract (the cron job's prompt)

Ten numbered lines, no more. In order:

1. read the style file first; on conflict, the style file wins;
2. the digest is material — no details, no how-it-was-solved, no tools, commands or files;
3. **coverage**: every `###` block is one event, name them all, an inventory clause is fine but
   four events means four mentions;
4. feeling after the events, at least one sentence, never a bare inventory;
5. length scales with the event count (1–2 → 300, 3–5 → 420, no floor), cut adjectives not events;
6. append one entry per window, oldest first, never touch existing entries, skip marked windows;
7. end each entry with `<!-- window:YYYY-MM-DD -->` (the window's start date);
8. `file` toolset only — no web, no terminal, no other tools;
9. **pre-submit self-check**: count the digest's `###` blocks, tick each one off in the entry,
   fill in anything missing before answering;
10. reply with one line per window: date and character count.

No tone advice, no forbidden-item list, no example sentence — all of that lives in the style file.
A working copy is in `examples/cron-prompt.md`.

Update it with `cronjob_manage(action='update', job_id=..., prompt=...)`; list jobs first rather
than guessing the id. Editing the prompt never touches the style file, and vice versa.

## Linting: the check that replaces trust

```bash
python scripts/journal_lint.py --digest digest.md --journal memory/journal/journal.md
```

Hard failures (exit 1): an event heading with no evidence in the entry, a missing marker, an entry
over its ceiling, or an entry whose day has no block in the digest (wrong day / wrong digest).

How coverage is decided, in order:

1. **Lexical.** Each `###` block contributes *distinctive* tokens — CJK bigrams and latin words that
   appear in exactly one block of that window. Tokens from the heading and `- key points:` lines are
   **strong** (one hit is enough); tokens that appear only in assistant-outcome prose are **weak**
   (two hits needed, and `--strict` still calls that weak evidence).
2. **Semantic (optional).** A paraphrase such as "merged those tables" for "combine the three price
   sheets" is invisible to re matching. If Ollama and an embedding model are present,
   the linter falls back to max cosine between the block and the entry's sentences (`--threshold`,
   default 0.45). No Ollama → lexical only, more false MISSes, still no cloud tokens.

   The 0.45 default is **calibrated, not guessed**: on the shipped fixtures with
   `qwen3-embedding:0.6b`, the entry that covers all four events scores 0.507–0.55, while the entry
   that narrates one event scores 0.296–0.312 on the three it misses (and 0.54 on the one it does
   cover). Any threshold in 0.35–0.50 separates them. Swapping embedding models changes the scale —
   re-measure a known-good and a known-thin entry before trusting a new number.

Warnings (exit 0 unless `--strict`): imagery, abstract wrap-ups, and sentences that near-duplicate
an earlier entry in the same journal (character 4-gram overlap ≥ 0.55) — the homogenisation smell.

`invented_time` ("in the morning", "深夜") is deliberately a **note**, never a failure: only the
digest clock can say whether it is true, and a strict rule would reject legitimate entries.

## See the digest a past window actually produced

Zero side effects: clone the journal into a temp file with the marker(s) you want re-owed removed,
point `JOURNAL_FILE` at the clone, and run the collector. Only unmarked windows are printed, so this
reproduces exactly what the writer received.

```bash
mkdir -p /tmp/journal-probe && cd /tmp/journal-probe
# probe.md = the journal truncated just before the target entry's marker
JOURNAL_FILE=/tmp/journal-probe/probe.md python /path/to/scripts/journal_collect.py --journal /tmp/journal-probe/probe.md
```

Count the `###` blocks in the output — that number is the coverage the entry owes.

## Regenerate one entry

Back up into a dedicated folder so backups never clutter the journal directory:
`mkdir -p .bak && cp journal.md .bak/journal-$(date +%Y%m%dT%H%M%S).md`. Then cut the file at the target entry's
`## YYYY-MM-DD` heading so the previous entry's marker is the last line, then trigger the job
(`cronjob_manage(action='run')`). The collector now sees exactly one owed window. Lint the result
against the digest before accepting it, and restore the backup if the rewrite is worse.

Full rebuild = truncate to the header block and let the job rewrite every window. That is the only
sanctioned way to mass-rewrite entries; never edit an entry in place.

## A/B a prompt or style change before trusting it

Two throwaway subagents, same digest, old rules vs new rules, text-only output — no files, no journal
writes:

- Put the digest **and** the style text **inline in each child's context**. A path in a scratch
  directory can be pruned between dispatch and read; if a path is unavoidable, use a persistent
  workspace directory.
- Tell both children it is an offline experiment, and that an existing entry for that window does
  **not** mean "skip" — otherwise the child honours the idempotency rule and returns nothing.
- Ask for the entry alone via `output_schema`, then score mechanically: count how many digest events
  are named in each entry. Coverage gaps are objective; "feels warmer" is not.

Keep the change only if the coverage count goes up, then apply it and regenerate one real window to
confirm end to end with the linter.
