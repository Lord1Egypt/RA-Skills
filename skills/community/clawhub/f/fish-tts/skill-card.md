## Description: <br>
Generate high-quality speech from text using Fish Audio S1 and optionally upload the resulting MP3 audio to NextCloud via WebDAV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gtank1](https://clawhub.ai/user/gtank1) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and operators use this skill to generate text-to-speech audio with selectable voices, basic emotion controls, and optional storage in a configured NextCloud folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds a default NextCloud password and fixed service URLs in examples and script defaults. <br>
Mitigation: Replace defaults with scoped credentials and trusted service URLs before execution, and rotate or remove any exposed password. <br>
Risk: Generated audio and input text may be sent to the configured TTS service and stored in NextCloud. <br>
Mitigation: Avoid sensitive text unless the Fish Audio and NextCloud services are controlled and approved for that data. <br>
Risk: The configured upload path may store files in an unintended NextCloud folder. <br>
Mitigation: Confirm the destination URL and folder before running upload commands or scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gtank1/fish-tts) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [SKILL.py](artifact/SKILL.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces audio-generation and upload instructions; referenced scripts may create MP3 files and upload them to NextCloud when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
