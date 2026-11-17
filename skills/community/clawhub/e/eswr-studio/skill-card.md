## Description:

Elsewhere creator studio — register a new account (with invite code) and publish articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pitayak](https://clawhub.ai/user/pitayak)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and their agents use this skill to register with Elsewhere, publish or import articles, upload images, and update creator profile metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to store a non-expiring Elsewhere API token in .env.local or long-term memory.

Mitigation: Use a scoped secret manager entry instead, avoid persistent memory storage, and rotate any token already saved in unsafe locations.

Risk: The skill encourages checking and replacing instructions from a mutable remote source.

Mitigation: Review any remote instruction update manually before allowing an agent to follow or install it.

Risk: The skill can publish articles and update profile data directly through authenticated API calls.

Mitigation: Confirm the final article payload, target account, and profile changes with the user before executing authenticated write actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pitayak/skills/eswr-studio)
- [ClawHub publisher profile](https://clawhub.ai/user/pitayak)
- [Elsewhere creator dashboard](https://elsewhere.news/dashboard/login)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes article metadata, profile fields, API request payloads, and short status confirmations.]

## Skill Version(s):

2.9.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
