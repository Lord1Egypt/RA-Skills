## Description:

Config Diagnose helps agents diagnose configuration, environment variable, service, file, and skill installation issues and return troubleshooting suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongrebeccahhh-boop](https://clawhub.ai/user/dongrebeccahhh-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to investigate why mail, API, service, file, or installed-skill configuration is not working. It can run diagnostic shell scripts, summarize detected issues, and suggest concrete remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic output may expose local secrets or system details, including API key prefixes, process details, file paths, installed skill names, and memory metadata.

Mitigation: Run only in environments where diagnostic output can be safely exposed, and review or redact logs before sharing them.

Risk: The IMAP server connection check uses an unsafe shell command pattern that could execute unintended commands when EMAIL_IMAP_SERVER is crafted maliciously.

Mitigation: Review and fix the IMAP command invocation before use, and avoid running the email diagnostic with untrusted environment variable values.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown and terminal diagnostic output with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local diagnostic details such as environment variable names, API key prefixes, process information, service ports, and file paths.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
