## Description:

Display, set, and manage environment variables in shell sessions. Use when inspecting or modifying the runtime environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Env Tool to inspect runtime environment variables and check specific values while troubleshooting shell sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default all-variable listing can print raw environment values into terminal output, agent transcripts, or logs, exposing secrets.

Mitigation: Prefer querying specific non-sensitive variables and avoid broad listings in environments that may contain credentials or tokens.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain text environment-variable output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw environment variable values; avoid broad output capture in logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
