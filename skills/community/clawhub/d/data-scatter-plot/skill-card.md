## Description: <br>
Reads CSV or Excel data files and generates scatter plots from Result row values with optional Min and Max Limit reference lines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewhb](https://clawhub.ai/user/matthewhb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and data analysts use this skill to turn structured CSV or Excel measurement data into scatter plot image files, including optional limit reference lines for quick visual inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency versions are specified with minimum bounds, so installations may drift over time. <br>
Mitigation: Install dependencies from a trusted Python package source and pin versions or use a lock file when reproducible output matters. <br>
Risk: Generated plot files may overwrite same-named files in the selected output directory. <br>
Mitigation: Run the skill only with data files and output folders you intend it to access, and review the output directory before batch generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/matthewhb/data-scatter-plot) <br>
- [Publisher profile](https://clawhub.ai/user/matthewhb) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Configuration instructions] <br>
**Output Format:** [PNG plot files and command-line or Python usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local .csv, .xls, and .xlsx files and writes generated plot files to a selected output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
