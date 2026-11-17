## Description:

Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangfeng1995](https://clawhub.ai/user/huangfeng1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users can use this skill to install and run blogwatcher commands for tracking RSS/Atom feeds, scanning for updates, listing articles, and marking feed items as read.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path fetches a mutable third-party Go CLI using @latest.

Mitigation: Install only after reviewing and trusting the upstream project; prefer a pinned, reviewed module version or commit for reproducible deployments.

Risk: The skill depends on an external blogwatcher binary being present before commands can run.

Mitigation: Confirm the blogwatcher binary is installed and available on PATH before using the skill's common commands.

## Reference(s):

- [blogwatcher upstream project](https://github.com/Hyaxia/blogwatcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
