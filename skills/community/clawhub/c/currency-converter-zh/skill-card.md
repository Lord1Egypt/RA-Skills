## Description:

Chinese-language currency conversion helper for exchange-rate lookup prompts and amount conversion across supported currencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjingzhi07](https://clawhub.ai/user/huangjingzhi07)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to respond to Chinese-language currency conversion requests and show reference rates for supported currencies such as USD, CNY, EUR, JPY, GBP, and HKD.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hard-coded sample exchange rates may be mistaken for current financial data.

Mitigation: Use the skill only for informal reference unless it is changed to fetch rates from a trusted provider and clearly show the provider timestamp.

Risk: Outputs are not suitable for payments, accounting, remittances, or financial decisions.

Mitigation: Route those workflows to verified financial systems or review the results against an authoritative exchange-rate source before use.

Risk: Broad Chinese activation keywords may trigger the skill in ordinary currency-related conversations.

Mitigation: Deploy it only where a Chinese currency-conversion helper is intended, and review activation keywords before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangjingzhi07/skills/currency-converter-zh)
- [ClawHub publisher profile](https://clawhub.ai/user/huangjingzhi07)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text responses in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Currency values are derived from hard-coded sample rates in the artifact.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
