## Description: <br>
Turns presales requirements, meeting notes, and solution materials into editable business capability blueprints, domain-knowledge maps, and architecture diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaisersong](https://clawhub.ai/user/kaisersong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, solution architects, and presales teams use this skill to convert requirements, meeting notes, or solution documents into structured blueprint JSON and diagram exports for review or downstream report and slide workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Capability metadata requests purchase authority, crypto access, OAuth tokens, and sensitive credentials without a matching offline-rendering need. <br>
Mitigation: Review and restrict capability grants before installation; do not enable purchase, crypto, OAuth, or credential permissions unless a separate deployment review justifies them. <br>
Risk: Generated audit files may preserve command-line arguments, paths, or source-material details. <br>
Mitigation: Avoid putting secrets, access tokens, or sensitive customer identifiers in command-line arguments or file paths, and review generated artifacts before sharing. <br>
Risk: Generated blueprints and diagrams can encode incorrect or misleading business or architecture guidance. <br>
Mitigation: Validate outputs with domain owners and run the skill's validation/export checks before using artifacts in customer-facing materials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaisersong/business-blueprint-skill) <br>
- [README](README.md) <br>
- [Skill contract](SKILL.md) <br>
- [Blueprint schema](references/blueprint-schema.md) <br>
- [Entity schema](references/entities-schema.md) <br>
- [Systems schema](references/systems-schema.md) <br>
- [Domain-knowledge extraction](references/domain-knowledge-extraction.md) <br>
- [Knowledge entities schema](references/knowledge-entities-schema.md) <br>
- [Route eligibility](references/route-eligibility.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance plus generated JSON, SVG, HTML, draw.io, Excalidraw, Mermaid, and projection artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts are written to workspace output paths and may include audit, patch, and viewer manifest files.] <br>

## Skill Version(s): <br>
0.16.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
