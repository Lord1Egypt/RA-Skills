## Description:

Calculate addition, subtraction, multiplication and division of two integers via a Python script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bing0109](https://clawhub.ai/user/bing0109)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform basic arithmetic on two integer operands by invoking a local Python calculator script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Use outside the documented arithmetic operations can fail or produce error output instead of a numeric result.

Mitigation: Use only add, sub, mul, or div with two integer operands, and handle nonzero exit codes.

Risk: Division by zero exits with an error rather than returning a numeric value.

Mitigation: Check the divisor before invoking div or handle the script's error status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bing0109/skills/bingo-calculator)
- [ClawHub publisher profile](https://clawhub.ai/user/bing0109)

## Skill Output:

**Output Type(s):** [Shell commands, Text]

**Output Format:** [Plain text numeric output or stderr error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; accepts two integer operands and one operation: add, sub, mul, or div.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
