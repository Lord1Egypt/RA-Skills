## Description:

Guides anime, game, original IP, and character-content teams through an AI-HIVE workflow that plans, samples, and generates original animation or game-oriented content after checking current models and prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, production teams, and developers use this skill to create original anime, comic-drama, game, or character-based content through AI-HIVE. It produces a plan, rights checklist, model and price checks, sample-first workflow, task records, generated assets, and acceptance checklist before paid generation or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send API credentials to an environment-selected server if the MCP URL is overridden.

Mitigation: Verify the MCP URL is exactly https://ai-hive.iclip.cn/api/mcp, avoid setting AI_HIVE_MCP_URL, and prefer the OAuth connector with revocable scoped credentials.

Risk: The MCP activation scope is broader than this narrow workflow.

Mitigation: Install only when intending to use AI-HIVE for this workflow and require explicit confirmation before paid generation, batch actions, uploads, sending, or publishing.

Risk: Image or video generation may incur cost or duplicate work if retried after a timeout.

Mitigation: Query current models and prices first, confirm the expected calls and budget, keep task IDs, and use ai_hive_get_task before submitting a retry.

Risk: Creative references or user materials may introduce intellectual property or rights issues.

Mitigation: Maintain a rights checklist, use references only for structure or mechanics, require authorization for public use, and check outputs for original differences before release.

Risk: API keys, OAuth tokens, private prompts, or user materials may be exposed in prompts, logs, screenshots, or repositories.

Mitigation: Store credentials in client secrets or environment variables, keep sensitive content out of shared artifacts, and revoke credentials immediately if exposed.

## Reference(s):

- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE remote MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [Original workflow card](references/original-workflow.md)
- [MCP login and binding guide](references/mcp-binding.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API key MCP configuration example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and local JSON work-order output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before paid generation, batch actions, uploads, sending, or public publishing.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
