## Description:

Installs and operates the AideNote local connection suite for Hermes so an agent can retrieve AideNote recordings, transcripts, summaries, action items, knowledge bases, account status, and mobile bridge health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajingmiao](https://clawhub.ai/user/ajingmiao)

### License/Terms of Use:

MIT-0

## Use Case:

Hermes users use this skill to connect AideNote and ask an agent to retrieve and summarize their real recordings, transcripts, meeting action items, account status, knowledge bases, and mobile bridge health from AideNote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses private recordings, transcripts, tasks, and knowledge bases.

Mitigation: Install only when the user trusts AideNote and is comfortable granting this access.

Risk: Credential setup can expose a long-lived API key through the local Hermes credential file.

Mitigation: Prefer the app pairing flow, treat local credentials as sensitive, and rotate or remove them when no longer needed.

Risk: The local bridge installs persistent services that keep AideNote connected to the machine.

Mitigation: Use the install flow only with explicit user consent and remove or disable the services when persistent access is no longer appropriate.

Risk: Using HTTP or an unfamiliar API base can weaken the connection security posture.

Mitigation: Use HTTPS and the expected AideNote API base unless the publisher provides verified replacement guidance.

## Reference(s):

- [AideNote API contract](references/api-contract.md)
- [AideNote homepage](https://www.aidenote.cn)
- [ClawHub skill page](https://clawhub.ai/ajingmiao/skills/aidenote-hermes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands and summarized JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return JSON; the agent should summarize results and avoid exposing credentials or configuration files.]

## Skill Version(s):

1.2.9 (source: evidence release and Hermes metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
