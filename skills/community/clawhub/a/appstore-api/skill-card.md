## Description:

Helps agents search public iOS App Store listings and retrieve app details, ratings, reviews, developer catalogs, and related apps through ReplyNodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[replynodes-ai](https://clawhub.ai/user/replynodes-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other App Store researchers use this skill to find iOS apps and examine public listing details, user feedback, ratings, and comparable apps.

### Deployment Geography for Use:

Global; results depend on the selected App Store storefront.

## Known Risks and Mitigations:

Risk: The packaged SKILL.md checksum does not match the package's checksum listing.

Mitigation: Obtain a fresh package or publisher confirmation before enabling the skill broadly.

Risk: The installation guide refers to an authentication flow absent from the inspected skill.

Mitigation: Configure any ReplyNodes API key manually; do not follow unverified instructions to obtain one.

Risk: App Store lookup terms and an optional workspace key are sent to ReplyNodes.

Mitigation: Use only if the service is acceptable for that data, and send the key only to the ReplyNodes API endpoint.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/replynodes-ai/skills/appstore-api)
- [API endpoints and parameters](artifact/references/endpoints.md)
- [Public API specification](artifact/references/appstore-public-v1.openapi.json)
- [Live access audit and limitations](artifact/references/live-audit.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language answers summarizing structured JSON from public App Store lookups]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; results may be incomplete, storefront-specific, or unavailable.]

## Skill Version(s):

2.1.4 (source: ClawHub release; packaged skill frontmatter says 2.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
