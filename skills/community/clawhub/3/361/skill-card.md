## Description:

Scan installed skills to inspect a specific skill directory or list available skills with names and descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OpenClaw skill directories, enumerate installed skills, and review basic SKILL.md metadata before installation or maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags an unpinned external pip package and unexplained safety scores.

Mitigation: Install only in an isolated environment, prefer a version-pinned package or bundled auditable source, and do not trust SAFE scores until independently verified.

Risk: The skill scans local skill directories and may be pointed at unrelated private directories.

Mitigation: Limit scans to intended skill directories and avoid paths containing unrelated private or sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/361)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and plain-text scan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports skill names, paths, descriptions, and scan status details when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
