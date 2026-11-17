# Deployment — wiring the job

## 1. Lay the skill down

```
<skills dir>/productivity/agent-daily-journal/
  SKILL.md
  scripts/journal_collect.py
  scripts/journal_lint.py
  config/journal.json          # your copy of config/journal.example.json
  references/ assets/ examples/ tests/
```

The skills directory is `<HERMES_HOME>/skills` — `%LOCALAPPDATA%/hermes/skills` on Windows,
`~/.hermes/skills` on Linux/macOS. After the first run, edit only `config/journal.json` and the
style file; the scripts stay untouched unless you are changing behaviour deliberately.

## 2. Point the config at your paths

Copy `config/journal.example.json` (or the `.zh` one) to `config/journal.json` and set
`workspace` to an **absolute** path. The journal defaults to
`<workspace>/memory/journal/journal.md`; set `journal` if it lives elsewhere. Create that file with
a header before the first run:

```markdown
# Journal

> One entry per day, 04:00 → 04:00. Append only.
```

Copy `assets/style.example.md` (or `.zh`) next to the journal as `style.md` and edit the
placeholders. The writer reads it on every run.

## 3. Create the cron job

```python
cronjob_manage(
    action="create",
    name="agent-daily-journal",
    schedule="0 4 * * *",              # local time; matches day_start_hour
    script="<absolute path to scripts/journal_collect.py>",   # its stdout is injected as the digest
    prompt="<the writer contract — see examples/cron-prompt.md>",
    skills=["agent-daily-journal"],    # loads this SKILL.md in the job's session
    enabled_toolsets=["file"],         # the writer must not have web/terminal
    deliver="local",
)
```

Notes that actually matter:

- **`script` is the whole trick.** The job runs the collector first and prepends its stdout to the
  prompt under a `Script Output` heading. The writer never runs a command itself, so it can stay on
  the `file` toolset.
- **`enabled_toolsets=["file"]`** keeps the entry honest: a writer with a shell starts chasing
  details, and details are what the entry must not contain.
- **`deliver="local"`** silences delivery noise; set a delivery target only if you want a message
  every morning.
- `cron.catch_up_missed` (default true) fires the missed 04:00 run on the first tick after Hermes
  starts. That is what makes the journal survive days when the machine was off.
- Do not create a second job for backfilling. One job with `max_windows` handles gaps; raising it is
  the only knob needed.

## 4. First-run checklist

1. `python scripts/journal_collect.py --config config/journal.json` → either the "nothing owed"
   line or one or more `## Window` blocks. If it says nothing is owed on a brand-new journal, set
   `JOURNAL_START=YYYY-MM-DD` to give it a floor.
2. `cronjob_manage(action='run', job_id=...)` → one entry appears at the end of the journal.
3. `python scripts/journal_lint.py --digest <saved digest> --journal <journal>` → exit 0,
   `coverage N/N` matching the digest.
4. Check the marker line is present and reads the window's **start** date.

## 5. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "nothing owed" forever | journal has no markers and `JOURNAL_START` unset | set `JOURNAL_START` or run with `--only DATE` once |
| every entry names one event | prompt still says "in one sentence" | use the contract in `references/writer-and-prompt.md` |
| digest is empty, journal has work | `state_db` path wrong, or sessions are `source='cron'`/`hidden=1` | check `--state-db`; pass `--only DATE --json` and inspect |
| writer reports a `write_file` refusal | a cron job appends to the same journal | append with `patch` on the last marker, or write a temp file and move it |
| entries all sound the same | example sentence in the style file or prompt | delete the example; keep shape as placeholders |
| `--json` shows `embeddings: false` | Ollama down or model name mismatch | `ollama list`, pull `qwen3-embedding:0.6b`, or accept lexical dedupe |
| lint MISSes an event the entry clearly covers | paraphrase with no shared tokens | run with Ollama up (semantic pass), or lower `--threshold` |

## 6. Windows specifics

- Both scripts are pure stdlib and path-agnostic; no shell pipeline is required.
- If a scheduled task runs them outside Hermes, invoke with
  `python "C:/path/to/scripts/journal_collect.py" --config ...` (forward slashes are fine) and set
  `HERMES_HOME` explicitly when `%LOCALAPPDATA%` is not the install root.
- Run tests with `python -m unittest discover -s tests` — no bash needed.
