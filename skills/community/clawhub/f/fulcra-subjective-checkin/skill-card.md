## Description:

Run a short conversational morning check-in that captures mood, energy, social battery, physical state, daily intention, and optional Fulcra sleep and calendar context, then saves the result as structured Fulcra annotations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keng009](https://clawhub.ai/user/keng009)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals using Fulcra with an agent use this skill to conduct a brief morning wellness journal, compare subjective state with sleep and calendar context, and store the result for later reflection or trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles and stores sensitive wellness, physical, sleep, calendar, and intention data.

Mitigation: Use it only in a private user context, avoid sharing check-in details outside Fulcra, summarize calendar context rather than exposing event titles, and ask before saving.

Risk: Runtime Fulcra API and CLI command overrides can change where the helper reads or writes data.

Mitigation: Review FULCRA_API_BASE and FULCRA_CLI_COMMAND before use; prefer the default Fulcra API endpoint and a pinned Fulcra CLI version.

Risk: Fulcra ingest can be eventually consistent, and repeating a save to force confirmation may create duplicate check-in records.

Mitigation: Do not rerun save solely because readback confirmation is delayed; wait for Fulcra Timeline or readback indexing to catch up.

## Reference(s):

- [Fulcra read/write notes](references/fulcra-write-notes.md)
- [Subjective Check-In ClawHub listing](https://clawhub.ai/keng009/skills/fulcra-subjective-checkin)
- [Fulcra API endpoint](https://api.fulcradynamics.com)

## Skill Output:

**Output Type(s):** [text, shell commands, json, guidance]

**Output Format:** [Conversational Markdown with shell commands and JSON helper output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write Fulcra moment and scale annotations after gathering user-provided check-in details.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
