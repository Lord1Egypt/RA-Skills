## Description:

Figma设计工具包（专业版） helps agents extract Figma design context, variables, screenshots, and assets, then generate structured outputs such as React or Vue component code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, design engineers, and automation teams use this skill to turn authorized Figma files into design tokens, exported assets, screenshots, and framework-oriented component code. It is intended for batch design-to-code and workflow automation tasks where generated output will be reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad command and file access while operating on Figma design data.

Mitigation: Review the skill before installation, run it with least necessary file and command permissions, and confirm where generated code, exported assets, logs, and webhook callbacks will go.

Risk: Figma personal access tokens may be exposed if pasted into examples, config files, logs, or generated outputs.

Mitigation: Use a least-privilege Figma token supplied through environment variables and avoid storing real tokens in prompts, examples, or project files.

Risk: Generated code, exported assets, and design tokens may include proprietary or sensitive design information.

Mitigation: Use the skill only with Figma files the operator is allowed to process, and review outputs before sharing, committing, or deploying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/figma-toolkit-pro)
- [Figma REST API](https://api.figma.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with code blocks, JSON responses, configuration examples, and generated component code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include design tokens, exported asset instructions, generated UI component code, execution logs, and error details.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
