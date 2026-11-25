## Description:

Helps developers integrate Didit Database Validation to check identity data against government and authoritative registries across 45 countries and receive per-field match results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and backend engineers use this skill to build API-key integrations that check identity details against country-specific government and authoritative registries. It helps select services, prepare requests, and interpret per-field match results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registry checks can send sensitive identity details, address data, and, for biometric services, selfie images to Didit and registry providers; API requests are saved as sessions by default, and the utility prints the response.

Mitigation: Send only fields required by the selected service, obtain required consent, use --no-save when the result should not be stored as a session, and treat printed responses as sensitive.

Risk: The skill requires a DIDIT_API_KEY and network access; the security evidence says scan coverage was partial and tool-misuse analysis was degraded.

Mitigation: Review the requested environment and network access, keep the API key in the environment rather than source code, and run the skill in a trusted environment.

## Reference(s):

- [Didit developer documentation](https://docs.didit.me)
- [Database Validation API reference](https://docs.didit.me/standalone-apis/database-validation)
- [Database Validation feature guide](https://docs.didit.me/core-technology/database-validation/overview)
- [Supported countries and services](https://docs.didit.me/core-technology/database-validation/database-validation-supported-countries)
- [Database Validation pricing](https://docs.didit.me/getting-started/database-validation-pricing)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, API calls, Guidance]

**Output Format:** [Markdown with Python and TypeScript examples, REST request fields, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include country and service selection guidance, request and response interpretation, and credential setup instructions.]

## Skill Version(s):

1.4.0 (source: SKILL.md frontmatter; server-resolved release metadata agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
