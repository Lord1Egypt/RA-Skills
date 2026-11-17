## Description:

Installs and manages Expert Library Plus, an OpenClaw expert library that uses name-based quality anchors and templates for expert guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kalluche](https://clawhub.ai/user/kalluche)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, verify, update, and manage an expert library with name templates and cross-platform setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer persistently modifies OpenClaw expert files under ~/.openclaw/experts.

Mitigation: Review the package before installing, install only from a trusted location, and keep backups of ~/.openclaw/experts.

Risk: The verifier is invoked through an unsafe shell-based call.

Mitigation: Prefer a fixed installer that invokes the verifier with subprocess.run using an argument list.

Risk: Existing expert or name-library files could be overwritten during installation.

Mitigation: Ask before overwriting user-created expert or name-library files and preserve timestamped backups.

## Reference(s):

- [Project homepage](https://github.com/kalluche/expert-library-plus)
- [ClawHub skill listing](https://clawhub.ai/kalluche/skills/expert-library-plus-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and file path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installation status, verification results, troubleshooting steps, and cross-platform path notes.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
