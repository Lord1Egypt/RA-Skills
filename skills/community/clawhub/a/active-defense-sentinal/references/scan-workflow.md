# Scan Workflow

## 1. Detect the source
Classify the candidate as one of:
- local folder skill
- ClawHub slug
- already-installed skill
- changed skill under `~/.openclaw/skills`

## 2. Stage when needed
For ClawHub installs, stage under:
`$OPENCLAW_WORKSPACE_DIR/.skill_stage/`

Then install into the staging dir before exposing it to the active skill tree.

## 3. Run the scan
Use one of:
- `uv run skill-scanner scan <path> --format markdown --detailed --output <report>`
- `uv run skill-scanner scan-all <dir> --format markdown --detailed --output <report>`

## 4. Read the report
Look for:
- Critical
- High
- Medium
- Low
- Info

If the report cannot be parsed, treat it as Yellow and review manually.

## 5. Decide
- High/Critical: block
- Medium/Low/Info only: allow with a warning summary
- Unknown: stop and investigate

## 6. Record the decision
Always preserve:
- input path or slug
- report path
- severity summary
- timestamp
- final action
