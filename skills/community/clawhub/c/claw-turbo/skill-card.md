## Description:

Zero-latency regex-based skill routing middleware for OpenClaw that intercepts known user commands using compiled regex patterns and executes skill scripts directly while forwarding unmatched requests to the local LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacobye2017-afk](https://clawhub.ai/user/jacobye2017-afk)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to route repetitive OpenClaw commands, such as deployments, restarts, log checks, document actions, and local automation, through configured regex routes instead of LLM inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can map ordinary chat phrases to immediate shell or service-management commands.

Mitigation: Require explicit command prefixes and confirmations for state-changing routes before enabling them.

Risk: The release installs remote code that the security evidence describes as unreviewed.

Mitigation: Pin and verify the implementation source before installation, then review configured routes before deployment.

Risk: Command templates can execute with the privileges of the running proxy process.

Mitigation: Run the proxy behind strong local access controls as a dedicated low-privilege user.

Risk: Raw shell templates may execute unintended commands if routes are too broad or captures are unsafe.

Mitigation: Avoid raw shell templates where possible and keep route patterns narrow, explicit, and reviewed.

## Reference(s):

- [claw-turbo GitHub repository](https://github.com/jacobye2017-afk/claw-turbo)
- [ClawHub skill page](https://clawhub.ai/jacobye2017-afk/skills/claw-turbo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce route definitions and command templates that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
