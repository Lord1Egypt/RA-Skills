## Description: <br>
Generate standardized figure legends for scientific charts and graphs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, academic writers, and developers use this skill to generate publication-style text legends for scientific figures such as bar charts, line graphs, scatter plots, box plots, heatmaps, microscopy images, flow cytometry plots, and western blots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Figure paths and output paths are read from user-provided command-line arguments. <br>
Mitigation: Provide only figure paths and output locations intended for local processing. <br>
Risk: The artifact documentation describes network/API behavior, while the reviewed security evidence says the code appears local-only. <br>
Mitigation: Avoid confidential unpublished figures until the publisher clarifies the documentation ambiguity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/figure-legend-gen) <br>
- [Figure Legend Templates](references/legend_templates.md) <br>
- [Academic Figure Legend Style Guide](references/academic_style_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Text, Markdown, or LaTeX figure legend text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the generated legend to stdout or to a user-provided output file; supports English and Chinese output options.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
