## Description:

Researches public Fiverr gigs and sellers through Crawlora, including keyword searches, gig pricing and packages, and seller profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

People comparing freelance services use this skill to search Fiverr gigs, compare prices and packages, and review public seller profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, seller names, and gig slugs are sent to Crawlora as a third-party API provider.

Mitigation: Use the skill only when sharing those research inputs with Crawlora is acceptable.

Risk: A disclosed Crawlora API key could allow unauthorized use.

Mitigation: Keep CRAWLORA_API_KEY in the environment and do not share it in prompts or files.

## Reference(s):

- [Fiverr research endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/fiverr-research)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Normalized JSON for gig searches, gig details, and seller profiles; optional text summaries for users]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results support pagination; gig details include package prices and delivery times.]

## Skill Version(s):

1.0.18 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
