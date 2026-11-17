## Description:

Checks whether the locally installed Claude Code binary contains near-invisible Unicode apostrophe markers in the system-prompt date line and guides an approved upgrade when affected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwbwin](https://clawhub.ai/user/wwbwin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit a local Claude Code installation for documented Unicode date-line marker behavior and decide whether to run the provided remediation command with explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional remediation can globally upgrade Claude Code from the mutable npm latest tag.

Mitigation: Run the audit first; use upgrade_cc.py --apply only after explicit approval, and prefer verifying or pinning the exact Claude Code version.

## Reference(s):

- [Known versions and Unicode marker signals](artifact/references/known_versions.md)
- [ClawHub skill page](https://clawhub.ai/wwbwin/skills/claude-code-unicode-audit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON audit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit exits with CLEAN or AFFECTED/SUSPECT status; remediation is dry-run by default unless --apply is explicitly used.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
