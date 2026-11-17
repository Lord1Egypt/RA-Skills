## Description:

This Chinese-language AI-HIVE workflow helps anime, webcomic, game, original IP, and character-content teams plan and produce ensemble character entrance animations with model lookup, rights checks, sample generation, task tracking, and acceptance criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, content teams, and developers use this skill to create original ensemble character entrance animations for anime, webcomic, game, short-video, and original-IP workflows through AI-HIVE. It guides planning, rights review, model and price lookup, sample generation, task recovery, and final acceptance checks while requiring explicit confirmation before paid generation, batching, sending, or public release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the helper can send AI-HIVE credentials to an environment-selected server.

Mitigation: Use OAuth or a client secret store, verify the official HTTPS AI-HIVE MCP endpoint before setting AI_HIVE_MCP_URL, and revoke any API key that may have been used with an untrusted endpoint.

Risk: Prompts, uploaded assets, and generation metadata may be sent to AI-HIVE.

Mitigation: Install and use the skill only when that data sharing is acceptable for the task, and avoid submitting private or unlicensed assets.

Risk: Image and video generation, uploads, batching, sending, or publication can affect cost and public exposure.

Mitigation: Require explicit user confirmation for paid generation, batch actions, sending, and public release, and preserve task IDs plus model and price snapshots for review.

## Reference(s):

- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [MCP login and binding guide](references/mcp-binding.md)
- [Original workflow guide](references/original-workflow.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API key MCP configuration example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, local JSON work orders, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send prompts, uploaded assets, credentials, and generation metadata to AI-HIVE when connected; paid generation and publication require explicit confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
