## Description: <br>
EasyEDA Agent helps agents operate EasyEDA Pro through local typed CLI actions for schematic, PCB, part-selection, linting, DRC, exports, and checkpointed design workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoushoujianwork](https://clawhub.ai/user/zhoushoujianwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, electrical engineers, and agent operators use this skill to inspect, create, edit, lint, and export EasyEDA Pro schematic and PCB projects through the local easyeda-agent CLI/daemon workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify live EasyEDA schematic and PCB data, including placement, wiring, imports, saves, and bulk layout operations. <br>
Mitigation: Run health and readback checks before mutation, require confirmation before destructive or bulk operations, and keep explicit saved checkpoints or project backups. <br>
Risk: Design correctness can be misread from stale screenshots after API edits. <br>
Mitigation: Judge state from EasyEDA list, check, DRC, and layout-lint data before claiming completion; use screenshots only as a visual review aid. <br>
Risk: Part-selection helpers may access JLCPCB network data and write local baseline or artifact files. <br>
Mitigation: Install only where this access is expected, review generated files under EasyEDA-related directories, and confirm selected parts before ordering or fabrication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhoushoujianwork/skills/easyeda-agent) <br>
- [EasyEDA Action Reference](references/actions.md) <br>
- [EasyEDA Design Flow](references/design-flow.md) <br>
- [EasyEDA Schematic](references/schematic.md) <br>
- [EasyEDA PCB](references/pcb.md) <br>
- [Auto-layout SOP](references/auto-layout-sop.md) <br>
- [Part Selection](references/part-selection.md) <br>
- [Schematic Layout Conventions](references/schematic-layout-conventions.md) <br>
- [PCB Layout Conventions](references/pcb-layout-conventions.md) <br>
- [Standard Parts Data](references/standard-parts.json) <br>
- [Orientation Data](references/orientation.json) <br>
- [Sheet Templates](references/sheet-templates.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, code snippets, status summaries, and generated artifact paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update EasyEDA project artifacts, BOM/netlist exports, lint baselines, screenshots, and local helper-script outputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
