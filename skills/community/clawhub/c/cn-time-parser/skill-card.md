## Description:

Parses Chinese natural-language time expressions into concrete Gregorian dates and millisecond timestamps, including lunar calendar dates, traditional festivals, and holiday/workday fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[as3long](https://clawhub.ai/user/as3long)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract Chinese time phrases from user requests and convert them into specific dates, timestamps, lunar calendar details, and holiday/workday indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Date, lunar-calendar, holiday, and workday results depend on third-party npm packages and local system time.

Mitigation: Use an accurate system clock, install with the lockfile for reproducibility, and review dependency updates before deployment.

Risk: The skill requires installing and running local Node.js dependencies.

Mitigation: Review npm dependencies before installation and execute the parser in an environment appropriate for third-party code.

## Reference(s):

- [Supported time keywords](references/time-keywords.md)
- [ClawHub skill page](https://clawhub.ai/as3long/skills/cn-time-parser)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON output from the parser script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parser results depend on the current system time and installed npm dependency versions.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
