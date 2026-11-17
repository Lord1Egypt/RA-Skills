## Description:

Convert Unix timestamps, date/time strings, time zones, date arithmetic, and durations using a bundled standard-library Python helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzzqiuchan](https://clawhub.ai/user/zzzqiuchan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert timestamps, date strings, time zones, spreadsheet serials, relative times, and durations without doing manual time math.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Naive date/time inputs can be interpreted in the machine's local time zone and produce an off-by-hours result.

Mitigation: Use an explicit input time zone with --in-tz and include the output time zone in user-facing answers.

Risk: Optional timezone-data installation can introduce package-supply-chain risk if pulled from an untrusted source.

Mitigation: Install optional timezone packages only from a trusted package index, preferably inside a virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzzqiuchan/skills/datetime-convert)
- [Publisher profile](https://clawhub.ai/user/zzzqiuchan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline shell commands and date/time values; optional JSON when the bundled script is invoked with --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should include explicit time zones when time zone context affects correctness.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
