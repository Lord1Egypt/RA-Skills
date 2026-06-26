## Description: <br>
Guide for OpenClaw agents to create, read, and edit Feishu/Lark documents through the Feishu Drive API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmin1113](https://clawhub.ai/user/jmin1113) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent operators use this skill to create Feishu/Lark documents, write block content, read existing documents by URL or ID, configure collaborator access, and troubleshoot cross-agent document workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill normalizes publicly editable Feishu documents and broad sharing settings. <br>
Mitigation: Require explicit approval before making documents public or editable by anyone, and prefer named collaborators or read-only links. <br>
Risk: Cross-agent session visibility can expose document workflows beyond the initiating agent. <br>
Mitigation: Avoid global session visibility unless the operator understands and accepts the cross-agent exposure. <br>
Risk: Feishu app secrets and tenant access tokens may be exposed through prompts, logs, or shared documents. <br>
Mitigation: Keep app secrets and tokens out of prompts, logs, generated documents, and shared collaboration spaces. <br>


## Reference(s): <br>
- [Agent Feishu Doc detailed guide](references/guide.md) <br>
- [Feishu Drive document API endpoint](https://open.feishu.cn/open-apis/drive/v1/documents) <br>
- [Feishu document URL pattern](https://feishu.cn/docx/{doc_id}) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Feishu API examples, curl commands, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; outputs are intended for agent operators to adapt before calling Feishu APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
