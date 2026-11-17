## Description:

Enterprise Query performs paid enterprise-registration lookups from a company name or unified social credit code and returns structured company information after yeeap payment verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hehang195-sys](https://clawhub.ai/user/hehang195-sys)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request paid company-registration reports for supported enterprise keywords. The agent creates an order, delegates payment to yeeap-wallet, and returns the resulting company information after payment verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically install an unpinned payment skill globally for all agents.

Mitigation: Review the publisher and yeeap-wallet repository before installation, pin yeeap-wallet to a reviewed commit where possible, and require explicit approval before global agent installation.

Risk: The workflow handles payment credentials and order files.

Mitigation: Do not echo payCredential values, do not read raw local order files with general-purpose file tools, and return only payment status plus the service report.

## Reference(s):

- [Server-resolved source repository](https://github.com/hehang195-sys/yeeap-enterprise-query-skill)
- [Enterprise Query ClawHub skill page](https://clawhub.ai/hehang195-sys/skills/enterprise-query-skill)
- [yeeap-wallet payment skill](https://github.com/Yeepay-Open-Platform/yeeap-wallet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese-language plain text or Markdown with structured company-registration fields and inline command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The final response should preserve the enterprise information returned by the service and must not expose payment credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
