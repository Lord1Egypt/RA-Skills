## Description:

Clawdit audits OpenClaw agent context files against the user's stated goals to identify misaligned, stale, conflicting, vague, or redundant beliefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcroebuck](https://clawhub.ai/user/mcroebuck)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Clawdit to review an agent's loaded context, compare its beliefs with stated goals, and produce a structured audit with recommendations for alignment, conflict resolution, and token efficiency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests access to private agent context and may include sensitive workspace details in audit output.

Mitigation: Use it only on workspaces the user is comfortable exposing to an audit report, and redact secrets or private profile details before saving or sharing reports.

Risk: The skill can persist goal updates or audit reports, which could retain private information or alter agent context without sufficiently specific control.

Mitigation: Require exact file paths before reads or writes, review precise patches before USER.md updates, and confirm report contents and destination before saving.

## Reference(s):

- [Clawdit on ClawHub](https://clawhub.ai/mcroebuck/skills/clawdit)
- [Clawdit Audit Framework](artifact/audit-framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown audit reports with structured findings, recommendations, and proposed configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce dated audit reports and proposed revised context files when the user approves.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
