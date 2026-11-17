## Description:

Monitor OpenClaw agent health, token usage, API cost, and context window in real time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuhao6741](https://clawhub.ai/user/liuhao6741)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent operators use Clawprobe to monitor live agent health, context utilization, estimated API cost, compaction events, and optimization suggestions during agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The globally installed clawprobe npm package or source repository may not match the reviewed release.

Mitigation: Verify the npm package and source repository before installation, and prefer a pinned reviewed version.

Risk: Monitoring may expose local agent session telemetry, cost estimates, and compaction history to the monitoring process.

Mitigation: Run Clawprobe only in environments where that local agent-session information is acceptable to expose.

Risk: Reported cost figures are estimates.

Mitigation: Check exact spend against the model provider billing dashboard before relying on cost totals.

## Reference(s):

- [ClawProbe homepage](https://github.com/seekcontext/ClawProbe)
- [ClawHub skill page](https://clawhub.ai/liuhao6741/skills/clawprobe)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI commands can emit structured JSON for programmatic monitoring; cost figures are estimates and should be checked against provider billing.]

## Skill Version(s):

0.6.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
