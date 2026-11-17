---
name: agent-config-lint
description: Check agent config for things that break silently on someone else's machine. Use before publishing or committing a SKILL.md, AGENTS.md, CLAUDE.md or llms.txt, before publishing a skill to ClawHub, when a skill "works on my machine" but not for a teammate, when a skill fails to trigger, or when asked to review agent config. Catches references to files that do not exist, absolute paths under the author's home directory, undeclared CLI dependencies, a frontmatter name that does not match the skill's directory, and two skills whose descriptions are so similar the agent fires the wrong one.
metadata:
  openclaw:
    emoji: "🔎"
    homepage: https://github.com/hyuga611/tenken
    requires:
      anyBins:
        - npx
        - node
    install:
      - kind: node
        package: "@hyuga/tenken"
        bins: [tenken]
---

# Agent config lint

Agent config fails quietly. A `SKILL.md` points at a script that was renamed, an
`AGENTS.md` hardcodes the author's home directory, two skills describe themselves so
similarly the agent picks the wrong one. Nothing throws — the agent just does the wrong
thing, and only on someone else's machine.

This skill runs `tenken`, which bundles three zero-dependency linters in one pass.

## When to use

Run it when any of these is true:

- about to commit or publish a `SKILL.md`, `AGENTS.md`, `CLAUDE.md` or `llms.txt`
- about to publish a skill to ClawHub
- a skill works for the author but not for a teammate
- a skill is not firing, or the wrong skill fires
- the user asks to review or check agent config

## How to run

```bash
npx @hyuga/tenken
```

Scan a specific path:

```bash
npx @hyuga/tenken path/to/skills
```

Machine-readable output, for when you need to act on individual findings:

```bash
npx @hyuga/tenken --format json
```

Exit code is `0` when clean, `1` when there is at least one error, `2` on bad usage.
Warnings do not fail unless `--strict` is passed.

## What it catches

| | |
|---|---|
| a back-quoted path or markdown link that does not resolve | reference rot |
| `/Users/<name>/…`, `C:\Users\<name>\…` | will not resolve for anyone else | <!-- carry-ignore -->
| an external CLI the document never declares or installs | missing dependency |
| an unresolved `<FILL_ME>` / `REPLACE_ME` left in a shipped file | unfinished | <!-- carry-ignore -->
| frontmatter `name` that does not match the skill's directory | installs under a different identity |
| missing `name` or `description` | the agent has no trigger to match on |
| two descriptions ≥0.7 similar | the agent fires the wrong skill |

## Reading the output

Each line is `[engine] file:line message`. Lines marked `!` are warnings.

```
✗ .claude/skills/report/SKILL.md — 2 problems
    [skills-lint] .claude/skills/report/SKILL.md:1  name "Report_Skill" does not match its directory "report"
    [skills-lint] .claude/skills/report/SKILL.md:12 reference `scripts/build-report.py` does not exist
```

Fix in this order, because the first two stop the skill from working at all:

1. missing or malformed frontmatter — the agent cannot trigger the skill
2. `name` not matching the directory — it installs under an identity nobody can find
3. absolute paths and undeclared CLIs — it breaks on the next machine
4. broken references — the agent reads something that is not there

## Suppressing a finding

When a path or dependency is deliberate:

```md
Save to `C:\tools\out.png` <!-- carry-ignore -->
```

To keep a specific reference out of the check, pass `--ignore <path>`. To allow a CLI the
document intentionally depends on, pass `--allow codex,gemini`.

## Scope

Static analysis only. It runs no model and needs no API key, so it costs nothing to run on
every commit and returns the same answer every time. It does not check whether a skill is
*good* — only whether it will still work once it leaves the machine it was written on.

For prompt-injection, malware and supply-chain scanning, use a security scanner instead;
this is a hygiene and portability check and does not replace one.

Source and issues: https://github.com/hyuga611/tenken
