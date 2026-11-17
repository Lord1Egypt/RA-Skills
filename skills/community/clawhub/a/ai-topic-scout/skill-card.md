## Description:

AI Topic Scout gathers recent YouTube videos and X/Twitter posts from configured AI creators, summarizes and clusters the content into trending short-video topic ideas, scores topic heat, and writes the results to DingTalk AI Tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agegr](https://clawhub.ai/user/agegr)

### License/Terms of Use:

MIT-0

## Use Case:

Content strategists, creators, and operators use this skill to monitor AI-focused YouTube and X/Twitter sources, identify cross-platform topic momentum, and generate short-video topic recommendations for review in DingTalk AI Tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live X/Twitter session cookies.

Mitigation: Use a dedicated low-privilege X/Twitter account, avoid passing auth_token or ct0 directly in shell history, and clear or disable command history if command-line credentials are unavoidable.

Risk: The skill writes records to DingTalk AI Tables.

Mitigation: Verify the DingTalk MCP base and table IDs before any write, and replace the bundled DingTalk IDs with an initialized configuration owned by the operator.

Risk: The skill depends on external CLIs and installed skills.

Mitigation: Pin or isolate dependencies such as mcporter, bird, yt-dlp, dingtalk-ai-table, and youtube-watcher in a controlled environment before routine use.

Risk: Incorrect creator handles or IDs could fetch or analyze the wrong source material.

Mitigation: Validate all YouTube handles, X/Twitter handles, base IDs, table IDs, field IDs, and option IDs before executing commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agegr/skills/ai-topic-scout)
- [DingTalk MCP Configuration](https://mcp.dingtalk.com/#/detail?mcpId=9555&detailType=marketMcpDetail)
- [Setup Guide](references/setup-guide.md)
- [Table Schema](references/table-schema.md)
- [Operational Gotchas](references/gotchas.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, summaries, scores, and DingTalk table records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces topic summaries, heat scores, background context, target-audience guidance, suggested video length, content structure, and title ideas.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
