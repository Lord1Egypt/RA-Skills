## Description:

Bitchat integration skill for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wkyleg](https://clawhub.ai/user/wkyleg)

### License/Terms of Use:

Unlicense

## Use Case:

Developers and operators use this skill to connect OpenClaw agents to a Bitchat BLE mesh channel for local peer-to-peer messaging and agent coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reachable HTTP callers or nearby peers may inject text into active OpenClaw sessions.

Mitigation: Bind the OpenClaw webhook and bitchat-node bridge to trusted local interfaces, avoid remote bridgeUrl values, and add transport security plus bridge authentication before exposing the bridge.

Risk: The direct-message policy can permit unsolicited peer messages.

Mitigation: Set dmPolicy to allowlist or disabled, and maintain allowFrom with only trusted peer IDs before using the skill with sensitive sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wkyleg/skills/bitchat)
- [bitchat-node](https://github.com/wkyleg/bitchat-node)
- [OpenClaw plugin documentation](https://docs.openclaw.ai/plugins)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route Bitchat messages into active OpenClaw sessions when installed and configured.]

## Skill Version(s):

0.1.2 (source: server release, SKILL.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
