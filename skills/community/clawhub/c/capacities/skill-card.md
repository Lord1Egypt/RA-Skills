## Description:

Manage Capacities notes, daily entries, and weblinks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidsmorais](https://clawhub.ai/user/davidsmorais)

### License/Terms of Use:


## Use Case:

External Capacities users use this skill to ask an agent to add notes, tasks, thoughts, and weblinks to a Capacities space, search for object IDs, and retrieve space information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe value substitution in shell examples could run unintended local commands.

Mitigation: Review generated commands before running them and avoid pasting arbitrary note text directly into shell command source.

Risk: The skill requires access to a private Capacities API token.

Mitigation: Use only your own Capacities account and keep CAPACITIES_API_TOKEN private.

Risk: Interpolating user content into curl JSON payloads can break request structure or alter command behavior.

Mitigation: Prefer structured JSON construction or an HTTP client that escapes user-provided content safely.

## Reference(s):

- [Capacities skill page](https://clawhub.ai/davidsmorais/skills/capacities)
- [Capacities publisher profile](https://clawhub.ai/user/davidsmorais)
- [Capacities save-to-daily-note API endpoint](https://api.capacities.io/save-to-daily-note)
- [Capacities save-weblink API endpoint](https://api.capacities.io/save-weblink)
- [Capacities lookup API endpoint](https://api.capacities.io/lookup)
- [Capacities space-info API endpoint](https://api.capacities.io/space-info)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAPACITIES_API_TOKEN; CAPACITIES_SPACE_ID is optional and defaults to the first available space when omitted.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
