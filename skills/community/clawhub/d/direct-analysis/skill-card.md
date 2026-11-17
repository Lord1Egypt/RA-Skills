## Description:

Analyzes Yandex Direct advertising campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimblemarketingapex-netizen](https://clawhub.ai/user/nimblemarketingapex-netizen)

### License/Terms of Use:


## Use Case:

Marketing operators and advertising analysts use this skill to review Yandex Direct campaign performance, including CTR, CPC, spend, conversions, weak ads, and keyword issues. It produces concise optimization recommendations for bids, budgets, ad text, calls to action, and audience segments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad advertising-related trigger words could cause unnecessary Yandex Direct account-data access.

Mitigation: Invoke the skill only for explicit Yandex Direct campaign-analysis requests and confirm intent before using YANDEX_TOKEN and CLIENT_LOGIN.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nimblemarketingapex-netizen/skills/direct-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text campaign analysis with concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference YANDEX_TOKEN and CLIENT_LOGIN when campaign statistics are needed.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
