## Description:

知识管理全流程：文章链接/对话内容/文稿 → 结构化总结 → 飞书知识库归档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[keson1521](https://clawhub.ai/user/keson1521)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use this skill to turn public article links, pasted drafts, or useful chat content into structured summaries and archive them into a personal Feishu knowledge base. It can also screen articles for reading value or produce summaries without archival.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary public URLs and process article or chat content.

Mitigation: Use explicit command-style invocation, restrict URLs to trusted public sites, and review content before archival when handling sensitive material.

Risk: The skill can write generated summaries, images, and index entries to Feishu under the user's account.

Mitigation: Run it only with Feishu credentials and workspace permissions appropriate for the target knowledge base, and review archived entries after use.

Risk: The skill relies on broad shell authority and dependencies that may be global or unpinned.

Mitigation: Install and run it in an isolated environment, pin dependencies where possible, and replace sourced shell configuration before business or sensitive-data use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keson1521/skills/feishu-knowledge-flow)
- [lark-cli](https://github.com/nicepkg/lark-cli)
- [Claude Code](https://claude.ai/code)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, Feishu document updates, and setup or execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Feishu knowledge base pages, update an index document, and create local configuration files during setup.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
