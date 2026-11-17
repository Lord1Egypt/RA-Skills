## Description:

Cn Timestamp Tool is a pure-Python timestamp conversion utility that requires no API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert Unix timestamps and date-time strings, get current timestamps in seconds or milliseconds, and format timestamp output with timezone support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Timezone defaults may produce unexpected conversions for users who do not intend Asia/Shanghai time.

Mitigation: Confirm the intended timezone and pass it explicitly when converting or formatting timestamps.

Risk: Chinese documentation and help text may be harder for non-Chinese reviewers or operators to assess.

Mitigation: Use translation or bilingual review before deployment in teams that do not read Chinese.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-timestamp-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text timestamp or date output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python standard library behavior; default timezone is Asia/Shanghai unless overridden where the CLI supports it.]

## Skill Version(s):

1.2.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
