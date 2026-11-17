## Description:

Automatically illustrate Markdown documents by turning image markers into screenshots or generated images, then writing an image-enriched Markdown output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and documentation teams use this skill to turn Markdown image markers into browser screenshots or generated illustrations and produce an image-enriched Markdown output with supporting assets and metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install unpinned browser automation and Python dependencies.

Mitigation: Prefer pinned, vetted versions of Playwright MCP, Playwright, and Python dependencies before running the workflow.

Risk: Browser automation may interact with authenticated websites and credentials.

Mitigation: Run browser automation in a constrained environment, expose only credentials needed for the specific site, and avoid sensitive pages unless required.

Risk: Screenshots, generated images, and final Markdown may contain sensitive or misleading content.

Mitigation: Review screenshots, generated assets, and generated Markdown before sharing or publishing them.

## Reference(s):

- [Browser Automation Guide](references/browser-automation.md)
- [Image Generation Guide](references/image-generation.md)
- [Playwright MCP Guide](references/playwright-mcp.md)
- [Site Explorer Guide](references/site-explorer.md)
- [Project homepage](https://github.com/Felo-Inc/felo-skills)
- [Support issues](https://github.com/Felo-Inc/felo-skills/issues)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated runs produce Markdown files, PNG image assets, and README metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses environment variables for website credentials and image-generation API keys; may create project-root output, raw, markdowns, and cache directories.]

## Skill Version(s):

1.0.0 (source: frontmatter, clawhub metadata, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
