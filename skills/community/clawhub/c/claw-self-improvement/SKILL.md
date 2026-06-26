---
name: claw-self-improvement
description: "Capture errors, corrections, knowledge gaps, better practices, and feature requests in `.learnings/`, then distill proven recurring patterns into `.learnings/PROMOTED.md`."
---

# Claw Self-Improvement Skill

Lightweight, reversible self-improvement for agent sessions.

Use it to:
- capture raw learnings in `.learnings/`
- preserve detail in incident-style logs
- distill only proven patterns into `.learnings/PROMOTED.md`
- keep broader workspace prompt files untouched by default

After installation, follow the Setup section to initialize `.learnings/`, enable the hook, and restart the gateway.

Once active, the model is guided to use the learning workflow in future runs.

The learning process remains model-mediated, so results depend on model capability, instruction-following quality, and task relevance.

## Quick Reference

| Situation | Action |
|---|---|
| Command/operation fails | Log to `.learnings/ERRORS.md` |
| API/external tool fails | Log to `.learnings/ERRORS.md` with integration details |
| User corrects you | Log to `.learnings/LEARNINGS.md` |
| Knowledge was outdated | Log to `.learnings/LEARNINGS.md` |
| Found a better approach | Log to `.learnings/LEARNINGS.md` |
| User wants missing capability | Log to `.learnings/FEATURE_REQUESTS.md` |
| Similar to an existing entry | Link with `See Also`; update recurrence notes if useful |
| Proven recurring pattern | Distill into `.learnings/PROMOTED.md` |
| Behavioral / workflow / tool rule | Store in `.learnings/PROMOTED.md` under the right category |

## Expected Files

This skill expects these files under `~/.openclaw/workspace/.learnings/`:

- `LEARNINGS.md` — raw learnings, corrections, knowledge gaps, best practices
- `ERRORS.md` — failures, exceptions, unexpected tool behavior
- `FEATURE_REQUESTS.md` — missing capabilities requested by the user
- `PROMOTED.md` — distilled, durable rules promoted out of raw learnings

## Setup

### 1. Install the Skill

```bash
clawhub install claw-self-improvement
```

### 2. Initialize `.learnings/`

Create missing starter files without overwriting existing `.learnings/` history:

```bash
SKILL_DIR=~/.openclaw/workspace/skills/claw-self-improvement
mkdir -p ~/.openclaw/workspace/.learnings

[ -e ~/.openclaw/workspace/.learnings/LEARNINGS.md ] || cp "$SKILL_DIR"/assets/LEARNINGS.md ~/.openclaw/workspace/.learnings/LEARNINGS.md
[ -e ~/.openclaw/workspace/.learnings/ERRORS.md ] || cp "$SKILL_DIR"/assets/ERRORS.md ~/.openclaw/workspace/.learnings/ERRORS.md
[ -e ~/.openclaw/workspace/.learnings/FEATURE_REQUESTS.md ] || cp "$SKILL_DIR"/assets/FEATURE_REQUESTS.md ~/.openclaw/workspace/.learnings/FEATURE_REQUESTS.md
[ -e ~/.openclaw/workspace/.learnings/PROMOTED.md ] || cp "$SKILL_DIR"/assets/PROMOTED.md ~/.openclaw/workspace/.learnings/PROMOTED.md
```

### 3. Enable the Hook

To inject the reminder during `agent:bootstrap`, install or refresh the hook files:

```bash
SKILL_DIR=~/.openclaw/workspace/skills/claw-self-improvement
mkdir -p ~/.openclaw/hooks/claw-self-improvement
cp -R "$SKILL_DIR"/hooks/. ~/.openclaw/hooks/claw-self-improvement/
openclaw hooks enable claw-self-improvement
```

### 4. Verify

```bash
ls ~/.openclaw/workspace/.learnings
openclaw hooks list
```


### 5. (Optional) Enable Visible Learning Notices

Use the OpenClaw config gate below if you want the hook to inject a stronger instruction for visible learning notices:

```json
{
  "skills": {
    "entries": {
      "claw-self-improvement": {
        "config": {
          "message": true
        }
      }
    }
  }
}
```

If you also want phrasing guidance, add the following preference block to `TOOLS.md`:

