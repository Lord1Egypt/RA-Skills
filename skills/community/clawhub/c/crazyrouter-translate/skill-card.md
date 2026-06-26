## Description: <br>
AI-powered translation via Crazyrouter for translating text or files between languages using selectable AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xujfcn](https://clawhub.ai/user/xujfcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to translate text or document files, preserve Markdown formatting when requested, choose source and target languages, and compare output from different supported models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text or files submitted for translation may be sent to Crazyrouter or another endpoint configured with CRAZYROUTER_BASE_URL. <br>
Mitigation: Use the skill only for content approved for that service, and confirm CRAZYROUTER_BASE_URL is unset or points to a trusted endpoint before execution. <br>
Risk: The configured endpoint receives the CRAZYROUTER_API_KEY in the Authorization header. <br>
Mitigation: Use a scoped API key and avoid running the skill with secrets or confidential documents unless that sharing has been approved. <br>


## Reference(s): <br>
- [Crazyrouter](https://crazyrouter.com) <br>
- [Crazyrouter API endpoint](https://crazyrouter.com/v1) <br>
- [ClawHub release page](https://clawhub.ai/xujfcn/crazyrouter-translate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Translated text on stdout or translated file content written to a requested output path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CRAZYROUTER_API_KEY; may use CRAZYROUTER_BASE_URL when configured; default model is gpt-4o-mini.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
