## Description:

Track, analyze, and optimize AI and infrastructure costs with budgeting, spend forecasts, token usage scans, and optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to track AI model, infrastructure, subscription, power, and hardware costs, set monthly budgets, scan local gateway logs for token usage, forecast spend, and generate optimization recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running scan-tokens reads local OpenClaw gateway logs and records aggregate model, token, and cost data in a local SQLite database.

Mitigation: Run scans only where local usage-history storage is acceptable, and set COST_GUARDIAN_DIR or edit config.json when data must be stored in a specific location.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Human-readable terminal output or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local cost configuration and SQLite data under ~/.openclaw/workspace/costs/ by default; COST_GUARDIAN_DIR can override the storage location.]

## Skill Version(s):

1.0.0 (source: server release metadata and script VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
