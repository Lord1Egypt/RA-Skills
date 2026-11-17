## Description:

Color Toolkit helps agents convert colors, check WCAG contrast, generate palettes, manipulate colors, mix colors, create random colors, and look up CSS named colors from a local Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and accessibility reviewers use this skill when they need quick local color conversion, palette generation, CSS color lookup, or WCAG contrast checks during design and implementation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided color arguments are parsed and executed by a local CLI.

Mitigation: Review command arguments before execution and use normal CLI hygiene; the server security evidence reports no network behavior, persistence, credential handling, or special sensitive permissions.

Risk: Contrast and palette output may inform accessibility or design decisions.

Mitigation: Review generated colors and WCAG contrast results against project requirements before applying them in production interfaces.

## Reference(s):

- [Color Toolkit on ClawHub](https://clawhub.ai/johnnywang2001/skills/color-toolkit)
- [johnnywang2001 publisher profile](https://clawhub.ai/user/johnnywang2001)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Terminal text or JSON from local CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured JSON output is available with --json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
