## Description:

Evaluates PA-managed tasks, skills, network health, billing, calendar connections, and memory quality by combining supervisor status checks with quality scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Owners and operators of OpenClaw PA workspaces use this skill to run on-demand, weekly, or incident-driven evaluations of task status, integration health, memory health, and PA performance. The skill produces a structured report with scores, findings, and prioritized recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect broad workspace state and run local shell checks.

Mitigation: Review the paths and commands before use, scope checks to the intended workspace, and require explicit approval before running broad audits.

Risk: The skill can contact external services with local credentials.

Mitigation: Require explicit consent for live credentialed checks, use least-privilege credentials, and avoid printing tokens or sensitive response bodies.

Risk: The skill loads local context through shell source semantics.

Mitigation: Replace shell sourcing with a safe configuration parser before deployment.

Risk: The skill can create ongoing feedback and evaluation records.

Mitigation: Define where logs are stored, who can read them, and how they are retained or deleted.

## Reference(s):

- [ClawHub Eval skill page](https://clawhub.ai/netanel-abergel/skills/eval)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with inline shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scores, counts, integration status checks, memory-health checks, and recommendations.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
