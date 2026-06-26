## Description: <br>
FlowStitch turns a short website or app brief into prompts, design systems, generated screens, React/TypeScript components, quality checks, and deployment guidance using Google Stitch MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windseeker1111](https://clawhub.ai/user/windseeker1111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use FlowStitch to turn product, brand, dashboard, mobile app, or competitor-analysis briefs into multi-page website or app builds. It guides prompt enhancement, design-system synthesis, Stitch screen generation, quality review, React/TypeScript export, and deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Competitor analysis and scraping workflows may access third-party sites without enough scoping or approval. <br>
Mitigation: Require explicit confirmation that the user is authorized to analyze the target site before any competitor scraping or browser-based collection. <br>
Risk: Automated deployment workflows can publish generated projects publicly through Vercel, Netlify, or GitHub Pages. <br>
Mitigation: Confirm the exact account, project, repository, deployment target, and public URL before publishing. <br>
Risk: Generated .stitch metadata and downloaded assets may contain project details that should not be committed or published without review. <br>
Mitigation: Review and sanitize .stitch metadata and generated assets before adding them to public repositories. <br>
Risk: Broad website-building workflows can create or modify many local project files. <br>
Mitigation: Review generated files and preview the site before deployment or handoff. <br>


## Reference(s): <br>
- [FlowStitch ClawHub Release](https://clawhub.ai/windseeker1111/flowstitch) <br>
- [Google Stitch Prompting Guide](https://stitch.withgoogle.com/docs/learn/prompting/) <br>
- [Design Mappings Reference](references/design-mappings.md) <br>
- [Prompt Keywords Reference](references/prompt-keywords.md) <br>
- [Stitch MCP Tool Schemas](references/tool-schemas.md) <br>
- [Quality Rubric](resources/quality-rubric.md) <br>
- [Architecture Checklist](resources/architecture-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, shell commands, and TypeScript/HTML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local .stitch metadata, site files, React/TypeScript components, downloaded Stitch assets, and deployment commands.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