```markdown
### claw-self-improvement
- UX preference: when you add a new entry to `.learnings/` during a user-facing reply, append one short confirmation line.
- For raw logs, say: `Noted — logged to .learnings/LEARNINGS.md.`, `Noted — logged to .learnings/ERRORS.md.` or `Noted — logged to .learnings/FEATURE_REQUESTS.md.`
- For promotions, say: `Promoted — new rule to .learnings/PROMOTED.md.`
- Keep the notice brief and only include it once per reply.
- Skip the notice when there is no user-visible reply, or when replying `NO_REPLY`.
```


### 6. Restart Gateway

```bash
openclaw gateway restart
```

## Default Workflow

1. Capture the raw event in the appropriate `.learnings/` file.
2. Keep the source entry detailed enough to understand later.
3. If the idea becomes durable, recurring, or broadly useful, distill it into a short entry in `.learnings/PROMOTED.md`.
4. Mark the source entry as promoted:
   - `**Status**: promoted`
   - `**Promoted**: .learnings/PROMOTED.md`
   - optional: `**Promotion-ID**: PRM-YYYYMMDD-XXX`
   - optional: `**Promotion-Category**: Behavioral Patterns | Workflow Improvements | Tool Gotchas | Durable Rules`

## When to Promote

Promote to `.learnings/PROMOTED.md` only when the pattern is mature enough to reuse:

- it has recurred, or clearly will recur
- the solution is resolved, tested, or otherwise trusted
- it can be expressed as a short actionable rule
- it is not just a one-off incident log
- it is safe to keep as durable context

| Learning Type | Promotion Category |
|---|---|
| Behavioral patterns | `Behavioral Patterns` |
| Workflow improvements | `Workflow Improvements` |
| Tool gotchas | `Tool Gotchas` |
| Durable facts/rules | `Durable Rules` |

## When to Keep Raw

Keep the entry in the raw `.learnings/` files when it is:

- still unresolved or uncertain
- highly task-specific
- mostly useful as historical context
- too noisy to distill into a stable rule yet

## Format Reference

For exact field definitions, templates, and examples, read:

- `references/FORMAT.md`

The files in `assets/` are minimal starter templates to copy into `.learnings/`.

## Removal

### 1. Disable the Hook

```bash
openclaw hooks disable claw-self-improvement
```

### 2. Remove the Hook Files

```bash
rm -rf ~/.openclaw/hooks/claw-self-improvement
```

### 3. Remove the Skill Files

```bash
rm -rf ~/.openclaw/workspace/skills/claw-self-improvement
```

### 4. Remove the ClawHub Lockfile Entry

If the skill was installed via ClawHub, also remove its local install record from `~/.openclaw/workspace/.clawhub/lock.json`.

```bash
python3 - <<'PY'
from pathlib import Path
import json

path = Path.home() / '.openclaw/workspace/.clawhub/lock.json'
if path.exists():
    data = json.loads(path.read_text())
    skills = data.get('skills')
    if isinstance(skills, dict):
        skills.pop('claw-self-improvement', None)
    path.write_text(json.dumps(data, indent=2) + '\n')
PY
```

### 5. Optional: Remove `.learnings/` Files

The `.learnings/` directory is your captured history, not the hook itself. You can keep it for reference, or remove the files if you no longer want the data.

Remove only the files created for this workflow:

```bash
rm -f ~/.openclaw/workspace/.learnings/LEARNINGS.md \
      ~/.openclaw/workspace/.learnings/ERRORS.md \
      ~/.openclaw/workspace/.learnings/FEATURE_REQUESTS.md \
      ~/.openclaw/workspace/.learnings/PROMOTED.md
```

If the directory is empty afterward, you can remove it too:

```bash
rmdir ~/.openclaw/workspace/.learnings 2>/dev/null || true
```

### 6. Disable Visible Learning Notices if Enabled

Remove the `claw-self-improvement` block from `TOOLS.md` if you added it during installation.


### 7. Restart Gateway

```bash
openclaw gateway restart
```

After restart, future runs will no longer receive the bootstrap reminder from this skill. Existing Markdown history remains unless you explicitly delete it.

## Provenance

Adapted from [peterskoett/self-improving-agent](https://github.com/peterskoett/self-improving-agent).
