## Description: <br>
Turns a banker-memo analysis.md and data-provenance.md into a structured slide outline and rendered investment-banker-style PowerPoint deck with tables, charts, risk heatmaps, and scenario grids. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackdark425](https://clawhub.ai/user/jackdark425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill after a banker memo is complete to create a structured slides-outline.md and render a .pptx deck with banker-style visual primitives instead of prose-only slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The renderer can expand into local package installation and code execution during deck rendering. <br>
Mitigation: Review the renderer before use, run it only in a sandbox or disposable project directory, and prefer preinstalling pinned dependencies with npm scripts disabled. <br>
Risk: Generated slide outlines can carry incorrect or unsupported data into the rendered deck. <br>
Mitigation: Inspect slides-outline.md before rendering and keep the documented provenance validation gates in the workflow. <br>
Risk: Confidential analysis may be placed into the active agent or model workflow. <br>
Mitigation: Avoid using confidential analysis unless the operator is comfortable exposing that content to the active workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jackdark425/banker-slides-pptx) <br>
- [Banker Slides PPTX prompt template](references/banker_slides_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, structured slides-outline.md, shell commands, Python rendering scripts, and a rendered .pptx deck.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires existing analysis.md and data-provenance.md inputs; renderer expects structured slide blocks and numeric chart data.] <br>

## Skill Version(s): <br>
0.9.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
