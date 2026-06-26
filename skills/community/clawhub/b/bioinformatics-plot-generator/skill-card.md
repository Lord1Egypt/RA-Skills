## Description: <br>
Route to the correct publication-quality plot sub-skill for volcano plots, heatmaps, box/violin plots, scatter plots, bar charts, MA plots, correlation matrices, and bubble charts from bioinformatics data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xutaoguo55](https://clawhub.ai/user/xutaoguo55) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bioinformatics researchers and analysts use this skill to choose and run script-based plotting tools for tabular genomics, proteomics, clinical, and related numeric datasets. It produces publication-quality static figures and optional statistics or processed tables from user-provided data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python plotting scripts against user-provided data and writes image or TSV outputs. <br>
Mitigation: Run it in a normal project directory, choose output paths deliberately, and review generated files before sharing or reusing them. <br>
Risk: Unpinned plotting and scientific Python dependencies can affect reproducibility or supply-chain control. <br>
Mitigation: Pin dependency versions in the execution environment when reproducibility, auditability, or regulated workflow controls are required. <br>
Risk: Generated statistical annotations and summaries depend on input column choices, thresholds, and assumptions in the selected plotting script. <br>
Mitigation: Confirm input columns, thresholds, and test settings against the analysis plan before using figures or tables in publications or decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xutaoguo55/bioinformatics-plot-generator) <br>
- [Router skill documentation](artifact/SKILL.md) <br>
- [Volcano plot sub-skill documentation](artifact/plot-volcano/SKILL.md) <br>
- [Heatmap sub-skill documentation](artifact/plot-heatmap/SKILL.md) <br>
- [Box, violin, and raincloud plot sub-skill documentation](artifact/plot-box-violin/SKILL.md) <br>
- [Scatter, bar, MA, correlation, and bubble plot sub-skill documentation](artifact/plot-scatter-bar/SKILL.md) <br>
- [Survival plot sub-skill documentation](artifact/plot-survival/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands that generate PNG, SVG, PDF, TSV, and console summary outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Python plotting scripts on user-provided CSV, TSV, or numeric matrix files and writes outputs to project paths selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
