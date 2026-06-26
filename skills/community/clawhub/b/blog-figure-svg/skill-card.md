## Description: <br>
Generates accessible, lightweight SVG figures and OG feature cards for blog and CMS workflows, with rasterized PNG outputs and writer-ready caption guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[automatelab](https://clawhub.ai/user/automatelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content marketers, indie hackers, and dev-tool blog writers use this skill to create accessible diagrams, comparison charts, taxonomy visuals, terminal mocks, and feature images after article prose is stable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated visuals may include incorrect, misleading, or uncited data if the source article is wrong or incomplete. <br>
Mitigation: Review each SVG/PNG and caption against the article before publishing, and do not plot data the article does not already cite. <br>
Risk: Optional rasterizer or PNG compression tools may be installed outside the skill package. <br>
Mitigation: Install ImageMagick, rsvg-convert, Inkscape, CairoSVG, pngquant, or oxipng only from trusted package sources and keep them updated. <br>
Risk: CMS upload credentials may be exposed if users connect generated assets to upload tooling carelessly. <br>
Mitigation: Use trusted CMS upload tooling and keep credentials in the CMS adapter rather than in generated figures, captions, or command history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/automatelab/blog-figure-svg) <br>
- [Skill homepage](https://github.com/AutomateLab-tech/publishing-skills) <br>
- [Publisher profile](https://clawhub.ai/user/automatelab) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, markdown, guidance] <br>
**Output Format:** [Markdown guidance with inline SVG, shell commands, and figure handoff snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces editable SVG source, rasterized PNG assets, and caption requirements for publishing workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
