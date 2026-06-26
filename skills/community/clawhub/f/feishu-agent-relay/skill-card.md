## Description: <br>
Enables multi-Agent collaboration on Feishu by relaying tasks between coordinator and specialist Bots with user ID mapping and proactive messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Glassmarbles](https://clawhub.ai/user/Glassmarbles) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and internal teams use this skill to coordinate multiple Feishu Bots, route user requests from a coordinator to specialist agents, and send follow-up messages through the correct Bot-specific Feishu open_id. Personal single-user deployments can use auto-registration; team deployments require careful identity controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weak identity binding in multi-user mode could let a user claim another identifier and cause private Bot messages to be misrouted. <br>
Mitigation: Use verified identity binding such as SSO, LDAP, or a workspace-approved directory before multi-user or production deployment. <br>
Risk: Cross-Bot identifier mappings can expose sensitive relationships between users and Feishu Bots if the mapping file is broadly accessible. <br>
Mitigation: Restrict access to the mapping file, encrypt or otherwise protect stored identifiers, and define retention and deletion rules. <br>
Risk: Specialist Bots can proactively message users, which may surprise users or violate internal communication expectations. <br>
Mitigation: Obtain user consent, document when proactive messages are sent, and limit Bot permissions to the minimum required workspace scope. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Glassmarbles/feishu-agent-relay) <br>
- [Single-User Mode Setup Guide](artifact/references/single-user-setup.md) <br>
- [Feishu Bot Setup Guide](artifact/references/feishu-bot-setup.md) <br>
- [User Mapping Table Schema](artifact/references/mapping-schema.md) <br>
- [Relay Examples](artifact/references/relay-examples.md) <br>
- [Feishu Developer Console](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown documentation with JavaScript examples, shell commands, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance, relay patterns, mapping-table schemas, and a JavaScript mapping helper for Feishu Bot coordination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
