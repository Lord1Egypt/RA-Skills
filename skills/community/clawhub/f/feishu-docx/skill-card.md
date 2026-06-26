## Description: <br>
Creates and edits Feishu cloud Docx documents through Feishu APIs, including document creation, text appending, Markdown import, file upload, and block updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cpjhy](https://clawhub.ai/user/cpjhy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to create or update Feishu Docx documents from agent workflows, including importing local Markdown content into Feishu cloud documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports hardcoded Feishu credentials in the skill artifact. <br>
Mitigation: Do not use or copy embedded credentials; replace them with credentials you control and rotate or revoke any exposed secrets. <br>
Risk: The security scan reports scripts that can upload local files and change Feishu Drive content. <br>
Mitigation: Review scripts before execution and require explicit confirmation for local file uploads, Feishu document creation or import, and deletion. <br>


## Reference(s): <br>
- [Feishu Docx API Reference](references/api_reference.md) <br>
- [ClawHub Feishu Docx release page](https://clawhub.ai/cpjhy/feishu-docx) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Python and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Feishu document IDs, file tokens, import task status, and Feishu document URLs when scripts are run with valid credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
