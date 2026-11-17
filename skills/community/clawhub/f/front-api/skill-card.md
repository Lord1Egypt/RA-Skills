## Description:

Helps agents manage Front conversations, messages, contacts, inboxes, and teams through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Customer-support and operations teams use this skill to look up and manage Front communications, contacts, and team resources. With approval, they can also set up Maton-hosted functions and triggers for related workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Front access may expose or change shared customer communications and contact data.

Mitigation: Use the connected account's least necessary access, start with reads, and confirm each write or new connection with the user.

Risk: Hosted functions, triggers, destinations, and watchers may run ongoing actions or forward event data.

Mitigation: Review their actions, payloads, and destinations and obtain explicit approval before enabling them.

Risk: Raw API keys and broad event payloads can be exposed to unintended recipients.

Mitigation: Prefer CLI OAuth, protect any required API key, and do not forward credentials or broad payloads to third-party hosts without an explicit user request.

## Reference(s):

- [Front skill release](https://clawhub.ai/byungkyu/skills/front-api)
- [Front API reference](https://dev.frontapp.com/reference/introduction)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Text or Markdown with command and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected Front records or instructions for approved automation.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
