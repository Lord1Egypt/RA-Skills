## Description:

FlowStitch guides an agent through Google Stitch workflows to turn a brief website or app idea into generated designs, React/TypeScript components, quality checks, and deployment commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windseeker1111](https://clawhub.ai/user/windseeker1111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and product teams use FlowStitch to prototype and ship websites, dashboards, and mobile app screens with Stitch-backed design generation, brand import, competitive analysis, React export, and deployment guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to install tools, write files, push code, and publish production deployments.

Mitigation: Use it in a sandboxed project and require explicit approval before package installation, git push, or production deployment.

Risk: Deployment steps can publish to the wrong account, project, or visibility setting.

Mitigation: Confirm the deployment provider account, target project, and public/private visibility before running deployment commands.

Risk: Competitive analysis workflows may scrape competitor sites.

Mitigation: Only analyze sites when authorized and after checking applicable site terms and policies.

Risk: Stitch download URLs may expose sensitive generated assets or expire unexpectedly.

Mitigation: Treat download URLs as sensitive and restrict downloads to expected Stitch or Google Cloud Storage assets under the intended project directory.

## Reference(s):

- [FlowStitch Skill Page](https://clawhub.ai/windseeker1111/skills/flowstitch)
- [Google Stitch Prompting Guide](https://stitch.withgoogle.com/docs/learn/prompting/)
- [Design Mappings & Descriptors](references/design-mappings.md)
- [UI/UX Keywords Reference](references/prompt-keywords.md)
- [Stitch MCP Tool Schemas](references/tool-schemas.md)
- [FlowStitch Quality Rubric](resources/quality-rubric.md)
- [React Component Architecture Quality Gate](resources/architecture-checklist.md)
- [Baton File Schema](resources/baton-schema.md)
- [Remotion Composition Quality Gate](resources/composition-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, shell, HTML, and TypeScript examples plus project files created during workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write site, design, component, quality-log, and deployment-support files in the active project workspace.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
