## Description: <br>
Encode or decode strings to and from Base64 format upon user request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xianghuan233-lang](https://clawhub.ai/user/xianghuan233-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to convert plain text to Base64 or decode Base64 strings back to readable text during routine encoding and decoding tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Base64 output may be mistaken for encrypted or protected data. <br>
Mitigation: Treat Base64 as reversible encoding and do not rely on it to protect sensitive information. <br>
Risk: Sensitive text may be visible to the agent, terminal output, or command history during encoding or decoding. <br>
Mitigation: Avoid processing secrets unless the execution environment and logs are appropriate for sensitive data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xianghuan233-lang/base64-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Base64 is an encoding format, not encryption.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
