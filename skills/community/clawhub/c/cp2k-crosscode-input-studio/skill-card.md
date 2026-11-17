## Description:

Generate, refine, explain, and cross-convert CP2K-centered input drafts for computational chemistry and materials workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lemon1044](https://clawhub.ai/user/lemon1044)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, computational chemists, and materials engineers use this skill to turn natural-language calculation requests and structure files into conservative CP2K input drafts, review reports, and cross-code draft inputs for Gaussian, VASP, ORCA, or Quantum ESPRESSO.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts write generated files to user-selected output paths.

Mitigation: Run the scripts in a dedicated working directory and use trusted output directories until path containment is reviewed.

Risk: Generated input fields may be carried into CP2K or cross-code draft files without strict validation.

Mitigation: Review normalized.json, job.inp, converted inputs, warnings, and review-required items before running any generated scientific job.

Risk: Draft basis, potential, k-point, spin, periodicity, and conversion choices can change scientific meaning.

Mitigation: Treat outputs as first-pass drafts and perform domain review plus convergence and library checks before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lemon1044/skills/cp2k-crosscode-input-studio)
- [README](README.md)
- [Design rules](references/design-rules.md)
- [Job spec schema](references/job-spec-schema.md)
- [CP2K task map](references/cp2k-task-map.md)
- [CP2K defaults](references/cp2k-defaults.md)
- [CP2K KIND defaults](references/cp2k-kinds.md)
- [Ambiguity policy](references/ambiguity-policy.md)
- [Conversion rules](references/conversion-rules.md)
- [Structure source routing](references/structure-sources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [JSON, Markdown, CP2K input text, and draft input files for Gaussian, VASP, ORCA, or Quantum ESPRESSO]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are first-pass drafts that surface assumptions, defaults, warnings, and review-required items rather than validated production settings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
