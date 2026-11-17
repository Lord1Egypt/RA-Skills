## Description:

Perform mathematical calculations from the command line. Arithmetic, trig, and unit conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and command-line users use this skill to run quick calculator-style arithmetic and trigonometric expression evaluation from a terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied calculator input is evaluated as unrestricted Python code.

Mitigation: Do not use this version in automated workflows or with expressions from other people; revise it to use a strict math expression parser that rejects imports and attribute access.

Risk: The release claims unit conversion support, but the security guidance says this feature should be implemented or removed before use.

Mitigation: Add tested unit conversion behavior or remove the claim from the skill documentation before relying on the release.

## Reference(s):

- [Calc Tool ClawHub release](https://clawhub.ai/dinghaibin/skills/calc-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI results and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI script defaults to 6 decimal places for floating-point results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
