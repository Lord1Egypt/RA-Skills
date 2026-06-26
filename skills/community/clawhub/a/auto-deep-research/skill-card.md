## Description: <br>
Automatically decomposes research questions, searches and reads sources, verifies findings across multiple independent sources, and writes structured research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pancat009](https://clawhub.ai/user/pancat009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to investigate technical concepts, compare tools, track trends, and produce evidence-backed research reports with source notes and uncertainty markers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries and selected URLs may be sent to external search or page-reading services. <br>
Mitigation: Use limited-scope API keys, avoid private or token-bearing URLs, and choose external services only when their terms fit the research task. <br>
Risk: Saved research folders can retain notes, source summaries, and reports that may contain sensitive task context. <br>
Mitigation: Keep output folders out of version control and delete saved research notes when they are no longer needed. <br>


## Reference(s): <br>
- [Source Trust Reference](references/source-trust.md) <br>
- [Conflict Detection Reference](references/conflict-detection.md) <br>
- [Tavily](https://tavily.com) <br>
- [Jina Reader](https://jina.ai/reader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown reports plus JSON state, memo, and source files; may include shell commands for search and page reading.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates output/{topic-slug}/ with state.json, memo.json, sources.json, and report.md; default maximum of 5 search iterations.] <br>

## Skill Version(s): <br>
0.0.1 (source: server evidence release.version and README version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
