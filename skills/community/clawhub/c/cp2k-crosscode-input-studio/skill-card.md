## Description: <br>
Generate, refine, explain, and cross-convert CP2K-centered input drafts for computational chemistry and materials workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lemon1044](https://clawhub.ai/user/lemon1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, computational chemists, and materials engineers use this skill to turn natural-language calculation requests and structure files into conservative CP2K draft inputs, review reports, and draft translations for Gaussian, VASP, ORCA, or Quantum ESPRESSO. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled Python helpers read request and structure files and write generated draft outputs in the project directory. <br>
Mitigation: Run the helpers in a controlled working directory and review generated files before moving them into production workflows. <br>
Risk: Generated CP2K and cross-code inputs are draft scientific configurations, not convergence-validated production settings. <br>
Mitigation: Review charge, spin, periodicity, basis and pseudopotential choices, k-points, dispersion, and convergence settings before executing calculations. <br>
Risk: Cross-code translations cannot guarantee exact basis, pseudopotential, or library equivalence across CP2K, Gaussian, VASP, ORCA, and Quantum ESPRESSO. <br>
Mitigation: Treat translated inputs as starting points and replace placeholders or code-specific library choices with values validated for the target code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lemon1044/cp2k-crosscode-input-studio) <br>
- [Design rules](references/design-rules.md) <br>
- [Job spec schema](references/job-spec-schema.md) <br>
- [CP2K task map](references/cp2k-task-map.md) <br>
- [CP2K defaults](references/cp2k-defaults.md) <br>
- [CP2K kinds](references/cp2k-kinds.md) <br>
- [Ambiguity policy](references/ambiguity-policy.md) <br>
- [Structure sources](references/structure-sources.md) <br>
- [Conversion rules](references/conversion-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON, CP2K input text, report files, and draft input files for supported target codes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are first-pass drafts with explicit assumptions, warnings, and review-required items.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
