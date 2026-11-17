## Description:

Convert between Unix epoch timestamps and human-readable datetimes, with timezone support and automatic unit detection (seconds/millis/micros/nanos).

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert log timestamps, current times, and date strings between Unix epoch values and ISO datetimes across IANA timezones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a bundled local Python helper.

Mitigation: Review the helper before execution and run it in a trusted workspace.

Risk: Timezone conversion depends on the local Python runtime and available IANA timezone data.

Mitigation: Use Python 3.9+ with timezone data installed, or restrict conversions to UTC on older runtimes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces timestamp conversion outputs; timezone handling depends on the local Python runtime and available IANA timezone data.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
