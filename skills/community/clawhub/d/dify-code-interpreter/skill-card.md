## Description: <br>
Explains code snippets in multiple programming languages through a Dify chatflow and returns structured notes on syntax, logic, purpose, and implementation details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangwp1](https://clawhub.ai/user/zhangwp1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to submit code snippets and receive structured explanations while reviewing, learning, or documenting code across languages such as C, Vue, Python, and Java. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes a live-looking Dify API key as a documented default value. <br>
Mitigation: Replace the key with a trusted credential before installation, and rotate or revoke the exposed key. <br>
Risk: Submitted code may be sent to the configured Dify deployment. <br>
Mitigation: Avoid submitting proprietary code or secrets unless the Dify deployment and its retention and access controls are trusted. <br>
Risk: The release evidence says core code and configuration files were removed, so the artifact may be documentation-only. <br>
Mitigation: Verify the required runtime files and Dify integration before relying on this release for agent execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangwp1/dify-code-interpreter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown or text explanation of submitted code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a code snippet plus trusted Dify endpoint and API key configuration; output depends on the configured Dify chatflow and model.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
