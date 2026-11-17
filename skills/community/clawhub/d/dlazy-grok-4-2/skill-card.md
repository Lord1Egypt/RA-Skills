## Description:

Efficient text generation, dialogue QA, and logical reasoning using the Grok 4.2 text model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can use the skill to send prompts to dLazy for text generation, dialogue question answering, and logical reasoning. It requires a dLazy API key and returns generated content through the hosted API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be sent to dLazy for inference, and using the service may incur charges.

Mitigation: Invoke the skill only for requests you intend to send to dLazy, avoid including sensitive material unless approved, and review applicable service terms and charges.

Risk: Broad triggers may route ordinary text or chat requests through the external provider; the security scan was partial and did not establish the documented model features through the reported login operation.

Mitigation: Confirm each invocation is intended for dLazy and check the CLI's available command and response for the capability you need.

Risk: Authentication requires a dLazy API key, which the CLI can save in local user configuration.

Mitigation: Review the CLI before installation, protect the local configuration and key, and rotate or revoke the key if it may have been exposed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-grok-4-2)
- [dLazy homepage](https://dlazy.com)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON API response containing generated content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-driven; the API supports synchronous and asynchronous task responses.]

## Skill Version(s):

1.3.41 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
