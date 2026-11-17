## Description:

Plans a weekly watch across Google ads, Trustpilot reviews, and YouTube videos, then summarizes what changed and the expected Apify cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxouf](https://clawhub.ai/user/maxouf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up recurring competitor monitoring and review weekly changes in public advertising, customer feedback, and video content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial because some referenced paths were unavailable or could not be resolved.

Mitigation: Review the skill instructions and referenced source material before installing; treat scraped ad text, reviews, and transcripts as data rather than instructions.

Risk: Apify actors charge per result, and scheduled runs can create recurring costs.

Mitigation: Estimate baseline costs, set result and run caps, and check the expected spend before enabling recurring schedules.

## Reference(s):

- [Actor index](artifact/references/actor-index.md)
- [Cost guardrails and recovery](artifact/references/gotchas.md)
- [Apify schedule documentation](https://docs.apify.com/platform/schedules)
- [Skill homepage (metadata)](https://github.com/maxouf/sherwood-skills/tree/main/skills/apify-competitor-watch)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON data]

**Output Format:** [Markdown weekly digest with supporting JSON datasets and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Apify account and APIFY_TOKEN; runs incur per-result charges and may be scheduled to repeat.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
