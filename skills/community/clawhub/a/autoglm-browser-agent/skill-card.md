## Description:

Autoglm Browser Agent delegates browser-based tasks to an autonomous browser subagent that can open sites, search, interact with pages, fill forms, capture screenshots, and continue sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrhenghu](https://clawhub.ai/user/mrhenghu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to automate browser workflows such as web search, social media interaction, form entry, screenshots, online shopping comparison, news review, and online document operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags unverifiable local binaries and a long-running browser relay.

Mitigation: Verify the exact binaries and their source before running them, and keep the relay stopped when browser automation is not in use.

Risk: The skill can persist broad approval for account actions through auto_approve.

Mitigation: Keep auto_approve disabled and require explicit user confirmation for posting, messaging, purchases, form submissions, and other sensitive actions.

Risk: Feishu integration can use app credentials and send screenshots to chats.

Mitigation: Use least-privilege Feishu credentials and enable screenshot replies only for trusted workspaces and conversations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrhenghu/skills/autoglm-browser-agent)
- [Publisher profile](https://clawhub.ai/user/mrhenghu)
- [AutoClaw Chrome Web Store extension](https://chromewebstore.google.com/detail/jelniggicmclhfgnlapbkgfibmgelfnp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown containing browser task results and screenshot links, with shell commands for setup and tool calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are expected to include screenshots; sensitive browser actions may require user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
