## Description: <br>
Generate CSS clip-path code for shapes. Use when the user asks to create a clip path, clip an element to a shape, generate clip-path CSS, or make a polygon, circle, ellipse, or inset clip. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to generate CSS clip-path snippets for common, preset, or custom shapes and include short usage examples for applying them to elements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated clip-path values may not match the intended visual shape when the request is ambiguous or parameters are outside the expected range. <br>
Mitigation: Review the generated CSS visually and use the skill's parameter handling guidance, including clamping out-of-range percentages and asking for at least three polygon coordinate pairs. <br>
Risk: Browser compatibility may vary when Safari requires a vendor-prefixed clip-path declaration. <br>
Mitigation: Request the optional -webkit-clip-path prefix when Safari compatibility matters and test the output in target browsers. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with CSS code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include standard and optional -webkit-prefixed clip-path declarations plus a short CSS usage example.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
