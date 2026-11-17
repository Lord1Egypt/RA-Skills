## Description:

Auto Deep Research helps agents investigate research topics by decomposing questions, searching multiple sources, tracking uncertainty and conflicts, and producing structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pancat009](https://clawhub.ai/user/pancat009)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to run structured, multi-source research on concepts, tools, events, trends, and investigative topics. It is intended for research workflows that need source tracking, conflict marking, uncertainty notes, and a final report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts accept caller-provided output paths and can overwrite user-writable files.

Mitigation: Run the skill in a dedicated research output directory and avoid passing custom output paths outside that directory.

Risk: Research topics, search queries, and page URLs may be sent to external search or page-reading services.

Mitigation: Use the skill only for topics and URLs that are acceptable to share with the configured external services.

Risk: The security scanner marked the release suspicious because file-write behavior should be tightened before sensitive use.

Mitigation: Review the package before installing it in sensitive workspaces and constrain file writes during execution.

## Reference(s):

- [Auto Deep Research ClawHub page](https://clawhub.ai/pancat009/skills/auto-deep-research)
- [Source Trust Reference](references/source-trust.md)
- [Conflict Detection Reference](references/conflict-detection.md)
- [Tavily](https://tavily.com)
- [Jina Reader](https://jina.ai/reader)
- [DuckDuckGo Instant Answer API](https://api.duckduckgo.com/?q=query&format=json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown reports plus JSON state, memo, and source files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates an output/{topic-slug}/ folder containing state.json, memo.json, sources.json, and report.md; normal operation uses external search and page-reading services.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
