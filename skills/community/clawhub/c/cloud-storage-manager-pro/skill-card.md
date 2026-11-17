## Description:

云存储管理器(专业版) helps teams and enterprises manage multi-cloud storage workflows, including batch migration, bidirectional sync, KMS-backed encryption, RBAC collaboration, lifecycle tiering, replica writes, and cost analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, security engineers, and cloud administrators use this skill to plan and execute multi-cloud storage administration tasks such as migrations, sync rules, credential-backed provider setup, encryption policy configuration, lifecycle tiering, and cost reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose high-impact cloud storage operations, including migrations, bidirectional sync, lifecycle changes, KMS updates, and multi-replica writes.

Mitigation: Require explicit user approval before command execution and prefer dry-run or preview modes with cost estimates when available.

Risk: Cloud and KMS credentials may be exposed or misused if handled directly in prompts, files, or command output.

Mitigation: Store credentials in a vault or environment variables, use least-privilege cloud roles, and avoid hard-coding or displaying secrets.

Risk: The security summary says the activation scope and safety controls are too broad for automatic use.

Mitigation: Limit use to intentional cloud storage administration sessions and require review for generated commands, policies, and configuration changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cloud-storage-manager-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON snippets, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may describe high-impact cloud storage actions and should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
