## Description: <br>
Drivethru Graphic Artist creates deterministic product mockups by compositing a user-supplied logo or graphic onto a blank product photo, with background removal, product-bound detection, and iterative placement tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmtucker](https://clawhub.ai/user/zmtucker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, designers, sellers, and developers use this skill to preview supplied artwork on blank apparel or products, remove simple image backgrounds, and iteratively adjust size, position, and rotation before choosing a mockup direction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local image files and writes PNG outputs and placement defaults. <br>
Mitigation: Use intended input paths, set MOCKUP_DATA_DIR to a dedicated folder, and review generated mockups before sharing them. <br>
Risk: Background removal may download a rembg segmentation model on first use. <br>
Mitigation: Preinstall and cache approved dependencies in controlled environments, or avoid background-removal flows when outbound network access is not allowed. <br>
Risk: Custom placement rules can change future mockup defaults. <br>
Mitigation: Use the schema-validated edit script and review rule changes before promoting tuned values as saved defaults. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zmtucker/drivethru-graphic-artist) <br>
- [Iterative feedback guide](references/iterative_feedback.md) <br>
- [Placement rules schema](references/placement_rules_schema.json) <br>
- [rembg project](https://github.com/danielgatis/rembg) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance, Configuration] <br>
**Output Format:** [PNG image files with JSON receipts and concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided image paths, writes output PNGs, and may update a local placement-rules catalog in MOCKUP_DATA_DIR.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
