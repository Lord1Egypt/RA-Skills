# Geordi

Geordi is the Enterprise Crew builder workflow: an installable mission runner for goals, PRD stories, Codex/Droid execution, separate verification, and receipts.

It merges the reusable build-pipeline discipline with a small CLI under the short `geordi` name.

## One-line install

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/h-mascot/Enterprise-Crew-skills/v1.1.0/geordi/install.sh)
```

## Local install from clone

```bash
git clone https://github.com/h-mascot/Enterprise-Crew-skills.git /tmp/enterprise-crew-skills
bash /tmp/enterprise-crew-skills/geordi/install.sh
```

## What gets installed

- `~/.geordi/` — the skill bundle and helper scripts.
- `~/.local/bin/geordi` — command wrapper.

No secrets are installed. No shell profile is modified unless `~/.local/bin` is missing from `PATH`; in that case the installer prints the line to add.

## First run

```bash
cd /path/to/git/repo
geordi init --goal "Ship the smallest useful version of X" --mode codex
geordi mission add "Implement the core path" --accept "npm test"
geordi run --mode codex
geordi status
```

## Runtime options

### Codex

Requires `codex` on PATH.

```bash
geordi run --mode codex
```

Optional:

```bash
GEORDI_CODEX_ARGS="exec --full-auto" geordi run --mode codex
```

### Droid

Requires `droid` on PATH.

```bash
geordi run --mode droid --model "custom:Your-Model-0"
```

Optional:

```bash
GEORDI_DROID_AUTO=low geordi run --mode droid --model "custom:Your-Model-0"
```

## Design

Geordi is deliberately thin:

1. Store the goal.
2. Store missions as JSONL.
3. Load project context.
4. Build a mission prompt.
5. Run Codex or Droid.
6. Run acceptance checks separately.
7. Save logs and git receipts.

That is enough structure to prevent agent work from turning into interpretive dance.
