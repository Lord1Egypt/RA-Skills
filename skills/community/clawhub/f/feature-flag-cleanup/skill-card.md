## Description:

Audits feature flag debt across common flag platforms and codebases, then produces stale-flag inventories, risk-ranked cleanup plans, removal pull requests, rollback plans, and prevention guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and DevOps teams use this skill to find stale feature flags, prioritize safe retirement work, generate owner-tagged tickets and PR plans, and reduce flag debt across flag services and monorepos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce broad cleanup plans involving flag archives, hard deletes, code removals, migrations, cron jobs, or persistent memory updates without clear confirmation gates.

Mitigation: Use narrow project and environment scope, require dry-run inventories first, review exact flag IDs and affected environments, and manually approve every PR, migration, archive, hard-delete, cron, or memory update.

Risk: Incomplete telemetry, ownership data, or environment context can cause active, high-risk, or compliance-sensitive flags to be misclassified as stale.

Mitigation: Provide service exports, code-reference grep results, 30 or more days of evaluation telemetry, CODEOWNERS or equivalent ownership data, target environments, and regulatory constraints before planning removals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/feature-flag-cleanup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, code blocks, shell/API commands, CSV-style inventories, ticket drafts, PR descriptions, and cleanup plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deletion, archive, migration, cron, and PR recommendations that require human review and approval before execution.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
