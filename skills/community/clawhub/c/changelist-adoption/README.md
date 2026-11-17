# Changelist Adoption

A [ZCode](https://zcode.ai) / agent skill that sets up and runs a **per-task changelist practice** in any repository: every completed code task becomes a small standalone engineering record, and a module index keeps months of agent- and human-driven changes searchable by functional area instead of buried in `git log`.

- One entry per task at `docs/changelist/{YYYYMMDD}/{slug}.md` — summary / problem & root cause / changes / decisions / validation
- Two-level module index at `docs/changelist/README.md` (module > submodule, date ascending)
- Rules pasted into the repo's agent instruction file (`AGENTS.md` etc.), coupled to commits
- Entries, index, code, and tests land in the same commit; a bundled verifier script proves no entry is ever dropped

Not a release `CHANGELOG.md` — a changelist entry is the engineering record of one task (root cause, diff, decisions, validation proof), while a release changelog summarizes user-visible changes per version.

## Install

Via [ClawHub](https://clawhub.ai/falllee/skills/changelist-adoption):

```bash
npx clawhub@latest install falllee/changelist-adoption
```

Or manually: copy this skill directory into the repo that should adopt the practice at `.agents/skills/changelist-adoption/`, or user-globally at `~/.zcode/skills/changelist-adoption/`.

## Usage

Ask the agent, inside the target repository, to set up change records. The skill has two modes:

- **bootstrap** — first-time setup: taxonomy design from the real architecture, index skeleton, adapted agent rules, verification.
- **per-change** — the loop after adoption: write entry → update index → commit together.

After any index edit, run the bundled checker:

```bash
node <skill-dir>/scripts/verify-index.mjs <changelist-root>
```

See [SKILL.md](SKILL.md) for the full practice definition (English / 中文).

## License

[MIT-0](LICENSE) — free to use, modify, and redistribute; no attribution required.
