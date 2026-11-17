## Description:

Document Diff compares two supported documents by parsing both with SoMark and producing structured Markdown and JSON diff outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soul-code](https://clawhub.ai/user/soul-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, reviewers, and external users use this skill to compare versions of contracts, reports, policies, presentations, images, or other supported documents and summarize meaningful additions, removals, and unchanged sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compared documents are sent to SoMark for parsing.

Mitigation: Use the skill only when external processing by SoMark is approved for the document contents.

Risk: Parsed Markdown and diff reports are saved locally in plaintext.

Mitigation: Write outputs to an approved location, restrict access to the output directory, and remove generated files when they are no longer needed.

## Reference(s):

- [Document Diff on ClawHub](https://clawhub.ai/soul-code/skills/document-diff)
- [SoMark Login](https://somark.tech/login)
- [SoMark Workbench](https://somark.tech/workbench/purchase)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown summaries, Markdown diff reports, JSON metadata, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOMARK_API_KEY; writes parsed Markdown files, diff_report.md, and diff_summary.json to a local output directory.]

## Skill Version(s):

0.1.2 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
