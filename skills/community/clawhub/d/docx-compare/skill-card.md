## Description:

Compares two DOCX files to identify duplicate paragraphs and images, then produces marked DOCX outputs and a text report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmz209](https://clawhub.ai/user/zmz209)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and document reviewers use this skill to compare two Word documents for duplicated text or images during content review, version comparison, or plagiarism checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing untrusted or very large DOCX files may cause resource exhaustion during DOCX parsing or duplicate comparison.

Mitigation: Run the skill in a controlled workspace, avoid very large untrusted DOCX files, and review results before using them in downstream workflows.

Risk: Writing outputs in a directory with important files can create local file-loss risk, especially around generated names such as __tmp_<document>.docx.

Mitigation: Use a dedicated empty output directory and avoid storing important files under names the skill may generate.

## Reference(s):

- [DOCX Compare ClawHub skill page](https://clawhub.ai/zmz209/skills/docx-compare)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; the script produces DOCX files and a plain-text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires two .docx inputs; optional output directory, comparison mode, and fuzzy-match threshold.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
