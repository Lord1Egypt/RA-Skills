## Description:

Generates speech with Microsoft Edge TTS and sends the resulting audio message to a configured Feishu chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anightmare2](https://clawhub.ai/user/anightmare2)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to generate spoken messages from text and deliver them into Feishu chats. It supports voice selection, rate and pitch adjustment, local audio output, and optional sending through Feishu app credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app credentials are required for sending audio messages and could be exposed through shared shell history or committed configuration.

Mitigation: Use a low-privilege Feishu app and avoid putting secrets in shared shell history or committed files.

Risk: Provided text and generated audio are sent through Edge TTS and Feishu when message delivery is enabled.

Mitigation: Install only when that data flow is acceptable for the intended content and chat recipients.

Risk: The edge-tts dependency is installed from the Python environment used by the operator.

Mitigation: Prefer a virtual environment or pinned dependency install for edge-tts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anightmare2/skills/feishu-edge-tts)
- [Publisher profile](https://clawhub.ai/user/anightmare2)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and generated audio file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate local audio only or upload and send the audio through Feishu when credentials are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata, clawhub.yaml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
