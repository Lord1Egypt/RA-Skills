## Description:

Analyzes Android APKs through the Crawlora API, returning JSON for static analysis, version diffs, timelines, and ownership-signal comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, mobile security engineers, and researchers use this skill to inspect authorized Android packages and compare app versions or ownership signals through Crawlora static analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitting an APK or URL without authorization could expose private app material to Crawlora.

Mitigation: Submit only packages and URLs you are authorized to share, especially when analyzing private apps.

Risk: Deleting an analysis job purges its stored metadata and results.

Mitigation: Save any needed results before requesting job deletion.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [Crawlora API](https://api.crawlora.net/api/v1)
- [Crawlora website](https://crawlora.net)
- [ClawHub skill page](https://clawhub.ai/crawlora-org/skills/apk-teardown-research)

## Skill Output:

**Output Type(s):** [Analysis, JSON]

**Output Format:** [Normalized JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static APK analysis and comparisons, including manifest, permissions, signing, SDK, and release-history signals when available.]

## Skill Version(s):

1.0.12 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
