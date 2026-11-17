## Description:

Read CoinFound RWA data from the bundled catalog and schema snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darrenluo](https://clawhub.ai/user/darrenluo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve CoinFound real-world asset data through read-only GET endpoints, using bundled endpoint catalog entries and schema snapshots to shape requests and responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes user-directed requests to CoinFound's API during normal operation.

Mitigation: Review the requested endpoint, path parameters, and query parameters before execution, and avoid sending sensitive values.

Risk: The bundle includes opt-in schema snapshot writing helpers outside the normal read workflow.

Mitigation: Do not run probe_schema.py with --write-snapshot or call write helper functions in environments that require strict no-write behavior.

## Reference(s):

- [CoinFound-Skill release page](https://clawhub.ai/darrenluo/skills/coinfound-skill)
- [darrenluo publisher profile](https://clawhub.ai/user/darrenluo)
- [RWA Read Workflow](references/rwa-read-workflow.md)
- [RWA Read Capabilities](references/rwa-read-capabilities.md)
- [RWA Read Integration Notes](references/rwa-read-integration-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON response examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default fetch output includes request, response_envelope, normalized_data, display_data, shape_family, and schema_source.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
