## Description: <br>
Extracts structured information from engineering drawings, including BOM rows, dimensions, tolerances, title-block metadata, and symbol inventories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to parse mechanical, P&ID, electrical, and civil drawing inputs into structured extraction results for review, downstream data processing, and annotated previews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential engineering drawings may contain sensitive design or IP information. <br>
Mitigation: Process only drawings the user explicitly provides, keep files in trusted workspaces, and choose output paths deliberately. <br>
Risk: Extracted BOM, title-block, and dimension data may be incomplete or incorrect. <br>
Mitigation: Review generated structured data and any low-confidence extraction items before using or sharing results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/boboy-j/engineering-drawing-parser) <br>
- [Project Homepage](https://github.com/openclaw-skills/engineering-drawing-parser) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON extraction examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce local JSON extraction results and Markdown previews; review extracted values before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
