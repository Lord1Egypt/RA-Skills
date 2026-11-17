## Description:

Guides creators through an AI-HIVE workflow for planning, generating, tracking, and reviewing an original new-school wuxia and folk-fantasy action short.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, directors, photographers, advertising teams, brand visual teams, and content creators use this skill to turn a short-film brief into an auditable AI-HIVE production plan, sample, generation record, and acceptance checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad remote MCP capabilities for AI-HIVE image, video, upload, and task operations.

Mitigation: Review before installing, prefer OAuth, verify the AI-HIVE connection target, and approve uploads or paid generations only after checking the model, cost, call count, and data being sent.

Risk: The helper script can send credentials to an environment-selected MCP endpoint.

Mitigation: Do not set a custom MCP endpoint unless it has been verified; keep API keys and OAuth tokens out of prompts, logs, screenshots, and repositories, and revoke grants or keys when finished.

Risk: Generated media may include unlicensed references, brands, likenesses, music, fonts, images, or videos.

Mitigation: Maintain a rights checklist, separate owned and authorized assets from analysis-only references, and require explicit confirmation before public release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-cinema-024-bd33891)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP binding guide](references/mcp-binding.md)
- [Original workflow guide](references/original-workflow.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API key MCP configuration example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and optional local JSON work orders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE model-routing guidance, task IDs, cost checkpoints, rights checks, and acceptance criteria.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
