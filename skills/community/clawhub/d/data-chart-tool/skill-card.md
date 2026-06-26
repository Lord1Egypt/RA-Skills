## Description: <br>
Data Chart Tool helps agents convert CSV, JSON, and Excel data into bar, line, pie, scatter, and area charts with configurable styling and PNG, JPEG, PDF, or SVG output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and report authors use this skill to turn CSV, JSON, or Excel datasets into chart files and previews for financial analysis, sales reporting, research figures, and personal data projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SKILL_LICENSE_SECRET is a tool-specific secret that could be exposed if reused, committed, or persisted broadly. <br>
Mitigation: Use a unique secret, keep it out of repositories and shared dotfiles, and set it only for commands that need paid features. <br>
Risk: The security summary notes a licensing bug affecting paid-feature handling. <br>
Mitigation: Do not rely on this skill as an access-control boundary; review the license path and update validation before commercial deployment. <br>
Risk: Installing dependencies directly can modify the user's active Python environment. <br>
Mitigation: Install and run the skill in a Python virtual environment where possible. <br>


## Reference(s): <br>
- [Data Chart Tool ClawHub Page](https://clawhub.ai/utopiabenben/data-chart-tool) <br>
- [Skill Usage Documentation](artifact/SKILL.md) <br>
- [Premium License Setup Guide](artifact/LICENSE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, plus generated chart files in PNG, JPEG, PDF, or SVG format.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scatter charts and unlimited batch export are described as paid features requiring a local license file and SKILL_LICENSE_SECRET.] <br>

## Skill Version(s): <br>
1.1.0-premium (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
