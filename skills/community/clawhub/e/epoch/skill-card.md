## Description:

Convert Unix timestamps, compare epochs, and do time arithmetic. Use when converting dates, debugging timestamps, or checking timezone offsets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Epoch to convert Unix timestamps, parse date strings, compare epoch values, and perform simple time arithmetic while debugging logs or checking timezone offsets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Date parsing and local time display depend on the host system date implementation and timezone.

Mitigation: Use explicit timezone input or UTC output when comparing results across systems.

Risk: The skill invokes a local Bash utility that passes user-provided date strings to standard system date parsing.

Mitigation: Review date inputs before execution and run the utility in a normal local environment; the security evidence reports no network or sensitive data handling.

## Reference(s):

- [Epoch on ClawHub](https://clawhub.ai/bytesagain3/skills/epoch)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local timestamp output depends on the host system date implementation and timezone.]

## Skill Version(s):

3.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
