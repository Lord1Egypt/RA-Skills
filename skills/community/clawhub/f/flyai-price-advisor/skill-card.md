## Description:

历史价格参谋 helps users decide whether to book or wait by combining FlyAI travel price searches with pricing-pattern analysis to assess flight and hotel price levels, compare nearby dates, predict likely trends, and give a buy-or-wait recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hello-ahang](https://clawhub.ai/user/hello-ahang)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users and travel-planning agents use this skill to evaluate whether current flight or hotel prices are favorable and whether they should book immediately or wait. It is intended for price-level assessment, nearby-date comparison, trend reasoning, and concise booking guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact documents global CLI installation and an elevated sudo fallback.

Mitigation: Review before installing, avoid sudo installs, and prefer a scoped or user-managed Node environment with a trusted FlyAI CLI version.

Risk: The artifact documents disabling TLS certificate verification for SSL failures.

Mitigation: Resolve certificate or network trust issues directly and do not run FlyAI commands with TLS verification disabled.

Risk: Search results can include booking URLs returned by external travel services.

Mitigation: Treat booking links as untrusted until the destination is visible, verified, and acceptable to the user.

Risk: Optional saved travel profiles can contain personal travel preferences, family details, budget ranges, and history.

Mitigation: Enable profile storage only with user consent, keep storage scoped, and provide clear deletion or update controls.

## Reference(s):

- [Workflow](reference/workflow.md)
- [Flight Search Reference](reference/search-flight.md)
- [Hotel Search Reference](reference/search-hotel.md)
- [Marriott Hotel Search Reference](reference/search-marriott-hotel.md)
- [Marriott Package Search Reference](reference/search-marriott-package.md)
- [POI Search Reference](reference/search-poi.md)
- [Train Search Reference](reference/search-train.md)
- [AI Search Reference](reference/ai-search.md)
- [Keyword Search Reference](reference/keyword-search.md)
- [User Profile Storage](reference/user-profile-storage.md)
- [Examples](reference/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown price assessment with FlyAI command usage, trend rationale, confidence level, and booking links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user preference notes, price comparisons, confidence estimates, and booking URLs returned by travel search results.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
