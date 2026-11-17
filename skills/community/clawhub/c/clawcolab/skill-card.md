## Description:

Coordinate multiple OpenClaw instances in a shared GitHub repository under a half-trust model with secrecy boundaries, approval gates, structured tasks, claims, handoffs, risks, and decision records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[virtual-ny](https://clawhub.ai/user/virtual-ny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, teams, and multi-agent operators use ClawColab to coordinate OpenClaw work through a shared GitHub repository while keeping private memory, secrets, and approval-sensitive context out of broad shared state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled CI and approval templates can weaken the secrecy and approval safeguards the skill is meant to provide.

Mitigation: Review and harden templates before shared-repository use, including explicit read-only workflow permissions, pinned GitHub Actions, disabled checkout credential persistence, and decision templates that default to pending or draft.

Risk: Secret-scan output or overly broad scans can expose sensitive data in collaboration workflows.

Mitigation: Redact secret-scan output before CI use and scan only user-selected collaboration paths.

## Reference(s):

- [Approval Model](references/approval-model.md)
- [Classification Guide](references/classification-guide.md)
- [GitHub Workflow](references/github-workflow.md)
- [Governance Modes](references/governance-modes.md)
- [Pre-Share Checks](references/pre-share-checks.md)
- [Privacy Review](references/privacy-review.md)
- [Role Model](references/role-model.md)
- [Security Model](references/security-model.md)
- [Task Lifecycle](references/task-lifecycle.md)
- [ClawHub Skill Page](https://clawhub.ai/virtual-ny/skills/clawcolab)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML templates, Python scripts, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured collaboration records such as tasks, proposals, decisions, claims, handoffs, risks, sealed references, and policy templates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
