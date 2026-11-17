## Description:

Helps animation, comics, game, original IP, and character content teams use AI-HIVE to plan and produce original image and video assets with model, price, task, and acceptance tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creative teams and agent users use this skill to turn a brief for the '万物皆战场' scenario into an original production plan, rights checklist, AI-HIVE model route, sample-generation workflow, task record, and acceptance checklist. The skill is intended for controlled AI-HIVE image and video generation where paid, batch, send, and public publish actions require separate confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or OAuth tokens could be exposed or sent to an unintended MCP endpoint if credential handling is loose or AI_HIVE_MCP_URL is overridden.

Mitigation: Use OAuth where supported, store API keys only in client secrets or environment variables, avoid overriding AI_HIVE_MCP_URL, and revoke credentials immediately if exposed.

Risk: Image, video, upload, batch, send, or publish actions may create cost, disclose user assets, or release content unintentionally.

Mitigation: Confirm the model, price, count, destination, and publish status before each paid, upload, batch, send, or public-release action.

Risk: Reference works, brands, music, fonts, images, or videos may lack rights for generated or published outputs.

Mitigation: Maintain a rights checklist, separate owned or licensed materials from analysis-only references, and verify originality before publication.

Risk: Retrying after local timeouts may duplicate generation tasks and charges.

Mitigation: Record task IDs and query the original task with ai_hive_get_task before retrying generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-animation-095-af8d8e5)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [Original workflow card](references/original-workflow.md)
- [MCP login and binding guide](references/mcp-binding.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API key MCP configuration example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell command examples, and optional local JSON work-order files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include planning artifacts, rights and safety checklists, model-routing guidance, task IDs, price snapshots, and acceptance criteria.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
