## Description:

Fetches Amazfit GTR3 health data from HCGateway and writes a daily Obsidian log note.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanwebgit](https://clawhub.ai/user/sanwebgit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch Amazfit GTR3 steps, sleep, heart rate, resting heart rate, SpO2, and distance data from HCGateway and record it as a daily Obsidian health note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles HCGateway credentials and personal health metrics.

Mitigation: Store the runtime config securely, limit file access, and install only where handling these health metrics is acceptable.

Risk: The example configuration can use plaintext HTTP for a remote HCGateway server.

Mitigation: Keep HCGateway on localhost or use HTTPS for remote access before sending credentials or health data.

Risk: The documented recovery path includes sudo Docker commands.

Mitigation: Review Docker commands manually before execution and only run elevated commands in an environment you administer.

Risk: The optional cron entry creates persistent daily health notes in an Obsidian vault.

Mitigation: Enable the cron job only when ongoing local retention of daily health data is intended.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown note file with terminal summary text and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes one daily Markdown health log for the requested date to the configured Obsidian vault.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
