## Description:

Calculate OpenClaw usage cost from offline event logs, apply budget thresholds, and export operator-facing reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike007jd](https://clawhub.ai/user/mike007jd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use CostLens to analyze offline token usage event logs, estimate model costs, check budget thresholds, and export local reports for handoff or audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the event log path supplied by the user, and those logs may contain sensitive usage data.

Mitigation: Use event logs that are appropriate for local cost analysis, and avoid pointing the skill at sensitive logs unless aggregate cost data can be included in local output.

Risk: Report mode can create or overwrite the output file path supplied by the user.

Mitigation: Choose an explicit report path and review it before running report export in automation.

Risk: Cost calculations use built-in default rates unless events provide explicit rate overrides.

Mitigation: Use per-event rate overrides when accurate billing or audit estimates require rates different from the built-in defaults.

## Reference(s):

- [CostLens ClawHub page](https://clawhub.ai/mike007jd/skills/costlens)
- [CostLens source homepage](https://github.com/mike007jd/openclaw-skills/tree/main/costlens)
- [CostLens README](artifact/README.md)
- [CostLens skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with CLI commands; CLI output may be table text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report mode writes a JSON report file; budget checks may return a blocking exit code for critical overruns.]

## Skill Version(s):

1.0.1 (source: server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
