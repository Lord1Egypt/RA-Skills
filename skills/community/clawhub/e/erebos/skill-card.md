## Description:

Erebos namespace for Netsnek e.U. dark theme and theming engine. Generates accessible dark mode palettes, manages theme tokens, and provides runtime theme switching for web apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

Developers use Erebos to add dark mode support to web applications by generating palette output and theme-token guidance for CSS variables and runtime switching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence assesses the package as non-malicious but unreliable, with advertised accessibility, preview, and export behavior not fully implemented.

Mitigation: Review and test the skill before installation, and independently validate generated theme contrast and build artifacts before relying on them.

Risk: The skill requests command execution and its documented preview behavior may hang or be unsuitable for automation.

Mitigation: Inspect the shell script and run it in a controlled environment before integrating it into automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kleberbaum/skills/erebos)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and CSS or JSON theme-token examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve executable shell-script output; generated accessibility claims should be independently verified before use.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
