## Description: <br>
Creates OpenClaw agents and binds them to Feishu group chats by collecting requirements, confirming an Agent Card, generating configuration files, and providing binding and testing commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuanyizhi](https://clawhub.ai/user/xuanyizhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace administrators use this skill to define a new OpenClaw agent, generate its local configuration files, and bind it to a Feishu group with administrator and member permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect Feishu group, administrator, allowlist, or routing settings could bind the wrong agent or expose the agent in an unintended group. <br>
Mitigation: Confirm the Agent Card, group ID, administrator identity, allowlist entry, and binding configuration before applying changes. <br>
Risk: Generated agent behavior may exceed the intended purpose if persona, capabilities, boundaries, or permissions are underspecified. <br>
Mitigation: Require explicit user confirmation of the persona, allowed capabilities, red-line boundaries, and administrator versus member permissions before writing configuration files. <br>
Risk: Setup notes written to memory could include sensitive operational details. <br>
Mitigation: Review setup notes for secrets, private group identifiers, or unnecessary sensitive details before saving them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuanyizhi/agent-creator-feishu) <br>
- [Agent Card Template](references/AGENT-CARD-TEMPLATE.md) <br>
- [OpenClaw Agent Creation Guide](references/AGENT-CREATION-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with generated file templates, JSON configuration snippets, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local OpenClaw agent workspace files, allowlist or routing configuration, and setup notes after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
