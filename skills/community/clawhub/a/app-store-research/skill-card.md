## Description:

Researches public app and browser-extension listings across the Apple App Store, Google Play, and Chrome Web Store using the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to discover and compare public apps and extensions, including listings, ratings, reviews, permissions, privacy disclosures, rankings, and release history across stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: App identifiers, search terms, review requests, locale choices, and the API key are sent to a third-party provider.

Mitigation: Use Crawlora only when its data handling meets your privacy expectations; avoid sensitive internal research targets and keep the API key private.

Risk: Public review samples and store disclosures may be mistaken for representative sentiment or an independent security assessment.

Mitigation: Preserve store, locale, and review-sample context; treat permissions and privacy disclosures as claims in public listings.

## Reference(s):

- [Endpoint reference](artifact/reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [App Store Research on ClawHub](https://clawhub.ai/crawlora-org/skills/app-store-research)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Markdown research summaries and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public listings and reviews; results vary by store and locale.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
