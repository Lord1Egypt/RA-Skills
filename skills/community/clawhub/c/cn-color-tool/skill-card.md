## Description:

Cn Color Tool is a pure-Python command-line utility for converting colors between HEX, RGB, and HSL formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert color values between HEX, RGB, and HSL and to generate terminal-friendly color conversion output for design or implementation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation examples call cn_color_tool.py, while the artifact stores the executable script at scripts/color_tool.py.

Mitigation: Call the bundled scripts/color_tool.py path directly or create an explicit local alias before following the examples.

Risk: The artifact documentation includes promotional external links unrelated to the color conversion function.

Mitigation: Avoid opening promotional links unless the destination is trusted and needed for the deployment context.

Risk: The user-facing documentation is primarily Chinese-language.

Mitigation: Install only where Chinese-language documentation and command help are acceptable for operators.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-color-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python standard library color conversion logic and emits terminal-readable color values.]

## Skill Version(s):

1.2.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
