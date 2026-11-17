## Description:

Search and compare flight tickets on Ctrip by departure, arrival, date, and cabin class, returning structured flight and price information in JSON format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrew-707](https://clawhub.ai/user/andrew-707)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and travel workflow builders can use this skill to search Ctrip flight listings, compare prices across dates, and collect structured flight data for downstream analysis or display.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill ships and automatically sends a hardcoded Ctrip FVP cookie.

Mitigation: Do not use the bundled cookie; replace it with a disposable runtime secret mechanism before execution.

Risk: The security evidence reports that users are instructed to paste personal browser cookies into source code.

Mitigation: Do not paste personal cookies into tracked files, and avoid committing or sharing any modified script that contains a cookie.

Risk: The security guidance calls for confirming Ctrip terms and privacy implications before use.

Mitigation: Review Ctrip terms, privacy requirements, and organizational policy before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andrew-707/skills/ctrip-flight-sunrise)
- [Ctrip flights](https://flights.ctrip.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included scripts produce structured JSON flight search results and statistics.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
