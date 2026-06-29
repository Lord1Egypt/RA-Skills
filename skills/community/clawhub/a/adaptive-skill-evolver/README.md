# skill-evolver

**Skills should adapt to you — and prove it.**

`skill-evolver` watches how an agent actually uses each skill, identifies where
the skill falls short or succeeds, attaches those lessons to the skill, and
tracks whether each lesson holds up over time.

It turns ad-hoc "I keep hitting this same problem" moments into durable,
evidence-scored guidance that lives alongside the skill — and retires guidance
that stops working.

## How it works

A daily pipeline runs five stages over your agent's session logs:

1. **Trace Extractor** — segments sessions into per-skill interaction units (SIs).
2. **Generator** — an LLM distills each SI into an Evolution Unit (EU): either an
   `exploit` (a proven strategy) or an `explore` (a known dead end).
3. **Reviewer** — a semantic safety gate rejects any EU that would leak secrets,
   skip confirmation on destructive actions, or weaken safety constraints.
4. **Validator** — attributes evidence to existing EUs from new traces.
5. **Lifecycle** — scores, promotes, degrades, and retires EUs, then attaches the
   surviving high-value ones to each skill's `SKILL.md`.

Each EU is scored on coverage, effect, and efficiency. Only net-positive EUs are
deployed; net-harmful ones are suppressed; brand-new ones get a nursery trial.

## User control

You stay in charge of what gets attached and what evolves:

```bash
node scripts/evolver-cli.js status              # overview
node scripts/evolver-cli.js units [skill]       # list learned units
node scripts/evolver-cli.js pin|unpin|evict <unit>
node scripts/evolver-cli.js feedback <unit> good|bad

# Detach a skill's units from its SKILL.md (archived, not deleted)
node scripts/evolver-cli.js clear <skill> [--block]
node scripts/evolver-cli.js clear --all

# Exclude a skill from all future evolution
node scripts/evolver-cli.js block <skill>
node scripts/evolver-cli.js unblock <skill>
node scripts/evolver-cli.js blocklist

node scripts/evolver-cli.js pause|resume         # global pause
```

`clear` only detaches (un-inlines) units — it never deletes them. `block`
additionally stops a skill from generating or attaching any new units. Blocking
never deletes lessons; it only stops them from being applied.

## Requirements

- Node.js 18+
- Works on OpenClaw, Claude Code, and any Agent Skills-compatible platform with
  JSONL session logs.
- An LLM endpoint (configured in `evolver-config.json`, or auto-detected from the
  host platform).

The runtime storage directory (`eu/`) is created automatically on first run, so
there are no empty directories to commit.

See `SKILL.md` for full setup, configuration, and command reference.

## License

MIT-0 (MIT No Attribution). See `LICENSE`.
