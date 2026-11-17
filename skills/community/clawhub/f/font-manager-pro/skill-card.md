## Description:

字体管理专业版 helps agents guide font governance workflows for professional frontend and design-system teams, including font pairing, subsetting, design-token integration, accessibility checks, multilingual typography, CDN fallback, and audit reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, design-system maintainers, accessibility engineers, and performance engineers use this skill to plan font-management workflows across CSS and design tokens, CJK typography, font subsetting, CDN fallback, and audit reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trigger and capability claims are broad enough to activate outside font and typography work.

Mitigation: Narrow use to typography tasks before installation and invocation.

Risk: The skill may propose local Python commands and generated file outputs.

Mitigation: Confirm commands before execution and review output paths for generated CSS, font, and report files.

Risk: CDN workflows may involve API keys or callback URLs.

Mitigation: Provide CDN credentials or callback URLs only when required for the workflow, and prefer environment variables for secrets.

## Reference(s):

- [Detailed reference](references/detail.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/font-manager-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, YAML, CSS-oriented examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file outputs such as CSS, font subsets, and HTML, PDF, or JSON audit reports when the agent environment supports them.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
