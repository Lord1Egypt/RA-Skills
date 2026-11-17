## Description:

Command-line tool to search flight prices using the Duffel API with options for dates, passengers, stops, and cabin class.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrojas537](https://clawhub.ai/user/jrojas537)

### License/Terms of Use:

MIT

## Use Case:

Agents, developers, and travelers use Flight Pricer to configure a Duffel API key and search flight offers by route, date, passenger count, stop count, and cabin class from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a Duffel API key that may have billing or account privileges.

Mitigation: Prefer entering the key through a hidden prompt, environment variable, or credential store, and restrict ~/.config/flight-pricer/config.yaml to the local user only.

Risk: Runtime dependencies are not pinned in the artifact.

Mitigation: Install in an isolated virtual environment and consider pinning dependencies before use.

## Reference(s):

- [Flight Pricer on ClawHub](https://clawhub.ai/jrojas537/skills/flight-pricer)
- [Duffel](https://duffel.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text CLI output with tabular flight offers, status messages, and error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes Duffel API key configuration to ~/.config/flight-pricer/config.yaml when configured.]

## Skill Version(s):

1.0.1 (source: server release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
