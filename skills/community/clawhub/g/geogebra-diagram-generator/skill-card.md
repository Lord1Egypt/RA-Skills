## Description: <br>
Generate precise static or interactive geometry diagrams for geometry problems using GeoGebra's Execute text script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gallexy-liu](https://clawhub.ai/user/gallexy-liu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn geometry problems into copy-pasteable GeoGebra Execute scripts that preserve constraints such as perpendiculars, rotations, tangencies, ratios, and dynamic points. It also guides browser-based verification in GeoGebra when automation is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Geometry prompts may contain private or sensitive information that is pasted into geogebra.org during browser verification. <br>
Mitigation: Review generated GeoGebra commands and source problem text before pasting them into GeoGebra, especially for private or sensitive geometry content. <br>
Risk: Generated geometry commands can fail or render misleading diagrams if syntax, localization, or hidden browser dialogs interfere with execution. <br>
Mitigation: Verify expected objects, measurements, or canvas output in GeoGebra before relying on the diagram. <br>


## Reference(s): <br>
- [GeoGebra Diagram Generator homepage](https://github.com/gallexy-liu/geogebra-diagram-generator) <br>
- [GeoGebra Geometry](https://www.geogebra.org/geometry) <br>
- [GeoGebra Classic](https://www.geogebra.org/classic) <br>
- [GeoGebra Execute Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with a fenced geogebra Execute command and concise explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser verification guidance and screenshot instructions when browser automation is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
