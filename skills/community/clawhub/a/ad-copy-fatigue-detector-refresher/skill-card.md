## Description:

Detect ad copy fatigue and auto-suggest micro-pivot refreshes by analyzing CTR/CPC degradation across Facebook, Google, and LinkedIn campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, growth operators, and developers use this skill to monitor paid advertising copy fatigue across Facebook, Google Ads, and LinkedIn, then generate refresh suggestions and setup guidance for tests or alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad ad-platform access can expose campaign, audience, and performance data beyond what fatigue analysis requires.

Mitigation: Grant the narrowest available read-only scopes for Facebook, Google Ads, and LinkedIn unless a reviewed workflow specifically needs write access.

Risk: Automated Zapier or ad-platform workflows could create or change live ads before a human reviews the proposed copy.

Mitigation: Require manual approval before any workflow launches variants, changes budgets, edits campaigns, or starts A/B tests.

Risk: Slack or email alerts may share sensitive campaign performance details with unintended recipients.

Mitigation: Send alerts only to approved private channels or distribution lists and avoid including unnecessary account identifiers.

Risk: Generated copy suggestions and estimated lift values may be inaccurate or misleading.

Mitigation: Review suggestions against brand, legal, and platform policy requirements before testing them in live campaigns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/ad-copy-fatigue-detector-refresher)
- [Publisher profile](https://clawhub.ai/user/ncreighton)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-style analysis reports with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ad fatigue scores, CTR and CPC trends, copy refresh suggestions, alert setup guidance, and A/B test recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
