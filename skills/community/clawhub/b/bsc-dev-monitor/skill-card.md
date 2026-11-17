## Description:

BSC Dev Monitor Skill monitors specified BSC wallet addresses for token-transfer activity and returns detections, payment-required responses, history, and webhook notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mybusd](https://clawhub.ai/user/mybusd)

### License/Terms of Use:

MIT

## Use Case:

External users and developers who follow BSC project or developer wallets use this skill to monitor addresses for new token-transfer activity, manage monitoring sessions, and receive structured notifications for further review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes exposed payment credentials and a ClawHub password.

Mitigation: Rotate the exposed credentials, remove deployment credentials from the package, and use environment-based configuration before installation or release.

Risk: Webhook destinations can receive detection payloads and may be user supplied.

Mitigation: Validate webhook URLs and restrict destinations according to the deployment policy before enabling notifications.

Risk: The package advertises safety and filtering controls that may require review before users rely on them.

Mitigation: Implement and test those controls or remove the claims from user-facing documentation before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mybusd/skills/bsc-dev-monitor)
- [Publisher profile](https://clawhub.ai/user/mybusd)
- [SkillPay](https://skillpay.me)
- [SkillPay documentation](https://docs.skillpay.me)
- [BNB Smart Chain](https://www.binance.org/en/smart-chain)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown documentation with inline shell and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return payment links, monitor status, detection records, history records, and webhook payloads.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
