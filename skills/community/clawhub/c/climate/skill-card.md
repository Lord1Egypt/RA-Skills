## Description:

Climate is a command-line utility that records local command inputs and provides status, search, statistics, and export functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill as a local CLI logging utility for simple entries, status checks, search, statistics, and data export. Reviewed evidence indicates it should not be treated as a climate data analysis toolkit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact presents itself as a climate toolkit, but the included script mainly logs arbitrary local command inputs and can replay or export them.

Mitigation: Install only if you intentionally want a local command-input logging utility, and evaluate the behavior against the intended climate use case before deployment.

Risk: Locally retained command entries may include secrets, credentials, private notes, or sensitive business data if users enter them.

Mitigation: Do not enter sensitive data, review ~/.local/share/climate after testing, and clear retained logs and exports when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/climate)
- [Publisher homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output with optional JSON, CSV, or text exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores command entries and exports under ~/.local/share/climate by default.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
