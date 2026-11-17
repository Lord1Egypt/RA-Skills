## Description:

API-Station helps agents quickly find and use 302+ AI APIs across chat, image, video, audio, Midjourney, and related categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qb-chen](https://clawhub.ai/user/qb-chen)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to choose endpoints, construct API calls, manage bearer-token authentication, and follow async polling patterns for the API-Station service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local image uploads may expose private or sensitive media to an external image-hosting service.

Mitigation: Use non-sensitive files only, confirm the exact file path before upload, and prefer already-public image URLs when appropriate.

Risk: Bearer tokens used for paid API access may be sent to a separate image-hosting domain.

Mitigation: Use a scoped or disposable token where possible and avoid sending a primary account token to the image-hosting domain unless the provider documents that this is intended and safely scoped.

## Reference(s):

- [API-Station Skill Page](https://clawhub.ai/qb-chen/skills/ai-api-transit-station)
- [Winfull API Documentation](https://winfull.apifox.cn/)
- [API-Station Console and Token Management](https://api.winfull.cloud-ip.cc/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with Python and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint paths, bearer-token headers, request payloads, polling steps, and generated media URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
