## Description:

Deploy Tool is a Bash command-line utility for logging, searching, summarizing, and exporting deployment-related activity entries stored locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to record deployment-related command-line notes, inspect recent activity, search local history, and export logs for operational tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-entered deployment notes are saved as plaintext local logs and exports.

Mitigation: Avoid entering API keys, passwords, tokens, private host details, or other secrets, and review exported files before sharing them.

Risk: The skill may be mistaken for a PHP framework deployment or provisioning tool.

Mitigation: Treat it as a local logging helper for deployment activity, not as an automated deployer or infrastructure provisioning system.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Plain text terminal output with local log files and optional JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries under ~/.local/share/deploy-tool; no external services, databases, or API keys are required.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
