## Description: <br>
Convert design images to pixel-perfect HTML/CSS by analyzing layout, colors, and fonts, then iteratively refining code through visual comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nodermachine](https://clawhub.ai/user/nodermachine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn static design mockups or screenshots into HTML/CSS and refine the result against rendered image comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bundled Python helper can install an unpinned Pillow package at runtime. <br>
Mitigation: Prefer the documented Node workflow, install dependencies explicitly, and avoid scripts/pipeline.py unless automatic package installation is acceptable. <br>
Risk: Design images and rendered HTML may contain proprietary or untrusted content. <br>
Mitigation: Run the workflow in a sandboxed environment when processing sensitive design assets or untrusted HTML. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Button Example](references/examples/button-example.md) <br>
- [Card Example](references/examples/card-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated HTML/CSS files, JSON reports, and PNG comparison images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce final.html, comparison_report.md, analysis.json, rendered screenshots, diff images, and iteration timelines.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
