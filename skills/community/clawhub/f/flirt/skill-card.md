## Description: <br>
Sends scheduled romantic text and cloned-voice messages to Feishu and QQ using a configurable phrase library, timing rules, and probability controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[william1hall](https://clawhub.ai/user/william1hall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers configuring OpenClaw messaging workflows use this skill to automate scheduled romantic messages and voice clips for Feishu and QQ recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill combines scheduled outbound messaging with account credentials. <br>
Mitigation: Review before installing, use a dedicated low-privilege Feishu app, and avoid placing secrets directly in the script where possible. <br>
Risk: The skill uses voice-cloning reference audio. <br>
Mitigation: Only use voice samples with clear consent and confirm how the Noiz TTS provider handles reference audio. <br>
Risk: The skill stores state, generated audio, credentials, and reference voice data with limited cleanup guidance. <br>
Mitigation: Add local cleanup steps for cron entries, credentials, state files, generated audio, and stored reference voice files. <br>


## Reference(s): <br>
- [hello-honey on ClawHub](https://clawhub.ai/william1hall/flirt) <br>
- [flirt_library.txt](references/flirt_library.txt) <br>
- [Noiz TTS skill repository](https://github.com/noizai/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scheduled Feishu and QQ text or audio message behavior after local configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
