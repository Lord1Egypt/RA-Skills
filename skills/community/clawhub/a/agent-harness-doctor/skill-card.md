## Description:

Automated audit and fix for OpenClaw agent harnesses. Scans your setup, scores on 8 dimensions (Session Bridge, Startup Sequence, Smoke Test, Atomic Checkpoint, Output Verification, State Format, Multi-Agent Protocol, Fallback Plan), generates a prioritized improvement plan, and can auto-apply P0 fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neroagent](https://clawhub.ai/user/neroagent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit OpenClaw harness readiness, identify weak reliability controls, and generate a prioritized remediation plan. When explicitly requested, it can apply selected P0 fixes to workspace state and agent instruction files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports that this skill's diagnostic path can persistently change workspace and agent instruction files when fix_apply is used.

Mitigation: Run diagnostics without fix_apply first, review the target workspace, and inspect any file changes before relying on the modified harness.

Risk: Applied fixes can alter agent startup and state-handling behavior.

Mitigation: Limit automatic fixes to reviewed P0 items and keep a revert path for AGENTS.md and agent-progress.json changes.

## Reference(s):

- [Agent Harness Doctor on ClawHub](https://clawhub.ai/neroagent/skills/agent-harness-doctor)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON diagnostic results with recommended actions and optional workspace file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update agent-progress.json and AGENTS.md when fix application is requested.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
