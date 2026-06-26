## Description: <br>
Guides an agent to send one user-specified local PDF for signature through the eSignGlobal CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weipengcopyright](https://clawhub.ai/user/weipengcopyright) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to collect an absolute PDF path, signer details, and an optional subject, then invoke eSignGlobal's CLI to send a single envelope for signature. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A confidential or regulated PDF may be sent to an external eSignGlobal service. <br>
Mitigation: Use only the absolute PDF path explicitly provided for the task and confirm the exact file before sending. <br>
Risk: Incorrect signer names or email addresses may send the envelope to the wrong recipients. <br>
Mitigation: Confirm the signer list, signing order, and optional subject before invoking the CLI. <br>
Risk: The eSignGlobal API key could be exposed through logs or local storage. <br>
Mitigation: Read credentials only from ESIGNGLOBAL_APIKEY and do not print, persist, or implement local storage for secrets. <br>


## Reference(s): <br>
- [Envelope Sender on ClawHub](https://clawhub.ai/weipengcopyright/envelope-sender) <br>
- [weipengcopyright publisher profile](https://clawhub.ai/user/weipengcopyright) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ESIGNGLOBAL_APIKEY and a single absolute path to an existing PDF.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
