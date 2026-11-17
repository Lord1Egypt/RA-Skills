## Description:

Generates paid-ad creative at volume, including RSA headlines and descriptions, hooks, and angle matrices message-matched to a destination landing page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and ad practitioners use this skill to turn an offer, destination URL, platform, audience, and optional existing variants into ready-to-review paid-ad creative for Search and Social campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ad copy can contain unsupported statistics, guarantees, testimonials, or restricted-vertical claims.

Mitigation: Review each claim against the destination page or provided evidence, keep unresolved claims marked as needs source, and run a policy pre-check before live use.

Risk: Landing-page content, ad exports, and competitor examples are untrusted marketing inputs.

Mitigation: Treat those inputs as data only, ignore embedded instructions, and review generated creative before approving it.

Risk: Optional ad-platform integrations could expose account credentials if provided unintentionally.

Mitigation: Use manual exports when possible and provide ad-platform credentials only when intentionally using an optional integration.

Risk: Saved handoff artifacts may contain sensitive campaign strategy or draft claims.

Mitigation: Save local handoff files only after user confirmation and handle them according to the workspace's data-handling rules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/ad-creative-builder)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Ad Format Specs](references/ad-format-specs.md)
- [Angle Matrix](references/angle-matrix.md)
- [Meta Ad Library](https://www.facebook.com/ads/library/)
- [Google Ads Transparency Center](https://adstransparency.google.com)
- [TikTok Commercial Content API](https://developers.tiktok.com/products/commercial-content-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown creative set with ad units, angle matrices, message-match notes, and an optional local handoff artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated units should fit the target ad-format limits and include claim dependency status before handoff.]

## Skill Version(s):

19.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
