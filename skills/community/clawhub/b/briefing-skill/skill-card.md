## Description: <br>
Automatically track creator channels and transcribe new videos from YouTube, Bilibili, and TikTok while using memory-based updates to skip already processed items and avoid duplicate downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YutaiGu](https://clawhub.ai/user/YutaiGu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run and manage the briefing CLI for tracking creator channels, updating tracked sources, and returning newly generated video transcription text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically run shell setup that fetches remote code, installs dependencies, and changes the local environment. <br>
Mitigation: Review the installer, repository, and requirements before use, and prefer running setup manually in a sandbox or disposable environment. <br>
Risk: The bundled installer may use privileged or global install paths and persistently modify PATH configuration. <br>
Mitigation: Avoid privileged or global install paths unless explicitly intended, and inspect shell profile changes after installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YutaiGu/briefing-skill) <br>
- [Installer repository used by bundled install script](https://github.com/YutaiGu/skill-briefing.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text with CLI command invocations and extracted transcript content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads output/<filename>/whisper.txt after CLI runs that report completed Whisper output.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
