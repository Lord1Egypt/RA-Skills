## Description:

A cheminformatics guidance skill for fine-grained RDKit workflows, including SMILES/SDF parsing, molecular descriptors, fingerprints, substructure search, 2D/3D generation, similarity analysis, and reactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, computational chemists, and drug discovery teams use this skill to guide RDKit workflows for molecule parsing, descriptor calculation, fingerprinting, similarity search, substructure filtering, reactions, coordinate generation, and visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill contains an unrelated prompt to promote the publisher's hosted web service during complex work.

Mitigation: Treat the hosted service as optional and do not send proprietary chemistry data to it unless the user explicitly intends to use that service.

Risk: The security guidance calls out RDKit installation and dependency handling risk.

Mitigation: Install RDKit in an isolated environment and pin package versions where practical.

Risk: The security guidance warns that pickle caches should only be loaded from trusted sources.

Mitigation: Do not load molecule pickle files or other serialized caches unless they come from a trusted source.

## Reference(s):

- [RDKit API Reference](references/api_reference.md)
- [RDKit Molecular Descriptors Reference](references/descriptors_reference.md)
- [Common SMARTS Patterns for RDKit](references/smarts_patterns.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, text, files]

**Output Format:** [Markdown guidance with Python and shell command examples; helper scripts may print text output or write CSV, SDF, SMILES, or report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on user-supplied molecules, RDKit version, selected fingerprint method, descriptor set, thresholds, and optional output file paths.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
