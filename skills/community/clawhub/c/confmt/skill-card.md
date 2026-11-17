## Description:

Format, convert, flatten, and diff configuration files with support for JSON, TOML on Python 3.11+, and .env formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect, normalize, convert, and compare configuration files during local development and operations work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The formatter can print values from user-provided .env or configuration files, including secrets.

Mitigation: Avoid running it on secret-bearing files in shared transcripts, logs, or other visible channels.

Risk: Generated env output is shell-style text and may be unsafe to source directly.

Mitigation: Review and sanitize generated env output before using it in a shell or deployment environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and plain-text configuration or diff output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print file contents supplied by the user, including secret-bearing .env values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
