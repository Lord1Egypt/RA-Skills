## Description: <br>
Extract, structure, and summarize Bilibili video/column content into structured notes with timestamps, key points, and chapter indexes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn Bilibili videos or columns into structured notes, summaries, timestamped key points, chapter outlines, and cross-video digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bilibili content is fetched, cached locally, and written into note files. <br>
Mitigation: Use the skill only for content you are comfortable storing locally, choose an appropriate output directory, and clear the local cache when retention is not desired. <br>
Risk: Video content, transcripts, danmaku, or pasted enrichment notes may be summarized by the configured LLM runtime. <br>
Mitigation: Avoid private notes or sensitive pasted context unless the configured model runtime is approved for that data. <br>
Risk: When subtitles are missing, summaries may rely on metadata, descriptions, danmaku, or user-provided notes. <br>
Mitigation: Review generated summaries against the source video before relying on them for decisions or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/bilibili-digest) <br>
- [Publisher profile](https://clawhub.ai/user/harrylabsj) <br>
- [Reference README](artifact/references/README.md) <br>
- [Export presets](artifact/references/presets.json) <br>
- [Video categories](artifact/references/video-categories.json) <br>
- [Danmaku stopwords](artifact/references/stopwords.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown, Obsidian-flavored Markdown, JSON, or prepared Notion/Feishu export content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include title, author, duration, view count, AI-generated summary, timestamped key points, chapters, resources, action steps, markdown content, and an output file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
