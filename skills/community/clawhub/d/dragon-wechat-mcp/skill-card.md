## Description:

Windows desktop WeChat MCP for monitoring WeChat state and sending messages to a specified contact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragon015](https://clawhub.ai/user/dragon015)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to let an MCP-capable agent inspect the local WeChat desktop window state and send messages to a selected or current contact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real WeChat messages through desktop automation.

Mitigation: Require explicit user confirmation before each send and require an exact recipient before message delivery.

Risk: Verification and diagnostics can leave private chat screenshots on disk.

Mitigation: Avoid saving screenshots during normal use, and delete or restrict access to diagnostic images when troubleshooting is necessary.

Risk: Message entry uses the system clipboard and can overwrite or expose clipboard contents.

Mitigation: Restore the prior clipboard contents after sending and disclose clipboard use to the operator.

Risk: Window automation can target the wrong chat or non-WeChat windows if contact detection is ambiguous.

Mitigation: Limit diagnostics to WeChat-only windows and verify the resolved contact before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dragon015/skills/dragon-wechat-mcp)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [MCP tool responses as text or JSON, with setup guidance and Python usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Controls a local Windows WeChat desktop session and may create local screenshot files during verification or diagnostics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
