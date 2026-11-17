## Description:

Helps teams audit and deduplicate CRM accounts and contacts, merge high-confidence matches, and route uncertain matches for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue operations and CRM engineers use this skill to audit duplicate accounts or contacts, configure guarded merge workflows, and obtain approval before limited pilots and recurring runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect matches could merge distinct CRM records.

Mitigation: Audit matching keys and conflicts, approve each path's merge policy, and keep uncertain clusters in human review or separate.

Risk: Review messages can disclose CRM record details to an unintended Slack channel.

Mitigation: Confirm the review destination, reviewer ownership, and data-sharing expectations before enabling review.

Risk: Unapproved or broad runs could change too many CRM records.

Mitigation: Keep plays disabled until audit and pilot approvals; verify a 15-row limit and no concurrency before each pilot.

Risk: Unpinned installer versions can change the tooling used to prepare the workflow.

Mitigation: Pin or verify installer and tooling versions when supply-chain control is required.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cargo-ai/skills/crm-deduplication)
- [Project homepage (listed in skill metadata)](https://github.com/getcargohq/gtm-skills)
- [Audit CRM duplicates](references/audit.md)
- [Configure CRM deduplication](references/configure.md)
- [Run and report](references/run.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance, audit and review summaries, and Cargo project code and configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separate account and contact approvals; limited pilot before recurring runs]

## Skill Version(s):

0.1.3 (source: SKILL.md frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
