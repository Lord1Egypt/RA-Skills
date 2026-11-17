## Description:

This skill helps animation, comics, game, original IP, and character-content teams plan and produce a warm farm-life pixel game short with AI-HIVE by querying current model options and prices, preparing original character and scene assets, generating samples and video assets after confirmation, and tracking tasks and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and content teams use this skill to turn a brief for a warm farm-life pixel game short into a production plan, rights checklist, storyboard, keyframes, animation clips, task records, and acceptance checklist. It is designed for original character and scene workflows and requires separate confirmation before paid generation, batch actions, sending, or public release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send credentials to a nonstandard AI-HIVE MCP endpoint if AI_HIVE_MCP_URL is overridden.

Mitigation: Use the documented AI-HIVE endpoint only, avoid setting AI_HIVE_MCP_URL, and keep AI_HIVE_API_KEY or OAuth tokens in a proper secret store.

Risk: Image or video generation, uploads, batch actions, sending, or publishing may have cost, rights, or release implications.

Mitigation: Confirm model choice, price snapshot, generation count, uploads, publishing, and any non-read-only tool call before proceeding.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/wubin1836/skills/ai-hive-animation-110-7382dc5)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [Original Workflow Reference](references/original-workflow.md)
- [AI-HIVE MCP Binding Guide](references/mcp-binding.md)
- [OAuth MCP Configuration Example](references/mcp-config.example.json)
- [API-Key MCP Configuration Example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a local JSON work order and AI-HIVE task identifiers when the user confirms execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
