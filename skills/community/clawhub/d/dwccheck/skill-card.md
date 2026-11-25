## Description:

Checks Darwin Core CSV or TSV occurrence files locally for common GBIF issues before upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data publishers use the skill to check a single Darwin Core occurrence file for issues GBIF can detect from the file alone before uploading it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial security scan could not resolve a local path-like reference.

Mitigation: Before installing, check the linked project and its installation instructions, and confirm you trust the source.

## Reference(s):

- [DwC Check on ClawHub](https://clawhub.ai/raktikoo/skills/dwccheck)

## Skill Output:

**Output Type(s):** [text, JSON, CSV]

**Output Format:** [Human-readable findings, JSON, or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include row, flag, severity, term, value, and message, with a summary and verdict.]

## Skill Version(s):

0.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
