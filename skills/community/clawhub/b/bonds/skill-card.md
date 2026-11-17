## Description:

Record bond holdings, analyze yields, and track maturity dates. Use when managing fixed-income portfolios, comparing yields, or exporting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use Bonds to record fixed-income portfolio notes, inspect recent entries, search local logs, and export saved records. Security evidence indicates it should be treated as a simple local logger rather than relied on for bond calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised for bond analysis, but security evidence says it behaves mostly as a broad local logger and does not actually perform the advertised bond calculations.

Mitigation: Use it only when simple local logging is acceptable, and independently verify any bond yields, maturity tracking, or portfolio analysis before relying on it.

Risk: Sensitive portfolio details may be stored as raw local text.

Mitigation: Avoid entering sensitive financial details unless the local machine is trusted, and protect or delete the ~/.local/share/bonds/ data directory according to the user's data-handling requirements.

## Reference(s):

- [Bonds on ClawHub](https://clawhub.ai/bytesagain-lab/skills/bonds)
- [BytesAgain homepage](https://bytesagain.com)
- [BytesAgain ClawHub profile](https://clawhub.ai/user/bytesagain-lab)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text terminal output and local JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local command logs under ~/.local/share/bonds/.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
