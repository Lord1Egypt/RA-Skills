## Description:

Gene Engine automates lifecycle management for agent behavior rules, including retirement checks, cooldown handling, active probing, verification intervals, wake-up-rate calculation, health scoring, metrics logging, JSON summaries, and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smilepeng0612](https://clawhub.ai/user/smilepeng0612)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Gene Engine in OpenClaw workspaces to audit and maintain behavior-rule state, identify stale or failing rules, and generate status summaries for heartbeat workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted gene keys or outcome text could execute unintended code while changing persistent agent state.

Mitigation: Run only in a trusted OpenClaw workspace, do not pass untrusted gene keys or outcome text, and fix the Python interpolation issues before shared or automated use.

Risk: The scripts update gene-state.json and append metrics logs in the OpenClaw workspace.

Mitigation: Review the scripts before installation, keep recoverable copies of workspace state, and restrict execution to the workspace owner.

## Reference(s):

- [Gene Engine on ClawHub](https://clawhub.ai/smilepeng0612/skills/gene-engine)
- [smilepeng0612 ClawHub profile](https://clawhub.ai/user/smilepeng0612)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text status reports with machine-readable JSON summaries and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates gene-state.json and appends metrics to gene-metrics.log in the OpenClaw workspace.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
