## Description:

Facebook ad copywriting assistant that generates six high-conversion ad variants with A/B testing recommendations and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chungvic](https://clawhub.ai/user/chungvic)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, agencies, and small businesses use this skill to generate Cantonese Facebook ad copy variants, A/B testing ideas, audience segments, and launch guidance for campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An embedded API credential and external-service calls may expose client, budget, or campaign data to third-party services.

Mitigation: Remove and rotate the embedded GLM key, require explicit user-provided credentials, and avoid confidential data unless third-party processing is acceptable.

Risk: Email and Telegram delivery can transmit generated content or questionnaire data outside the local environment.

Mitigation: Use those channels only when intentionally configured, add a pre-send privacy confirmation, and mask troubleshooting output.

Risk: Questionnaire file handling has weak scoping.

Mitigation: Restrict questionnaire inputs to a safe directory before processing client data.

Risk: Unpinned dependencies can change behavior across installs.

Mitigation: Pin dependency versions and review updates before release.

## Reference(s):

- [API Documentation](artifact/references/api-docs.md)
- [Example Copy Library](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown delivery package with optional JSON-style generated content and notification text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces six ad variants, A/B test guidance, audience analysis, campaign recommendations, and optional delivery notifications.]

## Skill Version(s):

2.1.0 (source: server release, frontmatter, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
