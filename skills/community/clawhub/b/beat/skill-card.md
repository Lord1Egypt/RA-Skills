## Description: <br>
Beat is advertised as a command-line tool for tracking, analyzing, and managing music and audio activity, while server security evidence notes that the included script mainly stores user-entered command text in local logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents can use Beat to run a local command-line activity logger for audio-oriented workflows, inspect recent entries, view simple statistics, search saved entries, and export local records. Because server security evidence flags the release as suspicious, users should validate its behavior before relying on it as an audio management tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as a music/audio management tool, but server security evidence says the script mainly logs command text entered by the user. <br>
Mitigation: Review it as a local activity logger and validate behavior before relying on it for audio processing or metadata management. <br>
Risk: Local logs may capture sensitive command text, private paths, unreleased project names, or other metadata. <br>
Mitigation: Avoid entering secrets or sensitive metadata, and inspect or clear ~/.local/share/beat after testing. <br>


## Reference(s): <br>
- [Beat on ClawHub](https://clawhub.ai/bytesagain3/beat) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text terminal output with optional JSON, CSV, or text export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores command activity under ~/.local/share/beat when executed.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
