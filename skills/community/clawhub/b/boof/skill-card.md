## Description:

Boof converts PDFs and documents to Markdown, indexes them locally for RAG retrieval, and helps agents analyze or summarize large documents using targeted chunks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chiefsegundo](https://clawhub.ai/user/chiefsegundo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Boof to convert local PDFs and documents into Markdown, build local RAG collections, and query targeted excerpts for summaries, comparisons, and document analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted file paths may cause unintended Python code execution when processed by the conversion script.

Mitigation: Use the skill only with trusted local file paths, avoid unusual crafted filenames, and prefer a patched version that passes paths as Python arguments.

Risk: Setup instructions install external dependencies without pinned versions or commits.

Mitigation: Pin dependency versions or commits and review upstream packages before installing the skill in managed environments.

## Reference(s):

- [Boof on ClawHub](https://clawhub.ai/chiefsegundo/skills/boof)
- [Boof Advanced Usage](references/advanced-usage.md)
- [Boof Setup Guide](references/setup-guide.md)
- [opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf)
- [QMD](https://github.com/tobi/qmd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, shell commands, configuration snippets, and optional JSON query output from QMD]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local Markdown files in knowledge/boofed by default and QMD collections for retrieval.]

## Skill Version(s):

4.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
