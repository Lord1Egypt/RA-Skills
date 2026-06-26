## Description: <br>
FlowBridge is a no-code cross-platform automation skill for building workflows across WeChat, DingTalk, Feishu, WPS, Tencent Docs, and Aliyun Drive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operations teams, and developers use FlowBridge to define and run no-code workflows that connect Chinese collaboration, messaging, document, approval, and file platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad cross-platform workflows could move messages, documents, approvals, or files without enough scoping or confirmation. <br>
Mitigation: Use test accounts first, restrict connector OAuth scopes, and review every AI-generated or template-created workflow before running it. <br>
Risk: Workflows and logs may involve chat logs, invoices, approvals, employee data, files, tokens, or sensitive audit data. <br>
Mitigation: Move sensitive data only with consent and a clear destination policy, and do not log or export tokens or sensitive audit data to shared locations. <br>


## Reference(s): <br>
- [FlowBridge README](artifact/README.md) <br>
- [Connector Configuration](artifact/config/connectors.yaml) <br>
- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/flowbridge) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code snippets, plus YAML connector configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated workflows can include connector actions, execution status, audit records, and exported logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
