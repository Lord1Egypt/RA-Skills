## Description:

Lightweight Garmin Connect skill that uses the clawhealth Python package to sync health data into local SQLite and expose JSON-friendly commands for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ernestyu](https://clawhub.ai/user/ernestyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an OpenClaw agent to their Garmin Connect account, sync health metrics into a local SQLite database, and query those metrics through JSON-oriented commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Garmin credentials, session tokens, local SQLite health data, and raw JSON payloads.

Mitigation: Use the password-file flow, restrict file permissions, and keep .env files, password files, config directories, databases, and raw exports out of shared workspaces, backups, and Git.

Risk: The skill may install and run the external clawhealth Python package before accessing sensitive health data.

Mitigation: Install in a trusted isolated environment, review the dependency before use, prefer pinning the package version, and invoke the intended virtualenv executable.

## Reference(s):

- [ClawHealth Garmin on ClawHub](https://clawhub.ai/ernestyu/skills/clawhealth-garmin)
- [clawhealth project homepage](https://github.com/ernestyu/clawhealth)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local health-data query results after the user configures Garmin credentials and completes MFA.]

## Skill Version(s):

0.1.8 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
