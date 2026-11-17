## Description:

Professional AI agent team management system for coordinating multiple OpenClaw agents with task assignment, progress tracking, quality control, and performance evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[komong](https://clawhub.ai/user/komong)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI operations teams use this skill to coordinate multiple OpenClaw agents across complex projects, including task assignment, progress tracking, quality review, performance evaluation, and workflow management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can include untrusted task or agent data.

Mitigation: Sanitize or escape caller-provided task names, statuses, and agent identifiers before rendering or sharing HTML reports.

Risk: Quality scoring and review gates may be unreliable.

Mitigation: Use generated quality scores as advisory signals only, and keep human review or independent validation for release decisions.

Risk: The implementation appears incomplete or overclaimed relative to its documentation.

Mitigation: Pilot the modules on non-critical workflows and verify each claimed integration before relying on the skill operationally.

Risk: The declared environment requirements request broader local workspace access than the code appears to need.

Mitigation: Run the skill with least privilege and scope OPENCLAW_WORKSPACE to a dedicated project workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/komong/skills/ai-agent-team-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, HTML, JavaScript snippets, and plain text status or guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local coordination data, reports, recommendations, and example usage patterns from caller-provided project, task, and agent inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
