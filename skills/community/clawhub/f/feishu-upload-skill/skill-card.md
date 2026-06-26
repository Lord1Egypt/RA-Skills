## Description: <br>
Uploads local files to Feishu cloud storage and can send the uploaded file to a specified Feishu chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeeWooo](https://clawhub.ai/user/DeeWooo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to upload local artifacts, logs, archives, or other files to Feishu and optionally share them into a target chat from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports bundled Feishu credentials and install-time authentication behavior. <br>
Mitigation: Remove bundled secrets, rotate any exposed Feishu credentials, and use user-controlled secret storage before installation or execution. <br>
Risk: Token values and API responses may be logged by the included scripts. <br>
Mitigation: Disable token and response logging, especially in debug mode, and avoid storing logs that contain access tokens or sensitive Feishu responses. <br>
Risk: Uploaded files are shared with Feishu and, when a chat ID is provided, with the target chat. <br>
Mitigation: Only upload files intended for that disclosure and avoid secrets, private workspace data, memory archives, or regulated data unless sharing is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DeeWooo/feishu-upload-skill) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, API calls] <br>
**Output Format:** [Markdown guidance with shell and Node.js command examples; scripts return console output and JSON status for uploads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, Feishu API access, and valid Feishu app credentials or access tokens; documented file uploads are limited to 30MB.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
