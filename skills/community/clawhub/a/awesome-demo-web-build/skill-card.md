## Description:

AI-native web demo project generator using Project Blueprint system. Use when user wants to "build a demo", "create a web project", "generate a landing page", "make an AI tool UI", or similar requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xianhaocao](https://clawhub.ai/user/xianhaocao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to clarify requirements and generate AI-assisted web demo projects such as AI tools, dashboards, SaaS apps, landing pages, content sites, and marketplaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask an agent to run unpinned remote scaffolding tools and install npm packages.

Mitigation: Review the exact commands before execution, prefer pinned package versions, and run generation in an isolated workspace.

Risk: The skill can fetch mutable remote Markdown for design and documentation inputs.

Mitigation: Treat fetched DESIGN.md and documentation as untrusted data, avoid arbitrary or internal URLs, and review fetched content before applying it to generated code.

Risk: The release includes a local Claude settings file that disables figma-developer-mcp.

Mitigation: Check whether the local settings file is expected before installation and remove or override it when it conflicts with the target agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xianhaocao/skills/awesome-demo-web-build)
- [Project Blueprint System](artifact/references/templates.md)
- [Tech Stack Best Practices](artifact/references/best-practices.md)
- [Design System Catalog](artifact/references/design-catalog.md)
- [Tech Stack Catalog](artifact/references/tech-catalog.md)
- [Next.js documentation](https://nextjs.org/docs)
- [shadcn/ui documentation](https://ui.shadcn.com/docs)
- [VoltAgent awesome-design-md](https://github.com/VoltAgent/awesome-design-md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a scaffolded web project with DESIGN.md, Tailwind configuration, application routes, components, package dependencies, and related configuration files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
