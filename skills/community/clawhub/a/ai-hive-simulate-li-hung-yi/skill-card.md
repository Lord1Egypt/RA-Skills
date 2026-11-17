## Description:

Helps users study Li Hung-yi's public content methods and produce original AI-HIVE content plans, scripts, visuals, and methodology-based strategic analysis without impersonation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, product managers, AI learners, and business users use this skill to convert public-source research into original content workflows and AI-HIVE execution plans. It also supports methodology-style advisory analysis when users provide materials they have rights to use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE credentials could be sent to an untrusted endpoint if endpoint override environment variables are set.

Mitigation: Use the documented AI-HIVE endpoints only, avoid setting AI_HIVE_MCP_URL or AI_HIVE_BASE_URL unless the destination is fully trusted, and keep API keys in a controlled secret store.

Risk: Image, video, advertising, or other generation tasks may create charges or duplicate work if submitted without review.

Mitigation: Confirm model, price, quantity, parameters, and budget before creating generation tasks; on timeout, query the original task ID instead of resubmitting.

Risk: Outputs could imply impersonation, false endorsement, or unauthorized use of protected content if published without human review.

Mitigation: Require source, identity, originality, rights, and public-release review before batch production or publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-hive-simulate-li-hung-yi)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [MCP Login and Binding Guide](references/mcp-binding.md)
- [OAuth MCP Configuration Example](references/mcp-config.example.json)
- [API Key MCP Configuration Example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and generated plan files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source ledgers, method maps, originality checks, AI-HIVE model and price snapshots, task IDs, and review gates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
