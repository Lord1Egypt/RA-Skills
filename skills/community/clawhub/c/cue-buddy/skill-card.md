## Description: <br>
Cue Buddy helps business users author, validate, debug, test, tune, and manage reusable Cue research templates for recurring public-data finance, compliance, and business research scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users and analysts use this skill to turn recurring public-data research workflows into Cue buddy templates, validate the template fields, submit or update templates in their Cue account, and optionally run paid tests after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Cue API key and can create or modify templates in the user's Cue account. <br>
Mitigation: Use a scoped or revocable Cue key where possible, review generated template changes before write operations, and rotate the key if it is accidentally pasted into chat. <br>
Risk: Test and tune flows can consume Cue credits. <br>
Mitigation: Run paid tests or tuning only after explicit user confirmation and review the expected credit cost before proceeding. <br>
Risk: The security summary flags under-disclosed local file upload capability and cautions against confidential local documents. <br>
Mitigation: Do not use confidential local files unless the file-upload helper is removed or disabled and the agent behavior is verified to keep reference materials local. <br>
Risk: The security guidance notes occasional GitHub update checks. <br>
Mitigation: Review or disable update-check behavior in restricted environments and inspect skill updates before applying them. <br>


## Reference(s): <br>
- [Cue Buddy ClawHub Release](https://clawhub.ai/wangxiaoxu/skills/cue-buddy) <br>
- [Cue Platform](https://cuecue.cn) <br>
- [Cue API Key Page](https://cuecue.cn/api-key) <br>
- [Cue API Base](https://cuecue.cn/api) <br>
- [Template Fields Specification](references/template-fields-spec.md) <br>
- [Hard Rules](references/hard-rules.md) <br>
- [Materials Intake Rules](references/materials-intake.md) <br>
- [Gemini CLI Verification Report](docs/verification-reports/2026-05-20-gemini-cli.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON template payloads, shell commands, and validation or test results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Cue APIs with a user-provided API key, create or update Cue templates, and run credit-consuming tests only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact metadata.version is 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
