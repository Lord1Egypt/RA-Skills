## Description:

Session retrospective and skill audit. Use when asked to reflect, do a retrospective, review lessons learned, audit what went well or wrong, or review session effectiveness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this tool to review a session or skill when asked for a retrospective or audit. It produces evidence-cited findings and prioritized, actionable improvements while observing authorization requirements for memory changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incomplete conversation or artifact evidence can lead to misleading retrospective findings.

Mitigation: State the scope reviewed and any missing or truncated evidence, and cite the specific exchange or artifact for each finding.

Risk: Persisting an inferred lesson without user authorization could retain an incorrect or sensitive memory.

Mitigation: Persist memory only when already authorized or after the user selects concrete items, and exclude credential values.

## Reference(s):

- [Capture and remedy routing](references/capture-and-routing.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown retrospective with evidence citations and prioritized improvement tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [States review scope and evidence gaps; improvements are actionable and prioritized, with no more than 10 items. Memory changes require existing authorization or user selection.]

## Skill Version(s):

5.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
