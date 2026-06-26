## Description: <br>
Local-first chart generation engine for trends, comparisons, distributions, and quick visual explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panchenbo](https://clawhub.ai/user/panchenbo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other ClawHub users use this skill to choose simple chart types and generate local chart images from inline data for comparisons, trends, distributions, and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read or visualize sensitive local data if pointed at files the user did not intend to share with the agent. <br>
Mitigation: Use it only with data files the user explicitly intends the agent to read. <br>
Risk: Chart generation writes PNG outputs and updates local chart history. <br>
Mitigation: Ask before writing or overwriting chart outputs in the workspace, and review generated files before relying on them. <br>


## Reference(s): <br>
- [Chart Philosophy](references/philosophy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with shell commands; generated PNG chart files and local JSON history when scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python scripts and matplotlib; stores chart history and outputs under ~/.openclaw/workspace/memory/chart/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
