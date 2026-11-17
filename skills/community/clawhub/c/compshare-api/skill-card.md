## Description:

Manages the full lifecycle of GPU instances on the 优云智算 CompShare platform, including create, query, start, stop, reboot, password reset, delete, and SSH administration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chsengni](https://clawhub.ai/user/chsengni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to provision and administer CompShare GPU cloud instances, manage lifecycle actions, reset passwords, and perform SSH-based remote administration.

### Deployment Geography for Use:

China regions supported by CompShare, including cn-wlcb and cn-sh2.

## Known Risks and Mitigations:

Risk: The skill can manage GPU instances and perform broad SSH administration.

Mitigation: Use credentials scoped only to CompShare resources the agent is allowed to manage, and review lifecycle and SSH actions before execution.

Risk: Passwords and instance login material may be passed through command-line arguments, command output, or logs.

Mitigation: Avoid passing passwords on the command line where possible, limit log retention, and treat list output and SSH connection details as sensitive.

Risk: SSH shell and file operations provide full remote administration authority on target instances.

Mitigation: Verify SSH host keys independently and restrict remote commands, uploads, downloads, permission changes, and deletions to approved tasks.

## Reference(s):

- [CompShare API Reference](artifact/references/api_reference.md)
- [CompShare API Endpoint](https://api.compshare.cn/)
- [CompShare API Management Console](https://console.compshare.cn/uaccount/api_manage)
- [ClawHub Skill Page](https://clawhub.ai/chsengni/skills/compshare-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and command output summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call CompShare APIs and SSH commands when the agent has configured credentials and user authorization.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
