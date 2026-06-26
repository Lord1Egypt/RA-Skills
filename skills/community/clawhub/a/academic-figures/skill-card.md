## Description: <br>
Academic Figures generates publication-quality charts from JSON or CSV data, including 14 chart types, colorblind-safe themes, CJK support, hatching, multi-panel layouts, flow diagrams, and PNG, SVG, PDF, TIFF, or EPS output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[docsor1212](https://clawhub.ai/user/docsor1212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to turn structured JSON or CSV datasets into journal-ready academic figures, diagrams, and statistical visualizations. It is suited for local figure generation workflows where the user controls the input data and output path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plotting workflow reads the user-selected input file and can write or overwrite the requested output file. <br>
Mitigation: Use intentional input data and explicit output paths, and review the generated figure before sharing or submitting it. <br>
Risk: Generic chart-generation requests may activate the skill in contexts where another visualization workflow would be more appropriate. <br>
Mitigation: Confirm the desired output is a publication-style academic figure before running the local generator. <br>


## Reference(s): <br>
- [Academic Figures Skill Page](https://clawhub.ai/docsor1212/academic-figures) <br>
- [Data Format Reference](references/data-formats.md) <br>
- [Academic Figures Pitfalls](references/pitfalls.md) <br>
- [Reverse-Engineering Chart Colors from Reference Images](references/reverse-engineering-colors.md) <br>
- [academic-figures v1.5.0 Upgrade Analysis](references/v1.5-upgrade-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated figure files may be PNG, SVG, PDF, TIFF, or EPS.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local execution with user-selected input and output paths; generated figures use a white background for publication workflows.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release metadata; artifact frontmatter lists 1.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
