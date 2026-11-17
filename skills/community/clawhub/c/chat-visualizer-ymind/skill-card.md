## Description:

YMind Chat Visualizer turns AI chat transcripts from shared links or pasted text into interactive D3.js thinking maps with reasoning nodes, thinking shifts, and action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yslenjoy](https://clawhub.ai/user/yslenjoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to visualize AI assistant conversations, extract reasoning paths, identify friction points and thinking shifts, and capture action items for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full chat transcripts and derived graph data are saved locally by default.

Mitigation: Use the skill only with non-sensitive conversations, set YMIND_DIR to an appropriate private workspace, and review or delete ~/ymind-ws outputs after use.

Risk: Generated HTML may contact third-party CDNs for visualization libraries and fonts.

Mitigation: Open generated HTML only in trusted environments and avoid rendering sensitive chats until CDN and HTML handling risks are reviewed.

Risk: The authoritative scan reports review-level concerns around HTML escaping, index rendering, helper discovery, and dependency pinning.

Mitigation: Prefer paste mode with non-sensitive content and defer use on credentials, private business data, or untrusted shared-chat links until those issues are fixed.

## Reference(s):

- [YMind Graph Schema Reference](references/graph-schema.md)
- [ClawHub skill page](https://clawhub.ai/yslenjoy/skills/chat-visualizer-ymind)
- [Publisher profile](https://clawhub.ai/user/yslenjoy)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML files, shell commands, configuration, guidance]

**Output Format:** [Markdown summary plus local graph.json, graph.html, optional graph.png, raw_chat.json, meta.json, index.json, and index.html files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are saved locally under YMIND_DIR, defaulting to ~/ymind-ws; URL fetching and screenshot generation require optional requests and Playwright dependencies.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
