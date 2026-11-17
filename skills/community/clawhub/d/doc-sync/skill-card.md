## Description:

Context-Aware Doc Generator: Automatically syncs Python docstrings (Google style), Go comments, and README.md based on code changes. Also logs change summaries to a local KB/ChromaDB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shangter666](https://clawhub.ai/user/shangter666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use doc-sync to keep Python docstrings, Go comments, and README API or usage sections aligned with code changes, and to record concise local change summaries for later retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation or README updates may introduce incorrect or misleading guidance if applied without review.

Mitigation: Review proposed docstring, comment, and README edits before applying them.

Risk: Knowledge-base logging may store change summaries and file paths locally under .gemini.

Mitigation: Do not log secrets or sensitive content unless local retention is acceptable.

## Reference(s):

- [Documentation Styles](references/doc_styles.md)
- [Google Python Style Guide: Comments and Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [Effective Go: Commentary](https://golang.org/doc/effective_go.html#commentary)
- [Go Doc Comments](https://go.dev/doc/comment)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown and code edits with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSONL or ChromaDB knowledge-base records when the KB logging workflow is used.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
