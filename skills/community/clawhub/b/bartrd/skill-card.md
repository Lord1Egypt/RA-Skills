## Description:

Bartrd helps university students trade skills using credits instead of cash.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xploreicon](https://clawhub.ai/user/xploreicon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and student-facing agents use this skill to search skill trades, post offers or requests, accept confirmed matches, check credit balances, and request credit-priced AI services through Bartrd.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posting trades, accepting matches, and requesting AI services can change account state or spend credits.

Mitigation: Show the user the planned action or credit cost and require explicit confirmation before proceeding.

Risk: The skill requires a Bartrd API key that can access the user's Bartrd account.

Mitigation: Install only with a Bartrd account, keep BARTRD_API_KEY in the agent configuration, and avoid exposing it in prompts or outputs.

Risk: Credit operations are final according to the skill instructions.

Mitigation: Review trade posts, match acceptances, and AI service requests carefully before confirmation.

## Reference(s):

- [Bartrd website](https://getbartrd.com)
- [Bartrd API base URL](https://getbartrd.com/api/v1)
- [ClawHub skill page](https://clawhub.ai/xploreicon/skills/bartrd)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown summaries with API-derived values, confirmation prompts, and generated text or code when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BARTRD_API_KEY; trade-changing and credit-spending actions require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
