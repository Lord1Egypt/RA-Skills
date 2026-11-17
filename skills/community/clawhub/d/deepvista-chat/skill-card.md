## Description:

DeepVista Chat: Send messages to the AI agent and manage chat sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingconan](https://clawhub.ai/user/jingconan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to interact with the DeepVista AI agent from the CLI, manage chat sessions, and stream assistant responses. The skill also documents when chat commands can create or modify remote session state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user messages to a remote DeepVista agent that may search, use tools, or create cards.

Mitigation: Confirm before using +send and avoid sending sensitive information unless remote DeepVista processing is intended.

Risk: The delete command removes chat sessions.

Mitigation: Confirm the target chat session with the user before executing destructive delete actions.

Risk: The skill depends on the deepvista-cli package and DeepVista service behavior.

Mitigation: Install only from trusted DeepVista package sources and review the CLI source or package metadata before deployment.

## Reference(s):

- [DeepVista CLI homepage](https://cli.deepvista.ai)
- [Deepvista Chat on ClawHub](https://clawhub.ai/jingconan/skills/deepvista-chat)
- [Publisher profile](https://clawhub.ai/user/jingconan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI command examples and streamed NDJSON response details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents read-only session commands plus user-confirmed delete and send actions. The send command streams one JSON object per line as the remote agent responds.]

## Skill Version(s):

0.1.0-alpha.21 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
