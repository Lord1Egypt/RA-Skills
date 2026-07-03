---
name: geordi
description: Use when turning a coding goal or PRD into bounded build missions, running those missions with Codex or Droid, verifying outcomes separately, and preserving receipts. Geordi merges the former build-pipeline discipline with the installable mission runner.
version: 1.1.1
author: SuperAda
license: MIT
metadata:
  tags: [agent-workflow, geordi, codex, droid, build-pipeline, missions, verification]
---

# Geordi

Geordi is the builder workflow for goal-driven coding work. It combines the former build-pipeline discipline — context first, implementation second, independent verification, retries, and receipts — with an installable CLI that can run bounded missions through Codex or Droid.

The machinery is intentionally plain: define a goal, add missions, run one runtime at a time, verify with real commands, and leave logs behind. Less mysticism. More receipts.

## What Geordi does

- Defines a **goal**: the operator outcome.
- Breaks work into **missions**: bounded implementation units with acceptance checks.
- Loads project context before building.
- Prepends the shared global `AGENTS.md` context before every mission prompt.
- Runs missions through **Codex** or **Droid**.
- Keeps state in `.geordi/state/` so runs can be resumed or audited.
- Separates implementation from verification.
- Captures receipts: prompts, command logs, verification logs, and git status before/after.

## Install

From the source repo:

```bash
git clone https://github.com/h-mascot/Enterprise-Crew-skills.git /tmp/enterprise-crew-skills
bash /tmp/enterprise-crew-skills/geordi/install.sh
```

Or one line, pinned to the public release:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/h-mascot/Enterprise-Crew-skills/v1.1.0/geordi/install.sh)
```

The installer copies the bundle into `~/.geordi`, creates `~/.local/bin/geordi`, and prints a verification command.

## Quick start

```bash
cd /path/to/repo
geordi init --goal "Ship dark mode settings" --mode codex
geordi mission add "Add settings toggle" --accept "npm test"
geordi run --mode codex
geordi status
```

## Global AGENTS context

Geordi requires a global `AGENTS.md` file by default. This keeps mission runs aligned with the operator's shared agent rules before project-specific context is applied.

Default path:

```bash
~/.agents/AGENTS.md
```

Override when needed:

```bash
GEORDI_AGENTS_FILE=/path/to/AGENTS.md geordi run --mode codex
```

To intentionally run without a global file:

```bash
GEORDI_REQUIRE_AGENTS=0 geordi run --mode codex
```

`geordi doctor` checks the global file unless `GEORDI_REQUIRE_AGENTS=0` is set.

Droid version:

```bash
cd /path/to/repo
geordi init --goal "Fix checkout form validation" --mode droid
geordi mission add "Repair validation and errors" --accept "npm test"
geordi run --mode droid --model "custom:Your-Model-0"
```

## Mission contract

Each mission should include:

- **Title** — what to change.
- **Acceptance command** — what proves it worked.
- **Scope note** — what not to touch, if relevant.

Example:

```bash
geordi mission add \
  "Add CSV export to reports page" \
  --accept "npm run test:unit -- reports" \
  --scope "Only reports UI and export helper files. Do not modify auth."
```

Good missions are small enough to verify in one command. If a mission needs five unrelated acceptance commands, split it.

## Runtime modes

### Codex mode

Uses `codex exec` from the current git repository.

Good for:

- feature builds
- refactors
- tests and type fixes
- PR review follow-up

Default command shape:

```bash
codex exec --full-auto "<mission prompt>"
```

Override with:

```bash
GEORDI_CODEX_ARGS="exec --full-auto" geordi run --mode codex
```

### Droid mode

Uses `droid exec` with optional `--model` and `--auto` settings.

Good for:

- BYOK model routing
- custom OpenAI-compatible endpoints
- Droid mission-style coding passes
- UI/code tasks where Droid is already configured

Default command shape:

```bash
droid exec --auto medium --cwd "$PWD" -m "$MODEL" "<mission prompt>"
```

Override with:

```bash
GEORDI_DROID_AUTO=low geordi run --mode droid --model "custom:Your-Model-0"
```

## Context-first build loop

The core build-pipeline rule remains: **load context before implementation**.

Before running a non-trivial mission, collect:

1. `AGENTS.md`, `CLAUDE.md`, or other repo agent instructions.
2. Relevant PRD/story/task text.
3. Existing test/build commands.
4. Recent git status and nearby code conventions.
5. Explicit scope exclusions.

The bundled helper scripts can support this pattern:

```bash
~/.geordi/scripts/load-context.sh /path/to/repo
~/.geordi/scripts/update-context.sh /path/to/repo "Added CSV export with unit tests; npm test passes."
```

If those scripts do not match a repo, do the same manually and put the important context directly into the mission title/scope.

## State layout

Inside the target repo:

```text
.geordi/
  goal.md
  missions.jsonl
  state/
    run-YYYYmmdd-HHMMSS/
      mission-001.prompt.md
      mission-001.log
      mission-001.verify.log
      git-before.txt
      git-after.txt
      summary.md
```

## Operator rules

1. Do not run open-ended prompts when a mission can be bounded.
2. Do not count agent completion as success; run the acceptance command.
3. Do not hide failures. Preserve the log and make the next mission smaller.
4. Do not put secrets in missions, prompts, or logs.
5. Read repo instructions before changing code.
6. Commit only after verification passes and scope is reviewed.
7. If verification fails, retry with the exact failure log and a smaller repair mission.

## When to use Geordi

Use Geordi when the work is larger than a single prompt but smaller than a full project-management system:

- Build a feature across a few files.
- Convert a PRD into a sequence of agent missions.
- Run the same mission through Codex or Droid and compare results.
- Keep receipts for agent work without building a control plane.
- Continue the former build-pipeline workflow under the shorter `geordi` name.

Do not use Geordi for:

- one-line edits where a normal direct change is cleaner
- destructive repo rewrites without explicit operator approval
- secrets, credentials, payment flows, or private data entry
- unbounded “go improve the whole codebase” prompts

## Verification

```bash
geordi doctor
```

Checks:

- bundle installed
- target directory is a git repo
- requested runtime exists (`codex` or `droid`)
- mission file is parseable
- acceptance command is available for each mission

## Common pitfalls

1. **Running the agent before reading repo instructions.** Always load context first.
2. **Over-wide missions.** Split broad PRD stories into smaller missions with one acceptance command each.
3. **Treating agent success as real success.** The acceptance command is the proof.
4. **Committing generated dirt.** Review `git status --short` before committing.
5. **Leaking private environment details.** Keep model IDs, internal hosts, private paths, and secrets out of public missions and docs.

## Verification checklist

- [ ] `geordi --version` prints the expected version.
- [ ] `geordi doctor` passes inside a git repo.
- [ ] `geordi init` creates `.geordi/goal.md` and `.geordi/missions.jsonl`.
- [ ] `geordi mission add` appends valid JSONL.
- [ ] `geordi run` writes prompt/log/verification receipts.
- [ ] Acceptance command output is preserved in `.geordi/state/*/*.verify.log`.
