## Description:

Analyzes local GHIN golf JSON data to report handicap trends, scoring patterns, course stats, and yearly performance without external connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT License

## Use Case:

Golfers and agents use this skill to analyze an already-collected GHIN JSON file and produce handicap, scoring, course, and yearly performance summaries. It is suited for local, credential-free review of personal golf statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GHIN data can include personal golf activity and performance history.

Mitigation: Provide only the local GHIN JSON file intended for analysis and avoid sharing generated reports beyond the intended audience.

Risk: Credential-based GHIN data collection is outside this skill and may require separate browser automation.

Mitigation: Review any data collection workflow independently; this skill should only analyze pre-collected JSON data.

Risk: Malformed or incomplete input data can produce incomplete or misleading statistics.

Mitigation: Use JSON files with the expected GHIN fields and review the generated report before relying on trends or summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pfrederiksen/skills/ghin-golf-tracker)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable text report or JSON printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads one local GHIN JSON input file and does not write files.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
