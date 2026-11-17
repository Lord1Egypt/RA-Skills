## Description:

Meeting Cadence Optimizer analyzes a user's Fulcra evening debrief and morning check-in history to correlate meeting count with day ratings and recommend a confidence-gated meeting cadence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keng009](https://clawhub.ai/user/keng009)

### License/Terms of Use:

MIT-0

## Use Case:

People who track Fulcra daily reflections use this skill to ask their agent whether their meeting load is harming day quality and to get concise cadence recommendations based on logged evening debrief and morning check-in data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses personal Fulcra reflection history, including meeting counts, day ratings, cadence feedback, and morning check-in data.

Mitigation: Keep outputs private, use the read-only analyze command first, and share only the returned aggregate numbers needed for the cadence decision.

Risk: The package includes broad credential-using Fulcra and CRM helper scripts beyond the stated meeting-cadence purpose.

Mitigation: Review before installing, require explicit approval for save mode or weekly automation, pin the Fulcra CLI version, avoid API base or CLI command overrides unless trusted, and do not provide an Attio API key unless that helper surface is intentionally needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keng009/skills/fulcra-meeting-cadence-optimizer)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, shell commands, guidance]

**Output Format:** [JSON from the cadence script, with agent-facing markdown or plain-text recommendations derived from returned fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only analyze mode is available; optional save mode writes a Cadence Analysis Fulcra annotation when explicitly used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
