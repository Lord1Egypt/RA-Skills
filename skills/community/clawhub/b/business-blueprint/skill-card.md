## Description: <br>
Turns presales requirements, meeting notes, and solution materials into editable business capability blueprints, swimlane flows, application architecture diagrams, and related exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaisersong](https://clawhub.ai/user/kaisersong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, solution architects, and presales teams use this skill to convert raw requirements or meeting notes into structured blueprint JSON, validate the result, and generate viewer or diagram exports for downstream reports and presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workspace artifacts, patch logs, or generation prompts may retain sensitive business requirements or meeting notes. <br>
Mitigation: Use dedicated workspace folders, avoid passing secrets or full confidential notes in CLI arguments, and review generated files before sharing or committing them. <br>
Risk: Server evidence reports sensitive capability tags that are not explained by the release materials. <br>
Mitigation: Install only in environments where those tags do not grant additional authority, and review the skill before enabling it in a broader agent runtime. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaisersong/business-blueprint) <br>
- [Business Blueprint README](README.md) <br>
- [Entity schema reference](references/entities-schema.md) <br>
- [Systems schema reference](references/systems-schema.md) <br>
- [Architecture design system](references/architecture-design-system.md) <br>
- [Export evaluation strategy](evals/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Blueprint JSON, projection JSON, static HTML viewers, SVG, draw.io, Excalidraw, Mermaid Markdown, and validation diagnostics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are written to workspace project folders and may include patch logs or generation prompts that should be reviewed before sharing.] <br>

## Skill Version(s): <br>
0.13.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
