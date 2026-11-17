## Description:

Cn Color Picker helps agents inspect and convert colors with a local Python helper, with current verified behavior focused on 6-digit HEX input converted to RGB, HSL, and HSV output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Designers and front-end developers can use this skill through an agent to convert color values during UI work. The release is best suited for workflows where Chinese-language documentation and command output are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current script is narrower than the documentation advertises and handles direct 6-digit HEX input rather than the documented palette, gradient, or command-style conversions.

Mitigation: Validate expected color operations before relying on the skill, and use it primarily for direct HEX-to-RGB/HSL/HSV conversion unless the artifact is updated.

Risk: Documentation and error output are Chinese-language.

Mitigation: Install and use the skill only in workflows where Chinese-language documentation and output are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freedompixels/skills/cn-color-picker)
- [Publisher Profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON/text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local Python standard-library script with no external dependencies or API keys.]

## Skill Version(s):

1.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
