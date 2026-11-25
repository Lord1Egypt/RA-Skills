## Description:

Use when the user wants to create, edit, or inspect an architectural floor plan / building layout as code — e.g. "draw a 2-bedroom apartment", "add a bathroom to this plan", "make the bedroom 1 m wider", "lay out an office floor". ArchLang is a tiny text language that compiles a .arch file to a professional floor-plan drawing (SVG/PNG/PDF/DXF). Drive it entirely through the `archlang` CLI; do not hand-render.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chanmeng666](https://clawhub.ai/user/chanmeng666)

### License/Terms of Use:

MIT

## Use Case:

Developers and design professionals use ArchLang to create, edit, and inspect architectural floor plans as text, then compile and validate those plans with its CLI. It can also export the plan to drawing and data formats for further review or use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended package-fetch commands do not pin a version, so package contents may change between installs.

Mitigation: Pin a reviewed package version before fetching or running it.

Risk: The security scan had incomplete coverage because referenced local paths were unavailable for resolution.

Mitigation: Review the package and its referenced files before running it.

## Reference(s):

- [ArchLang Plan JSON schema](https://archlang.uk/plan.schema.json)
- [ArchLang intent schema](https://archlang.uk/intent.schema.json)
- [ArchLang grammar (GBNF)](https://archlang.uk/archlang.gbnf)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [ArchLang source, CLI commands, and generated SVG, PNG, PDF, DXF, TXT, or Plan JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plan files can be compiled and checked with the ArchLang CLI.]

## Skill Version(s):

1.68.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
