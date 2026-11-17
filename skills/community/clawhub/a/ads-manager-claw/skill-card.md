## Description:

Manage paid advertising campaigns across Meta (Facebook and Instagram), Google Ads, X, and Snapchat for Indian businesses; the skill analyzes performance, detects issues, and recommends high-ROI actions before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhishekj9621](https://clawhub.ai/user/abhishekj9621)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers, founders, and marketing operators for Indian businesses use this skill to analyze campaign performance, diagnose ROAS, CAC, and funnel issues, and prepare confirmed campaign changes across Meta, Google Ads, X, and Snapchat.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: The skill asks for sensitive ad-platform credentials and can support write-level advertising actions.

Mitigation: Use secure OAuth or a secret store instead of pasting tokens or client secrets into chat; prefer read-only credentials for reporting workflows.

Risk: Campaign, budget, deletion, audience, or posting changes could affect live spend or public content.

Mitigation: Require explicit user confirmation before budget changes, activation, deletion, audience uploads, or posting content.

Risk: Performance guidance could be misleading if platform ROAS omits return, tracking, or funnel data.

Mitigation: Review recommendations against current business metrics such as CAC, LTV, payback period, return rate, and conversion tracking health.

## Reference(s):

- [Credential Guides](references/credential-guides.md)
- [Google Ads API Reference](references/google-ads.md)
- [Meta Ads API Reference](references/meta.md)
- [Snapchat Ads API Reference](references/snapchat.md)
- [X Ads API Reference](references/x-ads.md)
- [ClawHub skill page](https://clawhub.ai/abhishekj9621/skills/ads-manager-claw)
- [ClawHub publisher profile](https://clawhub.ai/user/abhishekj9621)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with analysis, recommendations, API request examples, and confirmation-gated action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Campaign changes should be treated as proposals until the user explicitly confirms execution.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
