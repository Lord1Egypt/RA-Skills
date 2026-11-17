## Description:

Compares public App Store privacy labels, Google Play data-safety declarations, and listed Android permissions for selected apps through Crawlora, preserving app identity, source context, and uncertainty.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other app evaluators use this skill to compare public privacy disclosures for a shortlist of iOS and Android apps, while distinguishing platform taxonomies, missing information, and unverified runtime behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: App search terms, identifiers, storefront and language choices, and the API key are sent to Crawlora.

Mitigation: Share only intended app queries, protect the API key, and keep requests within the planned scope and budget.

Risk: Public disclosures and listed permissions may be mistaken for evidence of runtime behavior, compliance, or device safety.

Mitigation: Attribute each statement to its store source, distinguish unknown from absent, and recommend separate runtime verification where needed.

## Reference(s):

- [Skill endpoint reference](artifact/reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/app-privacy-disclosure-comparison)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown comparison matrix with source attribution and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records app identifiers, storefront or language, source and retrieval times, declaration categories, and unknown or unmapped fields.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
