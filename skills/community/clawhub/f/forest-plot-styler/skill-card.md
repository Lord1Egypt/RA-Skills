## Description: <br>
Beautify meta-analysis forest plots with customizable odds ratio points and confidence intervals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to generate styled forest plots for meta-analysis or subgroup analysis from CSV or Excel data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Python dependencies are not pinned or constrained, which can make installs less reproducible and may miss dependency vulnerability controls. <br>
Mitigation: Install in an isolated environment and pin or constrain dependencies through normal vulnerability scanning, especially NumPy. <br>
Risk: The script reads local CSV or Excel inputs and writes plot output files to the selected path. <br>
Mitigation: Run it in a controlled workspace, review input and output paths, and avoid using sensitive datasets unless the environment is approved for them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands] <br>
**Output Format:** [PNG, PDF, or SVG plot files with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads CSV or Excel study data and writes the requested forest plot file.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
