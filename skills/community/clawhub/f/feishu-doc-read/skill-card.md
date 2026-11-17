## Description:

Fetches Feishu/Lark cloud document content as Markdown and identifies embedded images, files, and whiteboards for separate media retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to retrieve Feishu/Lark document content from a URL or token, then decide when to fetch embedded media or route wiki-backed sheets and bitables to the appropriate Feishu tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may access sensitive Feishu/Lark document content when given document URLs or tokens.

Mitigation: Use the skill only with documents the agent is expected to access, and review provided URLs or tokens before retrieval.

Risk: Embedded media downloads may write files to a user-specified output path.

Mitigation: Review the media download path before use and choose a controlled local destination.

Risk: Wiki links may resolve to sheets, bitables, or other Feishu object types rather than cloud documents.

Mitigation: Resolve the wiki node type first and route only the confirmed object type to the matching Feishu tool.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown content with HTML-style media placeholders and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Embedded images, files, and whiteboards require follow-up media download actions before local inspection.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
