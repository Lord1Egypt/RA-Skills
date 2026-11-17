## Description:

Query and interact with company knowledge bases or workflows using the Dify API with multi-turn context and streaming response support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whswhs1128](https://clawhub.ai/user/whswhs1128)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and employees use this skill to query internal Dify-backed knowledge bases, continue conversations with conversation IDs, or execute configured Dify workflows from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships a hardcoded Dify API key that could expose or authorize unintended access if used as packaged.

Mitigation: Rotate or revoke the packaged credential and require a user-provided secret through environment configuration before use.

Risk: The default Dify endpoint uses HTTP and can transmit credentials, internal queries, and conversation IDs without transport encryption.

Mitigation: Configure an HTTPS Dify endpoint before sending real internal queries or conversation context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whswhs1128/skills/dify-flow-access)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and Dify API response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports blocking or streaming responses and may return a conversation ID for follow-up turns.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact version information)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
