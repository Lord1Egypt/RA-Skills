## Description:

Converts RSS feeds into Markdown archives with batch processing, custom templates, AI-assisted summaries and keywords, scheduled archiving, multiple export formats, image downloading, full-text retrieval, and deduplication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and knowledge-management teams use this skill to convert and archive RSS or Atom feeds as Markdown or other document formats, with optional LLM-generated summaries and keyword metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch untrusted RSS content and write archive or export files to local paths.

Mitigation: Use trusted feeds, review configured output paths, and keep generated files in a dedicated working folder.

Risk: Scheduled archiving can repeatedly process feeds or write files before paths and cadence are reviewed.

Mitigation: Keep scheduled archiving disabled until the feed list, output directory, and schedule have been explicitly checked.

Risk: PDF and EPUB conversion examples rely on local conversion tools that may process untrusted content.

Mitigation: Sandbox or skip document conversion for untrusted feeds and review conversion tool behavior before enabling it.

Risk: AI content enhancement can produce inaccurate summaries, keywords, or tags.

Mitigation: Review generated summaries and metadata before using them for business records or downstream publication.

## Reference(s):

- [Detailed Reference](references/detail.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code, shell, configuration, and structured JSON-style result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local archives or exports and may call an LLM or local conversion tools when the agent follows the examples.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
