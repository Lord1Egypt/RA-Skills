## Description: <br>
Connector Hub is a centralized registry and decision guide for 33 connector integrations, with reference documentation and executable Python scripts for services across documents, messaging, storage, enterprise data, finance, code hosting, project management, and business services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to choose between platform connectors and Skill-based API alternatives, then follow the relevant reference file or script for integration tasks. It is most useful when an agent needs a broad catalog of connector options and examples for third-party services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send messages, upload files, or create records in live third-party systems. <br>
Mitigation: Use test workspaces first and review the exact script and target service before execution. <br>
Risk: Several integrations require OAuth tokens, wallet access, or other sensitive credentials. <br>
Mitigation: Use least-privilege credentials, keep secrets out of prompts and logs, and rotate tokens after testing. <br>
Risk: Some write-capable actions may appear in query-style connector categories. <br>
Mitigation: Confirm whether the selected script performs read or write operations before running it. <br>


## Reference(s): <br>
- [Connector Hub on ClawHub](https://clawhub.ai/wangjiaocheng/connector-hub) <br>
- [CloudBase connector reference](artifact/references/L1-platform-C01-cloudbase.md) <br>
- [EdgeOne Pages connector reference](artifact/references/L1-platform-C02-edgeone-pages.md) <br>
- [Zhiyan CI/CD connector reference](artifact/references/L1-platform-C03-zhiyan-ci-cd.md) <br>
- [Tencent Meeting connector reference](artifact/references/L1-platform-C04-tmeet.md) <br>
- [Tencent Docs connector reference](artifact/references/L2-auth-docs-kb-C05-tencent-docs.md) <br>
- [KDocs connector reference](artifact/references/L2-auth-docs-kb-C06-kdocs.md) <br>
- [Notion connector reference](artifact/references/L2-auth-docs-kb-C07-notion.md) <br>
- [Feishu connector reference](artifact/references/L2-auth-messaging-C12-feishu.md) <br>
- [DingTalk connector reference](artifact/references/L2-auth-messaging-C13-dingtalk.md) <br>
- [WeCom connector reference](artifact/references/L2-auth-messaging-C14-wecom.md) <br>
- [Baidu Netdisk connector reference](artifact/references/L2-auth-storage-C17-baidu-netdisk.md) <br>
- [GitHub connector reference](artifact/references/L3-api-code-hosting-C23-github.md) <br>
- [TAPD connector reference](artifact/references/L3-api-project-mgmt-C27-tapd.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python script references, shell command examples, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate live external API actions when the referenced scripts are run with valid credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
