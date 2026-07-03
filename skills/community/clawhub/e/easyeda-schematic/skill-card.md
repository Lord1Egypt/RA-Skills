## Description: <br>
EasyEDA Schematic helps agents inspect, edit, verify, and export artifacts from EasyEDA schematic pages through the easyeda-agent CLI or daemon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoushoujianwork](https://clawhub.ai/user/zhoushoujianwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and electronics engineers use this skill to automate EasyEDA schematic inspection, component placement, wiring, DRC and layout checks, and BOM or netlist export while keeping destructive edits behind confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on active EasyEDA projects and modify designs. <br>
Mitigation: Keep confirmation prompts for destructive actions and saves, use dry runs where available, and verify changes with readback, DRC, layout lint, or snapshots before proceeding. <br>
Risk: Generated snapshots, BOMs, netlists, and lint baselines may contain sensitive design data. <br>
Mitigation: Treat generated artifacts as project-sensitive data and store or share them only according to the user's design-data handling policy. <br>
Risk: Raw debug JavaScript paths can bypass typed EasyEDA actions. <br>
Mitigation: Avoid debug.exec_js unless necessary and require explicit user acceptance before using it. <br>


## Reference(s): <br>
- [EasyEDA Action Reference](references/actions.md) <br>
- [easyeda-agent homepage](https://github.com/zhoushoujianwork/easyeda-agent) <br>
- [ClawHub skill page](https://clawhub.ai/zhoushoujianwork/skills/easyeda-schematic) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to generate local EasyEDA snapshots, BOMs, netlists, lint reports, and JSON command outputs.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
