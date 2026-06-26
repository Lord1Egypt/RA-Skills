## Description: <br>
Design dashboard layout sketches for clinical trials showing enrollment progress and adverse event rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trial operations teams use this skill to generate HTML dashboard sketches for clinical trial monitoring, including recruitment progress, adverse event summaries, subject distribution, data quality, and milestones. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes an HTML report to a path supplied by --output, which can replace an existing file if the same path is reused. <br>
Mitigation: Use a dedicated output folder and avoid pointing --output at existing project files unless replacement is intended. <br>
Risk: The generated dashboard is a layout sketch based on provided parameters and generated sample values, not a validated clinical analysis. <br>
Mitigation: Review generated content before sharing it or using it in trial operations, especially metrics related to enrollment, adverse events, and data quality. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/dashboard-design-for-trials) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands] <br>
**Output Format:** [HTML file with embedded CSS and JavaScript plus console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to the user-specified --output path; default output is dashboard.html.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
