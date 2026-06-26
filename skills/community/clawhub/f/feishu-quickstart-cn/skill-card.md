## Description: <br>
飞书快速集成配置 helps users connect OpenClaw with Feishu for document management, knowledge base workflows, and office automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Enterprise users, team administrators, and OpenClaw operators use this skill to configure Feishu app credentials, permissions, document access, knowledge base workflows, bitable automation, and optional webhook subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu credentials and App Secret may be exposed through logs, screenshots, or version control. <br>
Mitigation: Keep the App Secret out of logs, screenshots, and repositories; use a dedicated Feishu app and store credentials only in the intended OpenClaw configuration. <br>
Risk: The skill guides write-capable access to Feishu documents, knowledge bases, bitables, and optional webhook subscriptions. <br>
Mitigation: Grant minimum required scopes, restrict webhook subscriptions, confirm target links before updates, and test write workflows on non-production documents or tables first. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/feishu-quickstart-cn) <br>
- [Feishu Developer Console](https://open.feishu.cn/app) <br>
- [Feishu Open Platform Documentation](https://open.feishu.cn/document) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Feishu permission scopes, credential configuration examples, validation prompts, troubleshooting guidance, and pricing notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
