## Description:

Connects to a live voice session, receiving and sending messages in real time via a WebSocket interface using the bundled client script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niczy](https://clawhub.ai/user/niczy)

### License/Terms of Use:


## Use Case:

Developers and operators use ClawVoice to connect an agent to a live voice session, send and receive transcribed messages, and optionally bridge messages to the main OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A WebSocket endpoint can supply messages that are forwarded to the main agent and can receive the agent's full output.

Mitigation: Use only trusted voice servers, avoid remote or shared endpoints unless transport and peer trust are handled externally, and run agent mode with a timeout and limited agent profile.

Risk: Voice messages and agent replies travel through the WebSocket session.

Mitigation: Do not send sensitive content unless the session endpoint and transport are trusted for that data.

## Reference(s):

- [ClawVoice Skill Page](https://clawhub.ai/niczy/skills/claw-voice)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON message examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled client can print JSON messages and stream JSON lines from a WebSocket session.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
