## Description:

Automatically searches for free API providers matching a requested capability and returns a concise report of candidate APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryyehai](https://clawhub.ai/user/terryyehai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical operators use API Hunter to find free or no-signup API providers for a capability such as weather, translation, market data, or image generation. It is best suited for initial discovery and comparison before validating provider terms and availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs outbound web requests and uses a localhost search service.

Mitigation: Run it only where outbound network access and localhost search use are approved, and avoid passing untrusted or internal URLs to dashboard checks.

Risk: Search results may be stale, incomplete, or misleading about free tiers and no-signup availability.

Mitigation: Verify provider documentation, pricing, registration requirements, and terms before relying on a recommended API.

Risk: Dependency drift or unused dependencies can increase maintenance and review burden.

Mitigation: Pin dependencies for deployment and remove unused beautifulsoup4 if it is not needed.

## Reference(s):

- [API Hunter on ClawHub](https://clawhub.ai/terryyehai/skills/api-hunter)
- [Public APIs collection](https://github.com/public-apis/public-apis)
- [Puter.js developer documentation](https://developer.puter.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with inline tables, terminal text, and Python string return values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live search depends on an approved localhost search service and outbound web requests.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
