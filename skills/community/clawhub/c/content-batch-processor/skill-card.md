## Description:

Batch content processing skill for text formatting, summary generation, keyword extraction, multilingual translation, file format conversion, and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[careytian-ai](https://clawhub.ai/user/careytian-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content teams use this skill to process batches of documents for formatting, summarization, keyword extraction, translation, conversion, renaming, and basic content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, PDF, image, edit, and command capabilities for batch document work.

Mitigation: Install and run it only in a constrained workspace with the minimum permissions needed for the current batch task.

Risk: Batch formatting, conversion, and renaming examples can overwrite or move many files at once.

Mitigation: Require confirmation, backups, or a separate output folder before bulk writes, conversions, or renames.

Risk: Generated summaries, keywords, translations, and analysis may be inaccurate or incomplete.

Mitigation: Review generated content before publication or downstream use, especially for research, legal, financial, or customer-facing material.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/careytian-ai/skills/content-batch-processor)
- [Publisher Profile](https://clawhub.ai/user/careytian-ai)
- [Release Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code examples and generated content outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include rewritten files, converted document formats, summaries, keyword lists, translations, renamed files, and content analysis results.]

## Skill Version(s):

1.0.0 (source: metadata.json, config.json, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
