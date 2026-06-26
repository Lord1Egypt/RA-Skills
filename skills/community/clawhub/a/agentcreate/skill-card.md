## Description: <br>
Creates or uninstalls isolated OpenClaw agents with separate workspaces, optional channel bindings such as Feishu or WeChat, and model selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xf9070](https://clawhub.ai/user/xf9070) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create independent agents, bind optional messaging channels, select models, and safely uninstall agents when they are no longer needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full uninstall can force-delete an agent workspace and directly edit local OpenClaw configuration. <br>
Mitigation: Verify the exact agent ID, never delete the protected main agent, back up the workspace and openclaw.json before deletion, and require the documented second confirmation. <br>
Risk: Channel credentials such as appId and appSecret may be exposed or removed from shared channel accounts. <br>
Mitigation: Treat channel credentials as sensitive, confirm whether an account is shared before removal, and rotate credentials if exposure is suspected. <br>
Risk: The artifact contains a hard-coded example configuration path for direct Python editing during account deletion. <br>
Mitigation: Replace the example path with the user's actual OpenClaw configuration path before running any edit and validate the configuration after the change. <br>


## Reference(s): <br>
- [Agent creation implementation](references/create.md) <br>
- [Agent uninstall implementation](references/delete.md) <br>
- [ClawHub skill page](https://clawhub.ai/xf9070/agentcreate) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash, JSON, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents through user confirmation, OpenClaw wrapper commands, configuration updates, validation checks, and rollback-aware deletion steps.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
