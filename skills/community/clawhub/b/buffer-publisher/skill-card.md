## Description:

Publishes or schedules LinkedIn and Twitter/X posts through Buffer's GraphQL API for configured Buffer channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Agents supporting Nissan's social publishing use this skill to publish immediately, queue, or schedule prepared posts on connected LinkedIn and Twitter/X channels through Buffer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected-channels account query retrieves unnecessary email and account data.

Mitigation: Remove or avoid the Get Connected Channels example as written, especially the email field.

Risk: Buffer API bearer tokens and authenticated API responses could be exposed in logs or shared transcripts.

Mitigation: Keep bearer tokens and Buffer API responses out of logs and shared transcripts, and use only the account owner's credential.

Risk: The skill can publish or schedule posts to connected social channels.

Mitigation: Install only for agents that are intended to publish or schedule posts, and review target channel, post text, and schedule before API calls.

## Reference(s):

- [Buffer Publisher on ClawHub](https://clawhub.ai/nissan/skills/buffer-publisher)
- [Publisher profile: nissan](https://clawhub.ai/user/nissan)
- [Buffer GraphQL API endpoint](https://api.buffer.com/graphql)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and bash code blocks, GraphQL payload examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Buffer channel IDs, API endpoint details, scheduling field guidance, and response-checking notes.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
