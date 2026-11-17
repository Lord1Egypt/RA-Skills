## Description:

Look up credit card rewards eligibility for merchants by checking MCC codes and card bonus categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gibtang](https://clawhub.ai/user/gibtang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to identify a merchant's MCC and compare credit card rewards eligibility for that merchant. It supports merchant lookup by domain, name search, MCC-based card eligibility checks, and MCC validation for SG and US regions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Merchant names, domains, MCCs, and region selections may be sent to check-mcc.com.

Mitigation: Avoid submitting sensitive merchant context, and disclose external API use before relying on the lookup.

Risk: Default-region documentation is inconsistent between the skill configuration and usage text.

Mitigation: Ask the user to specify SG or US explicitly until the default-region documentation is corrected.

Risk: Rewards output may be incomplete or change over time.

Mitigation: Treat card eligibility and rewards details as guidance, and verify important financial decisions with card issuer terms.

## Reference(s):

- [CheckMCC Skill Page](https://clawhub.ai/gibtang/skills/check-mcc)
- [CheckMCC API Base URL](https://check-mcc.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with concise merchant, MCC, category, eligibility, reward, cap, and condition details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include eligible and ineligible card lists, clarification prompts for ambiguous merchants, and error guidance when lookups fail.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
