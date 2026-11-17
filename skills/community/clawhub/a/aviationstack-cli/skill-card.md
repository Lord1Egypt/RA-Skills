## Description:

Manage AviationStack via CLI for flights, airports, airlines, and routes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melvynx](https://clawhub.ai/user/melvynx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users use this skill to configure and run aviationstack-cli commands for flight, airport, airline, and route lookup through the AviationStack API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute mutable third-party internet installers and link a local command into the user's command environment.

Mitigation: Review and pin referenced tools before installation, and run setup in an isolated environment when possible.

Risk: The AviationStack token is a secret used for outbound API calls and may be stored by the CLI.

Mitigation: Treat the token as sensitive, avoid exposing it in logs or transcripts, and rotate it if accidental disclosure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/melvynx/skills/aviationstack-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API calls, Guidance]

**Output Format:** [Markdown with inline bash commands and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should use --json when called programmatically; output may be JSON, CSV, YAML, or text depending on CLI flags.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
