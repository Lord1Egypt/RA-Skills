# Better Every Run Workflow

Better Every Run is for small, factual learning moments that the user explicitly wants persisted.

OpenClaw command name: `ber`.

## Normal Human Path

Use one command for outcome corrections:

```text
/ber fix agent used wrong host for code work -> agent uses the approved development host
```

The agent handles the helper command and reports the result. Normal `fix` and `remember` commands write only to `.better-every-run/`. Use `--scope` when the lesson has an obvious destination: `run`, `project`, `workspace`, `skill`, `memory`, or `eval`. Use `--expires YYYY-MM-DD` for temporary rules, or `--expires never` for explicit long-lived lessons.

For simple preferences:

```text
/ber remember do code work on the approved development host
```

## Internal Capture

Capture only evidence that would change future behavior and was explicitly requested through `/ber` or direct durable-learning instruction:

```bash
node scripts/ber.js capture --type correction --note "Do code work on the approved development host." --tags workspace,coding
```

Good captures:

- User explicitly asks `/ber fix ... -> ...`.
- User explicitly asks `/ber remember ...`.
- User directly asks to record a reusable workflow or safety boundary.
- A tool recovery path is reusable and the user approves capturing it.

Bad captures:

- Generic advice the base agent already knows.
- Private details unrelated to future behavior.
- Speculation without observed evidence.
- Casual chat containing words like "remember", "always", "never", or "next time" without clear durable-learning intent.

## Propose

Turn recent evidence into lesson proposals:

```bash
node scripts/ber.js propose --today
```

Proposals are not policy. They are review candidates.

## Report

Return the report in chat:

```text
/ber report
```

Keep the chat report short. Include local storage status and any open proposed lessons.

## Promote To Memory Or Skill

This flow is for agents, audits, tests, and explicit durable writes. In normal chat, summarize the result instead of making the human operate helper commands, but disclose any durable target file.

```bash
node scripts/ber.js card <lesson-id> --to memory --target memory/decisions.md
node scripts/ber.js promote <lesson-id> --to memory --target memory/decisions.md
node scripts/ber.js card <lesson-id> --to skill --target SKILL.md
node scripts/ber.js promote <lesson-id> --to skill --target SKILL.md
```

Lesson cards record target hashes and scanner verdicts before promotion. Promotion appends a reviewable block only if the target has not changed since the card was written and the scanner verdict is clean.

## Promote To Eval

Eval durability uses a structured fixture command, not markdown append promotion:

```bash
node scripts/ber.js eval-fixture <lesson-id> --target tests/ber-regressions.json
```

Eval fixture targets must be `.json` or `.jsonl` files under `tests/` or `evals/`.

## Lifecycle Hygiene

Use quarantine and supersession to keep learning sharp:

```bash
node scripts/ber.js quarantine <lesson-id> --reason "one-off"
node scripts/ber.js supersede <old-lesson-id> --by <new-lesson-id> --reason "environment changed"
```

## Review Export

This older patch flow is review-only now:

```bash
node scripts/ber.js accept <lesson-id>
node scripts/ber.js export-memory-patch
```

`apply-memory-patch` is retired and refuses. Normal `/ber fix` and `/ber remember` use should stay concise, while clearly saying the lesson is local until a reviewed promotion happens.
