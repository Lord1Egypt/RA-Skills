## Description: <br>
Generate narrative chronicles of developer work from git history, session transcripts, and memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sssamuelll](https://clawhub.ai/user/sssamuelll) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers use this skill to turn local git history, memory files, and agent session metadata into daily chronicles, weekly recaps, standup notes, or portfolio narratives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gather workflow can read local git history, memory files, and agent session metadata that may include private work details or secrets. <br>
Mitigation: Review and narrow config.json before use, especially projectDirs, memoryDir, and sessionsDir. <br>
Risk: Generated chronicles may include unrelated personal or sensitive development context. <br>
Mitigation: Treat generated output as private until it has been reviewed and redacted. <br>


## Reference(s): <br>
- [Voice Profile Template](references/voice-profile.md) <br>
- [Dev Chronicle on ClawHub](https://clawhub.ai/sssamuelll/dev-chronicle) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown prose with optional shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chronicles may include sensitive local development context and should be reviewed before sharing.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
