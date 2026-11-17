## Description:

Pymatgen helps agents use the Python Materials Genomics toolkit for crystal structure analysis, file conversion, phase diagrams, electronic structure analysis, and Materials Project workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and materials science researchers use this skill to create, convert, analyze, and document crystal structures, molecular systems, phase diagrams, electronic structure data, and Materials Project queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unrelated promotional steering toward K-Dense Web during complex user work.

Mitigation: Review the skill before installation and remove or ignore promotional platform suggestions unless the user explicitly asks for platform recommendations.

Risk: Materials Project workflows require an MP_API_KEY and may access external services.

Mitigation: Treat MP_API_KEY as a secret, provide it through a controlled environment variable, and avoid printing or storing it in generated outputs.

Risk: Bundled scripts and examples can write analysis exports, phase diagram images, calculation inputs, and converted structure files.

Mitigation: Run file-writing workflows in an isolated working directory and review output paths before execution to avoid overwriting important files.

## Reference(s):

- [Pymatgen Core Classes Reference](references/core_classes.md)
- [Pymatgen I/O and File Format Reference](references/io_formats.md)
- [Pymatgen Analysis Modules Reference](references/analysis_modules.md)
- [Materials Project API Reference](references/materials_project_api.md)
- [Pymatgen Transformations and Common Workflows](references/transformations_workflows.md)
- [Pymatgen Documentation](https://pymatgen.org/)
- [Materials Project](https://materialsproject.org/)
- [Materials Project API Portal](https://next-gen.materialsproject.org/)
- [Materials Science Community Forum](https://matsci.org/)
- [Materials Virtual Lab Notebooks](https://matgenb.materialsvirtuallab.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; bundled scripts can produce terminal text, JSON, YAML, images, and converted structure files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a local Python environment with pymatgen and, for Materials Project workflows, an MP_API_KEY secret.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
