## Description:

Use Brigade to set up and review agent memory handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-workspace operators use Brigade to set up, lint, and review local memory handoffs before the memory owner ingests them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Handoff content or diagnostics may expose private information when ingested or shared.

Mitigation: Review handoff content before ingestion and redact diagnostics and sensitive details before sharing.

Risk: The setup example installs the CLI without pinning a version.

Mitigation: Choose and install a reviewed Brigade CLI version.

## Reference(s):

- [Brigade Handoffs release page](https://clawhub.ai/solomonneas/skills/brigade-handoffs)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-first workflow; drafts and receipts await review and do not automatically edit canonical memory.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
