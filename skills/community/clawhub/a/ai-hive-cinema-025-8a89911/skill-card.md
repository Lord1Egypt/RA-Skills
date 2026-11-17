## Description:

This skill helps directors, photographers, creative teams, brand visual teams, and content creators plan and execute an AI-HIVE workflow for low-angle cool-blue science-fiction imagery with orange firelight, including model routing, work orders, sample generation, task tracking, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creative professionals and developers use this skill to turn a visual brief into an AI-HIVE production plan, rights checklist, model and cost routing, sample generation path, task record, and acceptance checklist for original image or video production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE credentials could be sent to an unintended remote MCP endpoint if AI_HIVE_MCP_URL is changed.

Mitigation: Keep the default AI-HIVE MCP URL, do not point AI_HIVE_MCP_URL at non-AI-HIVE services, and prefer OAuth or a tightly scoped and revocable API key.

Risk: Remote generation, upload, batch, send, or publish actions may create costs or expose content.

Mitigation: Confirm the selected model, current price, batch size, upload scope, send target, and publishing action before running generation commands.

Risk: Input media or generated outputs may include rights-sensitive people, brands, music, fonts, logos, or reference material.

Mitigation: Maintain a rights checklist, use only owned or licensed assets for public output, and avoid unauthorized likenesses, logos, music, characters, or direct living-artist imitation.

## Reference(s):

- [Original workflow card](artifact/references/original-workflow.md)
- [AI-HIVE MCP login and binding guide](artifact/references/mcp-binding.md)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-cinema-025-8a89911)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local JSON work orders, AI-HIVE model and price snapshots, task IDs, rights records, and acceptance checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
