## Description: <br>
code2animation helps agents build code-driven animated videos with TTS narration, browser preview, transitions, and MP4 rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etrobot](https://clawhub.ai/user/etrobot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to script HTML/CSS media scenes, generate narration, preview timing, and render portrait or landscape videos. It is suited for code-based promotional videos, product explainers, and other deterministic animated clips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports an unauthenticated audio-generation endpoint that can run shell commands from request input. <br>
Mitigation: Run the skill only in an isolated local workspace, keep the Vite server off exposed networks, and review or disable the endpoint before installation. <br>
Risk: TTS generation sends submitted script text to an external Microsoft Edge TTS service. <br>
Mitigation: Do not submit sensitive scripts or private data unless that external processing is acceptable. <br>
Risk: The package defines a GEMINI_API_KEY environment binding even though basic TTS use does not require secrets. <br>
Mitigation: Avoid providing secrets such as GEMINI_API_KEY unless a reviewed workflow explicitly requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/etrobot/code2animation) <br>
- [Publisher profile](https://clawhub.ai/user/etrobot) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill documentation](artifact/skill.md) <br>
- [Rendering scripts documentation](artifact/scripts/README.md) <br>
- [FFmpeg download reference](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks, JSON project configuration examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead to generated project files, audio timing metadata, and MP4 video artifacts when the documented commands are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
