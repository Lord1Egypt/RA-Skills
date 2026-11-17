## Description:

Extract, structure, and summarize Bilibili video/column content into structured notes with timestamps, key points, and chapter indexes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to turn Bilibili videos or columns into note-ready summaries, timestamped key points, chapter indexes, and cross-video digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Follow-up network requests for Bilibili subtitles could exceed the expected fetch scope.

Mitigation: Restrict subtitle and metadata fetches to expected Bilibili hosts before using the skill in sensitive or internal-network environments.

Risk: Local cache and export writes could place files outside the intended workspace.

Mitigation: Run with a contained output directory and review cache/export paths before broad deployment.

Risk: Summary material may be sent to the configured DeepSeek model.

Mitigation: Avoid processing sensitive, private, or internal content unless that model routing is approved for the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/bilibili-digest)
- [Publisher profile](https://clawhub.ai/user/harrylabsj)
- [Reference data README](artifact/references/README.md)
- [Input schema](artifact/schemas/input.schema.json)
- [Output schema](artifact/schemas/output.schema.json)
- [Bilibili video page](https://www.bilibili.com/)
- [Bilibili web interface API](https://api.bilibili.com/x/web-interface/view?bvid={bvid})
- [Bilibili player API](https://api.bilibili.com/x/player/v2?bvid={bvid})

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, guidance]

**Output Format:** [Structured Markdown or JSON containing summaries, timestamps, key points, chapters, resources, action steps, and output file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Markdown, Obsidian Markdown, JSON, and placeholder Notion/Feishu exports; optional transcript inclusion, danmaku analysis, and cross-video merging.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
