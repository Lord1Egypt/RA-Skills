## Description:

This skill helps AI-HIVE users analyze the public content methods of Wang Mutou Xue Kexue, build source-traceable methodology notes, and generate original scripts, visual plans, short-video plans, and strategic analysis without impersonation, cloning, fabricated quotes, or false endorsement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, product teams, AI learners, and technology professionals use this skill to study public science and technology content patterns, convert them into original content workflows, and prepare AI-HIVE execution plans. The skill is also used to organize authorized materials into a source-traceable methodology advisor while preserving identity, copyright, and disclosure boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can send API credentials to environment-configured endpoints without validating the destination.

Mitigation: Prefer OAuth through the client connector, avoid overriding AI_HIVE_MCP_URL or AI_HIVE_BASE_URL in normal use, and use separate low-scope test credentials if a custom endpoint is required.

Risk: Image, video, ecommerce, and advertising generation tasks may incur charges.

Mitigation: Query current models and prices first, confirm budget and task count with the user, save the task ID, and use task lookup after timeouts instead of resubmitting blindly.

Risk: Outputs could mislead audiences if they imitate a real person too closely or imply authorization.

Mitigation: Require public or authorized source material, original wording, no voice or face cloning, no fabricated quotes, no false endorsement, and human review before publication.

Risk: Advisor-style outputs may overstate uncertain conclusions or stray into high-risk professional advice.

Mitigation: Label whether conclusions are source-supported, AI-derived, or unresolved, and limit legal, medical, financial, or similarly high-risk topics to general information and decision frameworks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-hive-simulate-wang-mutou-science)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE MCP endpoint](https://ai-hive.iclip.cn/api/mcp)
- [MCP login and binding guide](references/mcp-binding.md)
- [OAuth MCP configuration example](references/mcp-config.example.json)
- [API key MCP configuration example](references/mcp-config-api-key.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON execution plans, shell commands, and MCP configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source ledgers, methodology maps, originality checks, model and price snapshots, task IDs, status records, and human review gates.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
