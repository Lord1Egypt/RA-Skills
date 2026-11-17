## Description:

1688 Marketing helps merchants query 1688 promotional enrollment activities, review suggested offer prices, submit confirmed enrollments, and discover market opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants and agents supporting 1688 sellers use this skill to find campaign enrollment opportunities, review suggested item pricing, and submit item enrollments only after explicit merchant confirmation. It also supports market opportunity discovery through keyword and category filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages 1688 account credentials locally, which can expose business account access if the workspace, backups, or host are shared or compromised.

Mitigation: Use the skill only on trusted machines, avoid shared workspaces and synced backups for credential storage, and prefer an OS keychain-backed environment when available.

Risk: The local authorization flow uses a temporary callback server, so browser and network trust matter during setup.

Mitigation: Complete authorization only on a trusted network and verify credential status, reset, and clear behavior before using the skill for business operations.

Risk: Campaign enrollment is a write action that can affect merchant operations.

Mitigation: Query suggested prices first, present them to the merchant, and submit enrollment only after explicit confirmation.

## Reference(s):

- [1688 ClawHub Portal](https://clawhub.1688.com/)
- [Configure AK](references/capabilities/configure.md)
- [1688 Enrollment Activity Query](references/capabilities/1688_enroll_activity_query.md)
- [1688 Enrollment Offer Query](references/capabilities/1688_enroll_offer_query.md)
- [1688 Enrollment Submit Item](references/capabilities/1688_enroll_submit_item.md)
- [1688 Opportunity Recommendation](references/capabilities/1688_opp_recommend.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command results with optional Markdown summaries and CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may call 1688 services, require local AK configuration, and include a write action for campaign enrollment.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
