## Description: <br>
Send a quick email via SMTP using `msmtp` without opening a full mail client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to draft shell commands and configuration guidance for sending quick SMTP email with `msmtp` from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email and attachments through the user's SMTP account. <br>
Mitigation: Verify every recipient, message body, header, and attachment before sending. <br>
Risk: SMTP credentials could be exposed if placed in prompts or files. <br>
Mitigation: Use a dedicated app password or scoped SMTP credential and keep `SMTP_PASS` out of prompts and committed files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires `msmtp` and SMTP environment variables; may include recipient, header, CC/BCC, and attachment guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
