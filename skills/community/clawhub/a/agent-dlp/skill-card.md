## Description: <br>
Agent DLP helps agents check inputs, memory, tool use, outputs, and audit logs for prompt-injection and sensitive-data risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caidongyun](https://clawhub.ai/user/caidongyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators can use this skill as DLP-oriented guidance for checking prompt injection, sensitive data exposure, risky tool calls, output filtering, and audit logging in agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release claims DLP enforcement behavior without shipping the referenced implementation files. <br>
Mitigation: Review the package before installing and ask the publisher to provide the missing implementation before relying on the skill for sensitive DLP enforcement. <br>
Risk: The release requests wallet-related access that is not explained by the submitted artifact. <br>
Mitigation: Ask the publisher to explain or remove the wallet capability before using the skill. <br>
Risk: The artifact describes audit logging but does not document log redaction, retention, storage, or protection controls. <br>
Mitigation: Require clear audit-log handling documentation before deploying the skill in workflows that may process sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caidongyun/agent-dlp) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/caidongyun) <br>
- [Submitted skill definition](artifact/SKILL.md) <br>
- [Submitted feature list](artifact/FEATURES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI examples, configuration snippets, and Python usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The submitted artifact describes status checks, input checks, output checks, tool checks, log review, and normal/strict modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
