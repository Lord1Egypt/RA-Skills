## Description:

Lightweight Dividend tracker. Add entries, view stats, search history, and export in multiple formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill as a local command-line finance logger for recording dividend-related entries, checking summary statistics, searching history, and exporting records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local finance notes and exports that may contain sensitive financial or tax details.

Mitigation: Avoid storing highly sensitive details on shared or unencrypted machines and protect exported files according to the user's data-handling requirements.

Risk: CSV and JSON exports may contain copied or shared input that downstream tools could treat unsafely.

Mitigation: Treat exported files as untrusted when opening or importing them elsewhere, and review copied input before sharing exports.

Risk: The security summary notes privacy and export-safety hardening gaps, including owner-only file permission and escaping concerns.

Mitigation: Prefer a release that sets owner-only file permissions and escapes exported data correctly before use with sensitive records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain3/skills/dividend)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Command-line text output with local JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores records and exports under ~/.local/share/dividend/.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
