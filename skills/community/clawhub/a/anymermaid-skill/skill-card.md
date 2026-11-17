## Description:

Anymermaid helps agents create Mermaid diagrams and render them with the mmdc CLI as SVG, PNG, or PDF files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyforge](https://clawhub.ai/user/anyforge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and agents use this skill to turn processes, architectures, timelines, data relationships, and other structured concepts into Mermaid diagrams and rendered image or document files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags risky unpinned package execution guidance for Mermaid CLI setup.

Mitigation: Install a pinned, reviewed Mermaid CLI version in a project with a lockfile before using the skill for sensitive work.

Risk: The security guidance flags one-shot npx, pnpm dlx, and bunx execution as unsuitable for sensitive work.

Mitigation: Avoid transient package execution in sensitive environments; use a preinstalled and reviewed mmdc binary instead.

Risk: The security guidance flags disabling the Chromium sandbox as a weakened browser security setting.

Mitigation: Do not disable the Chromium sandbox unless rendering only trusted diagrams inside a constrained environment.

## Reference(s):

- [Mermaid syntax reference](references/syntax.md)
- [Mermaid CLI repository](https://github.com/mermaid-js/mermaid-cli)
- [Mermaid documentation](https://mermaid.nodejs.cn/)
- [Mermaid configuration schema](https://mermaid.nodejs.cn/config/schema-docs/config.html)
- [ClawHub skill page](https://clawhub.ai/anyforge/skills/anymermaid-skill)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Mermaid source snippets, shell commands, and optional .mmd, SVG, PNG, or PDF file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports syntax lookup, optional dry-run validation, theme and rendering configuration, and headless-environment handling.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
