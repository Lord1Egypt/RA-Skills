## Description:

Use the EdgeFinder CLI for NFL, NBA, and MLB analysis, plus NFL/NBA schedules, standings, Polymarket odds, and portfolio lookups from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewnexys](https://clawhub.ai/user/andrewnexys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to run EdgeFinder CLI commands for sports betting analysis, NFL/NBA schedules and standings, Polymarket odds, and portfolio lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can automatically download and run an unpinned npm CLI through npx when edgefinder is not installed.

Mitigation: Prefer installing and reviewing a pinned EdgeFinder CLI version before use, and avoid relying on the npx fallback in controlled environments.

Risk: The skill uses an EdgeFinder API key or login session for paid access and portfolio data.

Mitigation: Provide only the required EDGEFINDER_API_KEY, avoid printing secrets, and limit environment exposure during agent runs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andrewnexys/skills/edgefinder-cli)
- [EdgeFinder CLI Repository](https://github.com/andrewnexys/edgefinder-cli)
- [Publisher Profile](https://clawhub.ai/user/andrewnexys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-producing CLI invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a locally installed edgefinder binary or fall back to npx; structured commands can request JSON output.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
