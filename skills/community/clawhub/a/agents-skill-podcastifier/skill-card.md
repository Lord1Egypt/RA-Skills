## Description: <br>
Turn incoming text (email/newsletter) into a short TTS podcast with chunking + ffmpeg concat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cerbug45](https://clawhub.ai/user/cerbug45) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill to convert email or newsletter text into a short podcast-style MP3 workflow with chunked TTS generation and ffmpeg concatenation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email or newsletter input may contain confidential text, and future external TTS or messaging integrations could expose that content. <br>
Mitigation: Review any added provider or delivery integration and its data handling before submitting sensitive text. <br>
Risk: The script writes an MP3 to the output path supplied by the user. <br>
Mitigation: Choose output paths deliberately and review paths before running the command. <br>


## Reference(s): <br>
- [Podcastifier ClawHub listing](https://clawhub.ai/cerbug45/agents-skill-podcastifier) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and an MP3 output file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and ffmpeg; writes the generated MP3 to the user-provided output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
