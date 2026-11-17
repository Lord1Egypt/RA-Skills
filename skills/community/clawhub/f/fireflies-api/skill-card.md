## Description:

Connects an agent to Fireflies.ai to retrieve meeting transcripts and summaries, analyze conversations, and manage recordings through a user-authorized connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use the skill to find and analyze meeting conversations, retrieve transcripts and summaries, and manage recordings with their authorized Fireflies account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting transcripts and recordings may contain sensitive business or personal information.

Mitigation: Limit retrieval and sharing to what the user requests, and treat meeting content as sensitive.

Risk: Writes or new automations may change meeting data or run repeatedly.

Mitigation: Confirm each write and automation setup with the user before proceeding.

Risk: Third-party trigger destinations can forward data persistently.

Mitigation: Review the destination and forwarded fields with the user; avoid unapproved external destinations and revoke unused functions or connections.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/byungkyu/skills/fireflies-api)
- [Fireflies GraphQL API Reference](https://docs.fireflies.ai/graphql-api)
- [Maton homepage](https://maton.ai)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton API Reference](https://docs.maton.ai/api-reference/overview)
- [Scheduled trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Plain text or Markdown with JSON, code, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Meeting content is accessible only through the user's authorized connection.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
