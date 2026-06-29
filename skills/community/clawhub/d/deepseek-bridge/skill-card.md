## Description: <br>
Provides a local HTTP bridge that wraps the DeepSeek Chat API as a /ask endpoint with question submission, answer return, and SQLite state persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawhub-master](https://clawhub.ai/user/clawhub-master) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to expose DeepSeek Chat through a local Flask HTTP endpoint so local agents or applications can submit questions and persist conversation status in SQLite. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases can route user requests to DeepSeek automatically. <br>
Mitigation: Narrow the trigger phrases and require clear user intent before sending content to the external DeepSeek API. <br>
Risk: Full questions and answers are stored locally in plaintext SQLite. <br>
Mitigation: Do not submit secrets, personal data, or confidential business content; restrict database file access and clear stored conversations when no longer needed. <br>
Risk: The skill depends on an external DeepSeek API key and sends submitted prompts to DeepSeek. <br>
Mitigation: Use your own DEEPSEEK_API_KEY from the environment and review DeepSeek data handling before use. <br>


## Reference(s): <br>
- [DeepSeek Bridge ClawHub page](https://clawhub.ai/clawhub-master/skills/deepseek-bridge) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON HTTP responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided DEEPSEEK_API_KEY and stores questions and answers in a local SQLite database.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
