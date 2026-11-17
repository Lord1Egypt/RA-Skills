## Description:

Controls a Roon music system through API calls for library and TIDAL search, playback, queue management, volume, shuffle, playlists, and zone status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wegow](https://clawhub.ai/user/wegow)

### License/Terms of Use:

MIT-0

## Use Case:

External users or personal automation agents use this skill to control a configured Roon music system, including finding music, starting playback, managing queues, adjusting volume, and checking playback state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release bundles unrelated long-term memory and credential-location guidance beyond the Roon control use case.

Mitigation: Remove MEMORY.md or ensure it cannot be imported as trusted memory before installation.

Risk: Broad activation language could make the skill run for casual or ambiguous music requests.

Mitigation: Narrow activation to explicit Roon-control requests.

Risk: Playback actions can clear queues or change volume.

Mitigation: Require user confirmation before queue-clearing playback actions or volume changes.

Risk: Hardcoded local hostnames and zone IDs may expose private configuration or fail outside the original environment.

Mitigation: Replace hostnames and zone IDs with local configuration before use.

Risk: Unauthenticated or broadly reachable Roon API access could allow unintended media control.

Mitigation: Protect the Roon API with authentication or network isolation.

## Reference(s):

- [ARCHIV ClawHub skill page](https://clawhub.ai/wegow/skills/archiv)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON request examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Roon API base URL and zone configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
