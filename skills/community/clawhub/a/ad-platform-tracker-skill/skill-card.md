## Description:

Tracks and analyzes advertising platform changes across Meta, Google Ads, privacy compliance, and competitor intelligence so agents can produce timely campaign guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhishekj9621](https://clawhub.ai/user/abhishekj9621)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, growth teams, and agent developers use this skill to assess Meta and Google Ads platform changes, policy shifts, compliance requirements, and competitor activity, then generate campaign impact assessments, update digests, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live competitor monitoring may involve third-party scraping or automation services that can conflict with platform terms or applicable law.

Mitigation: Prefer official APIs and transparency tools, confirm platform terms and legal requirements before monitoring, and limit collection to permitted public or authorized data.

Risk: Advertising platform policy and compliance claims are time-sensitive, and the bundled static notes are dated early 2026.

Mitigation: Verify high-impact recommendations against current official Meta, Google, and regulatory sources before changing campaigns or compliance posture.

Risk: Monitoring workflows can expose API tokens or advertising account data if credentials are mishandled.

Mitigation: Store credentials in approved secret management, avoid pasting tokens into prompts or logs, and scope API access to the minimum required permissions.

## Reference(s):

- [Meta Algorithm & Policy Tracker](references/meta-tracker.md)
- [Google Ads Algorithm & Policy Tracker](references/google-tracker.md)
- [Regulatory & Compliance Tracker](references/compliance-tracker.md)
- [Competitive Intelligence Tracker](references/competitive-tracker.md)
- [Meta for Business News](https://www.facebook.com/business/news)
- [Meta Transparency Center](https://transparency.fb.com/)
- [Meta Ads Library](https://www.facebook.com/ads/library)
- [Meta Graph API Changelog](https://developers.facebook.com/docs/graph-api/changelog)
- [Google Ads Blog](https://blog.google/products/ads-commerce/)
- [Google Ads Help Center](https://support.google.com/google-ads)
- [Google Ads Developer Blog](https://ads-developers.googleblog.com/)
- [Meta Ads Library API](https://www.facebook.com/ads/library/api/)
- [Google Ads Transparency Center](https://adstransparency.google.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured templates and optional code or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include daily update digests, campaign impact assessments, compliance alerts, competitor analysis, API examples, and monitoring recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
