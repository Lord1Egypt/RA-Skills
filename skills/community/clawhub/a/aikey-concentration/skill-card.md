## Description:

Assesses customer, channel, and product revenue concentration and estimates how long a business could operate if its largest customer left.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzifei](https://clawhub.ai/user/iamzifei)

### License/Terms of Use:

MIT-0

## Use Case:

External business owners and operators use the skill to review how much revenue depends on a small number of customers, channels, or products, assess warning signs and runway, and identify practical risks and actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles sensitive customer and financial details and may save business lessons without a stated retention limit.

Mitigation: Review the configuration and interaction guide, confirm the memory location, access permissions, and deletion arrangements, and use customer aliases or request session-only notes when appropriate.

## Reference(s):

- [Concentration analysis theory (bundled reference)](artifact/references/理论底座.md)
- [Legacy-name upgrade guide](https://github.com/iamzifei/aikey#老用户升级zmm-已改名为-ai-key)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown business review with concentration summaries, runway estimates, warning signs, and risk and do-not-do lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses figures supplied by the user; missing figures are identified rather than invented. Customer names are anonymized when data masking is enabled.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
