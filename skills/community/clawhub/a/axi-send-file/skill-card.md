## Description: <br>
Convert workspace files into Telegram-downloadable attachments such as PDF or ZIP files for OpenClaw MEDIA delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awalesagar](https://clawhub.ai/user/awalesagar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill when an agent needs to prepare generated or existing workspace files for reliable Telegram download as PDFs, ZIP archives, images, or existing binary files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may prepare or send the wrong workspace file, including sensitive data, if the target path is not checked. <br>
Mitigation: Confirm the exact file path before MEDIA delivery and avoid sending secrets, credentials, or sensitive workspace data unless sharing is intentional. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and MEDIA delivery lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces file-preparation instructions and delivery paths for Telegram-compatible attachments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
