## Description:

Helps Chinese-language creators and teams study Andrew Ng's public content methods, build sourced method maps, and plan original AI-HIVE content without impersonation or false endorsement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, product managers, AI learners, and teams use this skill to turn authorized public source material into sourced method maps, original scripts, visual plans, and AI-HIVE execution plans. It is intended for content research and production workflows that require human review for rights, identity, cost, and factual accuracy.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: AI-HIVE credentials could be exposed to an untrusted endpoint if users override the default MCP or API base URLs.

Mitigation: Prefer OAuth in a trusted client, avoid setting AI_HIVE_MCP_URL or AI_HIVE_BASE_URL, and keep API keys in a revocable secret store or environment variable.

Risk: Broad remote AI-HIVE tools can upload media or start image and video generation tasks that may incur costs.

Mitigation: Use read-only model listing for connection tests, confirm pricing, model choice, task count, and budget before generation, and save task IDs for follow-up instead of retrying blindly.

Risk: Private, paid, third-party, or sensitive material could be uploaded without adequate rights or permission.

Mitigation: Use only public or authorized materials, record source and rights information, and require human review before upload, batch processing, or publication.

Risk: Outputs about Andrew Ng could be mistaken for his own statements, endorsement, voice, likeness, or authorization.

Mitigation: Keep outputs framed as AI-assisted method analysis, avoid voice or face cloning, do not fabricate quotes or affiliations, and require public-facing identity review.

## Reference(s):

- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP login and binding guide](references/mcp-binding.md)
- [AI-HIVE OAuth MCP configuration example](references/mcp-config.example.json)
- [AI-HIVE API key MCP configuration example](references/mcp-config-api-key.example.json)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-simulate-andrew-ng-cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON execution plans, shell commands, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May connect to AI-HIVE after user authentication; generation tasks can be asynchronous and may incur costs.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
