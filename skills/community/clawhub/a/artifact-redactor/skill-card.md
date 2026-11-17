## Description:

Public OpenClaw skill for redacting private paths, secret-like strings, private URLs, and common PII from Markdown, JSON, logs, and other text artifacts before sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare text artifact bundles for sharing by scanning for obvious sensitive text, producing redacted copies, checking the redacted output, and generating a concise review report. It is aimed at Markdown, JSON, logs, YAML, CSV, shell output, and similar text files, with unsupported or binary files left for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Symlinks in the selected artifact tree may cause files outside that tree to be read and included in a share bundle.

Mitigation: Run the skill only on artifact trees you control, check for symlinks before processing, and review the generated report and output tree before sharing.

Risk: The redacted output may still require manual review, especially for skipped binary or unsupported files.

Mitigation: Treat skipped files, symlinks, and any manual-review-required or fix-required check result as blockers before public sharing.

## Reference(s):

- [Artifact Redactor ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/skills/artifact-redactor)
- [Artifact Redactor Project Homepage](https://github.com/zack-dev-cm/artifact-redactor)

## Skill Output:

**Output Type(s):** [Shell commands, Files, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; bundled scripts produce JSON reports, redacted text files, and a Markdown report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.9+. Automatic redaction is limited to supported text files; binary and unsupported files require manual review.]

## Skill Version(s):

1.0.7 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
