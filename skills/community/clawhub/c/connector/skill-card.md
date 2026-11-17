## Description:

Deprecated legacy connector skill. Use @launchthatbot/connect-openclaw-plugin for all new LaunchThatBot OpenClaw connect flows with configurable permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[launchthatbot](https://clawhub.ai/user/launchthatbot)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this legacy skill to connect an existing OpenClaw VPS or local deployment to LaunchThatBot for heartbeat, event ingest, replay checks, and live operational visibility. New LaunchThatBot OpenClaw connections should use @launchthatbot/connect-openclaw-plugin instead.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connector handles ingest tokens and telemetry and accepts a configurable base URL, which could expose data or credentials if pointed at an unintended endpoint.

Mitigation: Use only the intended LaunchThatBot HTTPS endpoint, restrict egress to that domain, and avoid plaintext HTTP except for isolated localhost development.

Risk: Secrets may be exposed through command history, logs, terminal output, screenshots, or recordings if passed directly on the command line.

Mitigation: Provide tokens through protected environment injection or a secure secret file, and rotate the ingest token if exposure is suspected.

Risk: This is a deprecated legacy connector and may not be the safest default for new installations.

Mitigation: Prefer @launchthatbot/connect-openclaw-plugin for new installs and review this connector carefully before use.

## Reference(s):

- [ClawHub Connector Listing](https://clawhub.ai/launchthatbot/skills/connector)
- [README.md](artifact/README.md)
- [SECURITY.md](artifact/SECURITY.md)
- [LaunchThatBot Connect Documentation](https://launchthatbot.com/docs/skills/connect)
- [LaunchThatBot Import Documentation](https://launchthatbot.com/docs/skills/import)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operator-facing setup, hardening, validation, and troubleshooting guidance for the connector flow.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
