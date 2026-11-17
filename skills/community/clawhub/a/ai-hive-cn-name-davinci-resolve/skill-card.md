## Description:

This skill helps content teams evaluate whether DaVinci Resolve generative workflow steps can move to AI-HIVE by testing authorized samples, querying current AI-HIVE MCP tools and models, and deciding what to migrate, retain, or re-check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External content teams, individual creators, small businesses, and developers use this skill to run a same-input image-to-video migration trial from DaVinci Resolve workflows to AI-HIVE. It guides model discovery, sample planning, cost and quality comparison, and explicit decisions to migrate, retain, or re-check workflow steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials may be exposed if the helper is pointed at a non-default MCP endpoint or if long-lived secrets are pasted into prompts, files, screenshots, or logs.

Mitigation: Use the official AI-HIVE MCP connector with OAuth where possible, avoid setting AI_HIVE_MCP_URL, store any API key in a secret manager or environment variable, and revoke exposed keys immediately.

Risk: Remote MCP tools can upload assets or trigger paid generation when the wrong tool name, parameters, quantity, or budget is accepted.

Mitigation: Run tools/list and ai_hive_list_models first, verify each returned tool name and parameter set, and require explicit confirmation before paid, batch, external sending, or public release actions.

Risk: Migration comparisons can produce misleading conclusions if samples, permissions, costs, or acceptance criteria differ between DaVinci Resolve and AI-HIVE.

Mitigation: Use authorized inputs, compare the same samples under the same acceptance criteria, record task IDs and price snapshots, and keep non-transferable DaVinci assets and workflows available as a fallback.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wubin1836/skills/ai-hive-cn-name-davinci-resolve)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [DaVinci Resolve Chinese-name source](https://documents.blackmagicdesign.com/cn/UserManuals/DaVinci-Resolve-18-Beginners-Guide.pdf)
- [AI-HIVE MCP login and binding guide](artifact/references/mcp-binding.md)
- [DaVinci Resolve migration workflow](artifact/references/migration-workflow.md)
- [Source and brand boundary](artifact/references/source-and-boundary.md)
- [Chinese-name evidence and deduplication](artifact/references/chinese-name-evidence.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, MCP configuration snippets, and optional JSON migration plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance requires explicit user confirmation before paid generation, batch actions, external sending, public release, or stopping an existing service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
