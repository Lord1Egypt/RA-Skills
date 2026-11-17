## Description:

Generates deep technical CookBooks, Handbooks, and Surveys from user materials, producing MDX chapters first and optionally converting them into ElegantBook LaTeX/PDF, Nextra website, and optimized EPUB outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samonysh](https://clawhub.ai/user/samonysh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and documentation teams use this skill to turn multi-source technical material into structured long-form books, handbooks, surveys, and cookbook-style documentation. It supports MDX as the primary intermediate output with optional PDF, website, and EPUB build paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote diagram rendering can expose diagram source content to a third-party service.

Mitigation: Use trusted source material, avoid confidential diagrams with remote rendering, and prefer local Docker or offline PlantUML rendering for sensitive projects.

Risk: Generated project content can influence file writes, generated code, shell commands, and build outputs.

Mitigation: Run build scripts in a sandboxed workspace and review generated paths, chapter slugs, scaffold arguments, and conversion plans before executing npm, Docker, Python, or LaTeX commands.

Risk: LLM-assisted conversion steps can produce incorrect LaTeX, XHTML, citations, or technical explanations.

Mitigation: Review converted chapters and generated book artifacts before publication, especially code samples, references, formulas, diagrams, and security-sensitive guidance.

## Reference(s):

- [O'Reilly Cookbook Style Guide](references/style-guide-oreilly.md)
- [Springer Handbook Style Guide](references/style-guide-springer.md)
- [ElegantBook](https://github.com/ElegantLaTeX/ElegantBook)
- [Kroki Diagram Rendering](https://kroki.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [MDX/Markdown with generated project files and optional LaTeX, XHTML, EPUB, and Nextra site assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured book directory with MDX as the default output and optional format-specific subdirectories for PDF, website, EPUB, figures, diagrams, and metadata.]

## Skill Version(s):

1.2.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
