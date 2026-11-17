## Description:

Scans React, TSX, and HTML projects for missing or incorrect accessibility labels and can report or repair issues such as unlabeled icon buttons, non-semantic click targets, weak image alt text, unlabeled form controls, dialog labeling gaps, live-region issues, and cross-platform ARIA compatibility risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ityhg](https://clawhub.ai/user/ityhg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and front-end engineers use this skill to audit React, TSX, HTML, Next.js, Tauri, browser extension, and embedded WebView projects for accessibility-label defects. It helps produce grouped audit findings and candidate code fixes for WCAG-oriented accessibility improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically change accessibility-related code across a broad default scope.

Mitigation: Use explicit target paths, request report-only or dry-run behavior first, and review diffs before accepting changes.

Risk: Automatically inferred aria-label or alt text can misrepresent UI intent.

Mitigation: Review generated labels and alt text with product context before merging code changes.

## Reference(s):

- [Detailed Rule Reference](artifact/reference.md)
- [Repair Examples](artifact/examples.md)
- [Usage Guide](artifact/USAGE.md)
- [ClawHub Skill Listing](https://clawhub.ai/ityhg/skills/a11y-label-audit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown audit reports with tables, suggested fixes, and candidate code edits or commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit project files when asked to apply fixes; review generated diffs before accepting changes.]

## Skill Version(s):

1.0.0 (source: release evidence, clawhub.json, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
