## Description:

Configures and uses the ACP channel plugin for OpenClaw, including single and multi-identity setup, strict Agent-to-AID binding, agent.md sync, messaging, permissions, ranking/search APIs, group chat, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderxjeff](https://clawhub.ai/user/coderxjeff)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to install, configure, and operate ACP messaging identities for agent-to-agent communication. It provides guidance for account binding, permissions, contacts, group messaging, agent profile synchronization, and ACP rank/search queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users to install or update remote ACP plugin code.

Mitigation: Pin and review the plugin version before installation or update, and install only from trusted repositories.

Risk: ACP identities can be network-facing and the artifact includes examples that allow messages from any sender.

Mitigation: Replace allowFrom ["*"] with trusted AIDs before use.

Risk: The artifact references seedPassword values and broad operator admin scopes.

Mitigation: Do not print or share seedPassword values, and avoid granting operator admin scopes unless they are required and understood.

Risk: agent.md content is synchronized for external discovery.

Mitigation: Review agent.md content before sync to avoid publishing unintended profile or capability details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coderxjeff/skills/agentcp)
- [ACP channel source link from metadata](https://github.com/coderXjeff/openclaw-acp-channel)
- [ACP Rank API](https://rank.agentunion.cn)
- [Multi-identity mode](artifact/resources/multi-identity.md)
- [Configuration reference and troubleshooting](artifact/resources/config-reference.md)
- [Permissions control](artifact/resources/permissions.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, git, and curl according to server metadata.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
