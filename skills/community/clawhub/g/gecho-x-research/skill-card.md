## Description:

Search X (Twitter) posts and retrieve known post details and replies through the official Gecho Bridge MCP tools for keyword monitoring, post research, author context, engagement signals, and reply analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search X posts by keyword, inspect known posts and replies, compare engagement signals, and summarize social-media research through Gecho Bridge MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a logged-in X session through Gecho's Chrome extension and MCP server.

Mitigation: Confirm the user understands the browser-extension workflow and has logged in to both Gecho and X before running research tasks.

Risk: Saved JSON research results can contain potentially sensitive local data from X research sessions.

Mitigation: Use a directory the user controls, avoid shared-machine locations, and treat saved result files as sensitive.

## Reference(s):

- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Website](https://gecho.ai/)
- [Gecho Chrome Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw Setup Video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes Setup Video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and links; MCP tool results may include structured JSON files saved locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize X search results, post details, author context, engagement counts, reply themes, setup steps, and saved result paths.]

## Skill Version(s):

1.1.38 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
