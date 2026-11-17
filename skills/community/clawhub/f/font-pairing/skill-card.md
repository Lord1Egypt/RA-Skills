## Description:

字体搭配推荐、中文字体指南、Web字体加载、标题字体、系统字体栈、预览HTML生成。Font pairing recommendations, Chinese fonts guide, web fonts, heading fonts, system font stacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, developers, and content teams use this skill to generate font pairing recommendations, Chinese font guidance, web font loading advice, system font stacks, and preview HTML for typography decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled helper may save command arguments locally, which could include client names, project codenames, or other sensitive text.

Mitigation: Avoid passing sensitive identifiers as command arguments; review and clear the skill's local data directory before sharing logs or workspaces.

Risk: The package includes broader design-helper commands than the font-focused description suggests.

Mitigation: Review available commands before installation and limit use to expected typography and design-reference workflows.

## Reference(s):

- [Font Pairing ClawHub listing](https://clawhub.ai/ckchzh/skills/font-pairing)
- [BytesAgain homepage](https://bytesagain.com)
- [Font Pairing Tips](artifact/tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and plain text with CSS, HTML, and shell command snippets when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands emit prompt text for an agent to complete; the bundled helper also writes command history under the user's data directory.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
