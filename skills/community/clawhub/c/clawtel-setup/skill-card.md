## Description: <br>
Use when setting up clawtel to report token usage from a project that calls the Anthropic API, Claude Code, or any tapes-wrapped agent to the claw.tech leaderboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bdougie](https://clawhub.ai/user/bdougie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and configure clawtel, route Anthropic traffic through tapes, set required environment variables, verify heartbeat delivery, and optionally run telemetry as a persistent service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup routes Anthropic calls through tapes and enables telemetry to claw.tech. <br>
Mitigation: Review the disclosed data flow before installation and confirm the user is comfortable sending aggregate token usage data. <br>
Risk: The setup installs an external clawtel binary. <br>
Mitigation: Prefer the pinned release path and verify the release checksum before placing the binary on PATH. <br>
Risk: CLAW_INGEST_KEY is a credential required for network calls. <br>
Mitigation: Store CLAW_INGEST_KEY only in the intended shell or service environment and protect service environment files with restrictive permissions. <br>
Risk: Running clawtel as a persistent systemd service can keep telemetry active across restarts. <br>
Mitigation: Enable the service only after reviewing the telemetry behavior and confirming the configured TAPES_DB points to the intended SQLite database. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bdougie/clawtel-setup) <br>
- [clawtel GitHub repository](https://github.com/bdougie/clawtel) <br>
- [clawtel releases](https://github.com/bdougie/clawtel/releases) <br>
- [clawtel install script](https://raw.githubusercontent.com/bdougie/clawtel/main/scripts/install.sh) <br>
- [claw.tech](https://claw.tech) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, SQL, and systemd configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, verification checks, troubleshooting guidance, and security footprint notes.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
