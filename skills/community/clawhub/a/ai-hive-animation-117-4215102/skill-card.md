## Description:

Guides creators through an AI-HIVE workflow for high-perspective, high-contrast comic-style animation, from planning and rights checks to model routing, sample generation, task tracking, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and content teams use this skill to plan and produce original anime, web-comic, game, music-video, visual-effects, and short-form animation assets with AI-HIVE. It emphasizes original characters, licensed inputs, model and price checks, task records, and explicit confirmation before paid generation or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send AI-HIVE credentials to an arbitrary configured endpoint.

Mitigation: Prefer OAuth through an MCP client or a scoped API key in a secret manager, and set AI_HIVE_MCP_URL only for destinations that are fully trusted.

Risk: Image or video generation, upload, batch, send, and publish actions may incur cost or expose user-provided media.

Mitigation: Query current models and prices first, preserve task IDs, and require explicit user confirmation before paid or public actions.

Risk: Using unlicensed characters, logos, music, fonts, images, video, or likenesses can create rights and publication issues.

Mitigation: Use original or licensed assets, keep a rights checklist, and limit references to mechanisms such as composition, rhythm, camera language, or information hierarchy.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/ai-hive-animation-117-4215102)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [Original workflow card](references/original-workflow.md)
- [AI-HIVE MCP binding guide](references/mcp-binding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, JSON work orders, shell commands, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model and price snapshots, task IDs, rights checklists, generation plans, and acceptance checks when the user confirms generation.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
