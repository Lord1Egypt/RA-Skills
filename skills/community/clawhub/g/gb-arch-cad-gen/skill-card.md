## Description: <br>
Generates programmatic CAD floor-plan drawings aligned with cited Chinese architectural drawing and residential design standards, with SVG and PDF output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wongeven](https://clawhub.ai/user/wongeven) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Architectural designers, developers, and agents can use this skill to generate draft residential floor-plan drawings, title blocks, dimensions, layers, and structured drawing outputs for review. Outputs should be treated as scheme-level reference material, not construction-ready documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated drawings may appear code-compliant even when building-code compliance has not been independently verified. <br>
Mitigation: Treat outputs as draft/reference material and require review by a qualified professional before permitting, construction, or safety decisions. <br>
Risk: The artifact can continue generating drawings after validation warnings are detected. <br>
Mitigation: Make mandatory-rule validation blocking in downstream workflows and resolve reported violations before relying on generated files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wongeven/gb-arch-cad-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance plus generated SVG, PDF, and JSON-like drawing data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and makerjs; writes drawing files to an output directory when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package metadata, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
