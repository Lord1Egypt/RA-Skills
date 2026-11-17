## Description:

Cn Math Calculator helps agents safely evaluate mathematical expressions and convert common units for Chinese-language math workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to calculate arithmetic and scientific expressions, return optional JSON results, and perform common length, weight, temperature, and area conversions with Chinese and English unit names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted public input could submit very long expressions, very large numeric operations, or calculations that take excessive execution time.

Mitigation: Use expression length, numeric-size, and execution-time limits before exposing the calculator to public traffic.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-math-calculator)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON, often with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python standard library math evaluation and unit conversion logic.]

## Skill Version(s):

1.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
