## Description:

Create RFQ-ready 2D DXF and optional SVG preview files from a strict, validated JSON spec derived from a natural-language design prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajmwagar](https://clawhub.ai/user/ajmwagar)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to convert simple sheet or plate part requirements into validated manufacturing-oriented JSON specs, then render DXF and SVG files for quoting or review. It is suited for mounting plates, gussets, brackets, hole patterns, slots, closed polyline profiles, and simple etched drawings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted design specs can manipulate generated DXF structure through unvalidated layer names.

Mitigation: Use trusted specs, keep default or simple layer names, and review generated DXF/SVG files before RFQ or manufacturing use.

Risk: Generated files may overwrite existing outputs with the same spec basename in the selected output directory.

Mitigation: Write to a dedicated output directory for each job and preserve reviewed outputs separately.

Risk: The artifact documents known geometry limits such as no kerf compensation, no bend-line or flat-pattern support, and no full geometric self-intersection checks.

Mitigation: Treat outputs as quoting and review artifacts, and verify manufacturability in CAD/CAM before fabrication.

## Reference(s):

- [Spec schema](artifact/references/spec_schema.md)
- [Test prompts](artifact/references/test_prompts.md)
- [ClawHub skill page](https://clawhub.ai/ajmwagar/skills/create-dxf)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [JSON spec plus generated DXF and SVG files with command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local files named from the input spec basename in the selected output directory.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
