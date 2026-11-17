## Description:

Query Atlas Obscura places for unusual location inspiration by coordinates, place ID, or global place coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dougbtv](https://clawhub.ai/user/dougbtv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and creative agents use this skill to retrieve nearby Atlas Obscura places, look up place details, and add unusual location context to travel inspiration, prompts, or worldbuilding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill fetches the Atlas Obscura client and transitive npm dependencies.

Mitigation: Review package-lock.json and install only in environments where npm dependency fetching is acceptable.

Risk: Search coordinates may be sent to the underlying Atlas Obscura data source.

Mitigation: Use approximate coordinates instead of sensitive exact locations when privacy matters.

## Reference(s):

- [Atlas Obscura API Skill on ClawHub](https://clawhub.ai/dougbtv/skills/atlas-obscura-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are limited by command arguments; field availability may vary if the underlying Atlas Obscura data source or client library changes.]

## Skill Version(s):

0.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
