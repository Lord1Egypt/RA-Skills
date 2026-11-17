## Description:

A skill dedicated to Antom payment integration, helping merchants select the right product and integration approach based on business needs, and build code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-intl](https://clawhub.ai/user/ant-intl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose an Antom payment product and integration mode, then implement and validate merchant payment flows for one-time, tokenized, or subscription payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment integration mistakes can expose private keys or trust unverified client-side payment results.

Mitigation: Keep private keys on the server, never log or commit them, and confirm payment status through verified asynchronous notifications or transaction query APIs.

Risk: Generated integration code may use stale API parameters or examples from dynamic remote documentation.

Mitigation: Fetch the relevant Antom product documentation and SDK guidance before coding, then verify SDK packages, endpoints, signatures, notification handling, and credential storage against current official documentation before production use.

## Reference(s):

- [SDK Description](https://cdn.marmot-cloud.com/page/antom-integration-doc/references/select-sdk.md)
- [Product Decision](https://cdn.marmot-cloud.com/page/antom-integration-doc/references/product-decision.md)
- [Integration Checklist](https://cdn.marmot-cloud.com/page/antom-integration-doc/references/checklist.md)
- [Antom Official Website](https://www.antom.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference current remote Antom documentation that should be reviewed before production use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
