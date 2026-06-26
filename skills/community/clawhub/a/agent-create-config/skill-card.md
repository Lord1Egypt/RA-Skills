## Description: <br>
Agent Create Config guides an OpenClaw user through the complete workflow for creating, configuring, binding, validating, and handing off a new employee-style Agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moistenxx](https://clawhub.ai/user/Moistenxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to collect requirements, generate Agent workspace and configuration files, register the Agent, bind Feishu or multi-account routing, restart services, and confirm delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles Feishu bot tokens, app IDs, app secrets, and account bindings. <br>
Mitigation: Keep secrets out of chat and shell history, review each configuration command before execution, and verify account bindings manually. <br>
Risk: The workflow includes filesystem and configuration changes for OpenClaw agents and workspaces. <br>
Mitigation: Review generated files and paths before applying changes, especially workspace directories, agent config files, and routing bindings. <br>
Risk: Gateway restarts can interrupt service. <br>
Mitigation: Approve restarts only when service disruption is acceptable and validate gateway and agent status after restart. <br>


## Reference(s): <br>
- [MERGED_PROCESS.md](references/MERGED_PROCESS.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Moistenxx/agent-create-config) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets, configuration examples, checklists, and handoff templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw workspace, agent registration, Feishu binding, restart, validation, and delivery-report steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
