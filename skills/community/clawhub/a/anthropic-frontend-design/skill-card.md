## Description: <br>
Create distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Qrucio](https://clawhub.ai/user/Qrucio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and designers use this skill to create frontend components, pages, applications, and interface guidance with stronger typography, color, interaction, accessibility, and stack-specific design choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The --persist and --output-dir options can write generated design-system Markdown files outside the intended project area if pointed at a broad or sensitive directory. <br>
Mitigation: Use --persist only inside a project workspace or dedicated output folder, and review the chosen output path before execution. <br>
Risk: Bundled style and UX reference data can influence design decisions but is not policy-quality accessibility or inclusion guidance. <br>
Mitigation: Treat generated recommendations as design inspiration and verify accessibility, inclusion, and product requirements through project review before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Qrucio/anthropic-frontend-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and plain text guidance; optional Markdown files when persistence is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bundled local CSV design references. With --persist, it can write design-system Markdown files under the current directory or a requested output directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
