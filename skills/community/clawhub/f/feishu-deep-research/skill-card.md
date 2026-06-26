## Description: <br>
Generates structured deep-research reports from a user topic and imports the resulting Markdown report into a Feishu cloud document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henryjing96](https://clawhub.ai/user/henryjing96) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, analysts, and developers use this skill to run multi-step research on a topic, produce a cited Markdown report, and deliver it as a Feishu document in a target cloud-space folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make authenticated Feishu cloud-document changes. <br>
Mitigation: Use a least-privilege Feishu app and a non-sensitive target folder. <br>
Risk: The artifact instructs agents to print Feishu app secrets, tenant access tokens, file tokens, tickets, and document tokens in chat. <br>
Mitigation: Use a managed secret store and mask secrets and tokens in status output. <br>
Risk: The security verdict is suspicious because live Feishu tokens and secrets may be exposed during execution. <br>
Mitigation: Review before installing and prevent credential disclosure before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/henryjing96/feishu-deep-research) <br>
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu media upload API endpoint](https://open.feishu.cn/open-apis/drive/v1/medias/upload_all) <br>
- [Feishu import task API endpoint](https://open.feishu.cn/open-apis/drive/v1/import_tasks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report, Feishu document link, status summary, and JSON-style execution result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a research topic, Feishu folder token, and Feishu app credentials with document upload and import permissions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
