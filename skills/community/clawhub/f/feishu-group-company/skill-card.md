## Description: <br>
Configure a Feishu multi-bot company group so a coordinator bot handles normal messages while specialist bots reply only when explicitly @mentioned. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex-shen1121](https://clawhub.ai/user/alex-shen1121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to patch and verify OpenClaw Feishu routing for shared company groups with a default coordinator and mention-gated specialist bots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configuration patch changes local OpenClaw Feishu routing behavior for a group. <br>
Mitigation: Run the script with --dry-run first, verify the group and account IDs, and use --backup before writing changes. <br>
Risk: Incorrect group or account IDs can route messages to the wrong coordinator or specialist bots. <br>
Mitigation: Confirm the target group chat ID and all Feishu account IDs before applying the patch, then reload Gateway and test plain and @mentioned messages. <br>


## Reference(s): <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub skill page](https://clawhub.ai/alex-shen1121/feishu-group-company) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dry-run and backup guidance for a Python script that updates local OpenClaw Feishu routing configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
