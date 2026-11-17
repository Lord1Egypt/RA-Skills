## Description:

Convert colors and generate palettes with WCAG contrast checks for palette building, hex/RGB conversion, and accessibility checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use ColorLab to convert color formats, generate palette variants, check WCAG contrast ratios, and identify nearby CSS color names from a terminal workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Numeric arguments may permit command injection when supplied from untrusted input.

Mitigation: Validate numeric arguments as decimal integers, reject non-numeric values before arithmetic or awk evaluation, and bound count parameters before release.

Risk: Users may run the local shell helper before reviewing a suspicious security verdict.

Mitigation: Review the shell script and avoid untrusted color or count input until the numeric validation issue is fixed.

## Reference(s):

- [Colorlab ClawHub listing](https://clawhub.ai/bytesagain3/skills/colorlab)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal text and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include ANSI 24-bit color swatches when used in a modern terminal.]

## Skill Version(s):

3.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
