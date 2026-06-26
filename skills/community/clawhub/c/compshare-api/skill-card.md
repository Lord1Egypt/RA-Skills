## Description: <br>
管理优云智算CompShare平台的GPU实例全生命周期，包括创建、查询、启动、停止、重启、重置密码和删除实例；当用户需要创建GPU云服务器、查询实例状态、管理实例启停、重置实例密码或删除实例时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chsengni](https://clawhub.ai/user/chsengni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage CompShare GPU cloud instances and administer the resulting servers over SSH. It supports instance lifecycle actions, credential-based API setup, remote command execution, and file transfer workflows. <br>

### Deployment Geography for Use: <br>
China CompShare regions referenced by the artifact, primarily cn-wlcb/cn-wlcb-01. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage a CompShare account and administer GPU servers over SSH. <br>
Mitigation: Install only for workflows where agent-managed CompShare resources and SSH administration are intended, and use least-privilege API keys. <br>
Risk: Destructive or high-impact actions include delete, reset-password, remote exec, file deletion, chmod, upload/download, and interactive shell use. <br>
Mitigation: Require explicit approval and verify the instance ID, SSH target, command, and path before each high-impact action. <br>
Risk: API keys and SSH passwords may be exposed through shell history, shared logs, or copied command examples. <br>
Mitigation: Avoid placing secrets directly in shell commands or shared logs; store credentials in protected configuration and rotate them if exposure is suspected. <br>


## Reference(s): <br>
- [CompShare API Reference](references/api_reference.md) <br>
- [CompShare Skill Page](https://clawhub.ai/chsengni/compshare-api) <br>
- [CompShare Console](https://console.compshare.cn/) <br>
- [CompShare API Management](https://console.compshare.cn/uaccount/api_manage) <br>
- [CompShare Image Community](https://www.compshare.cn/image-community) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, configuration snippets, and JSON-style command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CompShare API credentials and SSH passwords supplied by the user; API and SSH operations can affect live cloud resources.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
