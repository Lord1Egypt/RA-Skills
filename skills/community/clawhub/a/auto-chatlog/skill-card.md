## Description: <br>
Automatically archives key conversation information to daily memory files and loads recent memory context at session start for cross-session recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hahaerer](https://clawhub.ai/user/hahaerer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to persist conversation notes, preferences, task results, configuration changes, and todos across sessions through MEMORY.md and daily memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically persists and reloads conversation history, which can retain sensitive personal or business details. <br>
Mitigation: Install only when persistent chat memory is intended, avoid sharing confidential details while active, and regularly inspect or delete MEMORY.md and memory/YYYY-MM-DD.md files. <br>
Risk: The release evidence flags unsafe credential-memory instructions. <br>
Mitigation: Do not store passwords, API keys, tokens, session cookies, or credential values in memory files; fix credential-retention language before sensitive use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hahaerer/auto-chatlog) <br>
- [Publisher profile](https://clawhub.ai/user/hahaerer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown memory files with optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates MEMORY.md and memory/YYYY-MM-DD.md in the configured workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
