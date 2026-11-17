## Description:

Converts a codebase into an offline Chinese interactive HTML course, with a product-manager mode for business flows and a developer mode for architecture, data flow, and technical explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouchang1988](https://clawhub.ai/user/zhouchang1988)

### License/Terms of Use:

MIT

## Use Case:

Developers, product managers, and technical educators use this skill in Claude Code to turn local or GitHub code repositories into Chinese, offline-ready interactive browser courses for business or technical onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated interactive HTML may run injected browser code when untrusted repository content is incorporated into unsafe browser-rendered content.

Mitigation: Use trusted repositories, inspect generated module HTML before opening index.html, and add strict escaping or sanitization before using the skill with untrusted input.

Risk: The skill reads the target repository and writes a generated course directory.

Mitigation: Run it in a controlled workspace and review generated files before sharing, opening, or deploying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouchang1988/skills/codebase-to-course-cn)
- [README](README.md)
- [Design system overview](DESIGN.md)
- [Product-manager content philosophy](references/content-philosophy.md)
- [Developer content philosophy](references/content-philosophy-pro.md)
- [Design system reference](references/design-system.md)
- [Interactive elements reference](references/interactive-elements.md)
- [Common gotchas](references/gotchas.md)
- [Module brief template](references/module-brief-template.md)
- [Inspiration project link from README](https://github.com/zarazhangrui/codebase-to-course)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance plus generated HTML, CSS, JavaScript, shell script, and assembled browser course files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a course directory named from user-provided keywords and version mode; generated courses are intended to run offline.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
