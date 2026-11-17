## Description:

Gb Arch Cad Gen helps agents generate conceptual CAD floor-plan drawings aligned with cited Chinese architectural drafting standards, exporting SVG and PDF files without AutoCAD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wongeven](https://clawhub.ai/user/wongeven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and design automation users can use this skill to generate parameterized residential plan drawings, title blocks, dimensions, and local SVG/PDF outputs for early-stage design review. The outputs should be treated as conceptual drafts and reviewed by qualified professionals before any construction or compliance use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CAD drawings may be incomplete, approximate, or unsuitable for construction, permitting, structural, MEP, fire-safety, or accessibility decisions.

Mitigation: Use the drawings only as conceptual drafts and require review by qualified architects, engineers, and code specialists before relying on them.

Risk: Running the skill can install npm packages and write SVG/PDF outputs to the local filesystem.

Mitigation: Review dependency versions, run in a controlled workspace, and inspect generated files before moving them into sensitive project environments.

Risk: The skill cites Chinese architectural standards, but automated checks may not prove full legal or project-specific compliance.

Mitigation: Treat built-in standard checks as preliminary screening and verify all applicable regulatory requirements against authoritative project documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wongeven/skills/gb-arch-cad-gen)
- [Skill definition](artifact/SKILL.md)
- [Package manifest](artifact/package.json/document.md)
- [Drawing engine source](artifact/scripts/main.js/document.md)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [SVG and PDF drawing files with optional JSON design data and Markdown or shell guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated drawings locally under ./output; generated drawings are conceptual drafts and require professional review.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json/document.md, _skillhub_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
