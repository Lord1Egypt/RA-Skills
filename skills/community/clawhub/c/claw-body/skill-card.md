## Description: <br>
Claw Body gives an OpenClaw agent a real-time NuwaAI avatar with voice chat, lip-synced video, and presentation narration for PPT/PDF slides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianglingling007](https://clawhub.ai/user/jianglingling007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to interact with an OpenClaw agent through a browser-based digital avatar, including voice conversation and narrated presentation playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local server exposes unauthenticated APIs while it is running. <br>
Mitigation: Run the server only when needed, keep it bound to local use, and close it when the avatar session is finished. <br>
Risk: The workflow can use NuwaAI credentials and microphone audio. <br>
Mitigation: Use only trusted NuwaAI accounts, avoid high-value credentials, and confirm microphone use is acceptable before starting a session. <br>
Risk: Uploaded presentations may be parsed and used for narration. <br>
Mitigation: Do not upload confidential presentations unless their contents may be processed for narration. <br>
Risk: The server can proxy requests to the local OpenClaw agent. <br>
Mitigation: Use this skill only with a trusted local OpenClaw agent and review the enabled Gateway chat endpoint before use. <br>


## Reference(s): <br>
- [Claw Body release page](https://clawhub.ai/jianglingling007/claw-body) <br>
- [NuwaAI](https://nuwaai.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and presentation control tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Starts a local browser interface for voice, avatar, chat, and presentation workflows.] <br>

## Skill Version(s): <br>
1.0.10 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
