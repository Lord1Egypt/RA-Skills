## Description: <br>
CAD Editor turns natural language drafting requests into CAD engineering drawings across architectural, mechanical, electrical, piping, structural, and basic geometry domains, producing DXF files and PNG/SVG/PDF previews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and CAD users use this skill to convert natural language drafting requests into standards-oriented engineering drawings and preview/export files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run generated Python code derived from user drafting requests. <br>
Mitigation: Review generated scripts before execution, run them only in a virtual environment or disposable workspace, and keep outputs in a dedicated folder. <br>
Risk: Untrusted filenames, output paths, or direct generator parameters could affect where files are written or how generated code behaves. <br>
Mitigation: Avoid passing untrusted paths or raw generator parameters; constrain output paths to a known project directory. <br>


## Reference(s): <br>
- [CAD Editor release page](https://clawhub.ai/wangjiaocheng/cad-editor) <br>
- [ACI color index and drafting color guidance](artifact/references/color_index.md) <br>
- [DXF entity group code reference](artifact/references/dxf_entity_codes.md) <br>
- [Natural language intent templates](artifact/references/intent_templates.json) <br>
- [GB/T layer naming standards](artifact/references/layer_standards.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown instructions with Python code examples and generated CAD output files such as DXF, PNG, SVG, and PDF] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated drawing scripts and file paths should be reviewed before execution or delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
