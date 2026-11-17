## Description:

Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vickk1ng](https://clawhub.ai/user/vickk1ng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to install and operate the blogwatcher CLI for tracking RSS, Atom, and blog updates from local shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs blogwatcher from an unpinned Go module version.

Mitigation: Install only after trusting the upstream project; prefer a pinned module version when available and review the CLI before use in environments with sensitive local files or credentials.

## Reference(s):

- [Blogwatcher Local on ClawHub](https://clawhub.ai/vickk1ng/skills/blogwatcher-local)
- [blogwatcher GitHub repository](https://github.com/Hyaxia/blogwatcher)
- [Go install module](https://pkg.go.dev/github.com/Hyaxia/blogwatcher/cmd/blogwatcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on blogwatcher CLI installation and common commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
