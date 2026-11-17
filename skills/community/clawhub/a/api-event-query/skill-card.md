## Description:

Closeli Open Device Event Query lets an agent query Closeli device events with natural language and return an AI summary, event list, event times, scene descriptions, and screenshot or video links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[closeli-open](https://clawhub.ai/user/closeli-open)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and agents use this skill to answer questions about Closeli device events, such as whether a person or vehicle appeared during a date range. The skill is intended for event review workflows that need concise summaries plus links to supporting event media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive device-event data and API credentials through the shared ~/.openclaw/.env configuration file.

Mitigation: Use a least-privilege, revocable API key; restrict ~/.openclaw/.env permissions; and avoid storing unrelated secrets in the shared file.

Risk: A mutable AI_GATEWAY_HOST setting could send event queries or credentials to an unintended gateway.

Mitigation: Confirm AI_GATEWAY_HOST is the intended trusted HTTPS gateway before use.

Risk: Disabling TLS verification can expose API keys and device-event data to interception.

Mitigation: Keep TLS verification enabled in production and do not set AI_GATEWAY_VERIFY_SSL=false except for controlled development environments.

Risk: Passing the API key on the command line can expose it through shell history or process listings.

Mitigation: Prefer the permission-restricted ~/.openclaw/.env configuration path for persistent credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/closeli-open/skills/api-event-query)
- [Publisher profile](https://clawhub.ai/user/closeli-open)
- [Default AI gateway endpoint](https://ai-open.icloseli.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON from the script, with agent-rendered Markdown summaries, tables, and media links for users.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires device IDs, a date range, a natural language query, and an API key; the script trims returned events and records the total event count.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
