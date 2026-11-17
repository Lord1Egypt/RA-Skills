## Description:

Personal content collection and knowledge management skill for saving, organizing, searching, and repurposing content from webpages, social posts, and videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to collect URLs and media into structured local Markdown notes, maintain searchable indexes and tags, sync optionally to Obsidian, and retrieve saved material for later writing or repurposing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save collected content locally and optionally sync it to an Obsidian vault.

Mitigation: Confirm collection and Obsidian paths before use, avoid collecting sensitive material unintentionally, and require explicit consent before writing to a vault.

Risk: Video collection workflows may use browser cookies or authenticated media retrieval.

Mitigation: Review or disable cookie access before video workflows and only process media URLs from trusted sources.

Risk: Local video-transcription scripts and media filenames can introduce execution and dependency risk.

Mitigation: Run helper scripts in a controlled workspace, avoid untrusted local media filenames, and prefer pinned dependencies for transcription tooling.

Risk: Article image downloads and external extraction APIs can expose URLs or content to third-party services.

Mitigation: Review configured extraction services and API keys, and use fallback local or browser-based extraction when content should not be sent to an external service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lovensky1992-wk/skills/content-collector)
- [URL Routing and Site Specs](references/url-routing-and-site-specs.md)
- [Schema Extraction Spec](references/schema-extraction-spec.md)
- [Image Extraction Spec](references/image-extraction-spec.md)
- [Theme Extraction Spec](references/theme-extraction-spec.md)
- [Highlight Extraction Spec](references/highlight-extraction-spec.md)
- [Content Overview Spec](references/content-overview-spec.md)
- [Obsidian Integration](references/obsidian-integration.md)
- [Bilibili Comments Extraction](references/bilibili-comments.md)
- [Evaluation Benchmark](evals/benchmark.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown collection notes with YAML frontmatter, structured summaries, indexes, tags, Mermaid diagrams when applicable, and inline shell commands for helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local collection files and optional Obsidian copies; helper scripts may emit JSON metadata or transcripts.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
