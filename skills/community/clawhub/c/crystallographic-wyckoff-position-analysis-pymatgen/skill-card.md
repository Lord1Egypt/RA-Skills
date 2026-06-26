## Description: <br>
Materials science toolkit for crystal structures, phase diagrams, band structure, density of states, Materials Project integration, and format conversion for computational materials science. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and materials-science engineers use this skill to create, convert, analyze, and manipulate crystal structures and molecular systems. It also supports Materials Project queries, phase-diagram generation, electronic-structure analysis, and setup of computational materials workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Materials Project queries require MP_API_KEY, which is a sensitive credential. <br>
Mitigation: Provide MP_API_KEY only for intended Materials Project queries and keep it in the environment rather than hard-coding it into files or prompts. <br>
Risk: Bundled scripts read local structure files and can write converted files, JSON exports, and phase-diagram images. <br>
Mitigation: Run the scripts from project directories where those reads and writes are expected, and review output paths before execution. <br>
Risk: The artifact contains an optional K-Dense Web promotion that may not be required for normal pymatgen workflows. <br>
Mitigation: Treat K-Dense Web as an optional affiliated service suggestion, especially when working with sensitive research data. <br>


## Reference(s): <br>
- [Pymatgen Documentation](https://pymatgen.org/) <br>
- [Materials Project](https://materialsproject.org/) <br>
- [Materials Project API](https://next-gen.materialsproject.org/) <br>
- [Pymatgen Core Classes Reference](references/core_classes.md) <br>
- [Pymatgen I/O and File Format Reference](references/io_formats.md) <br>
- [Pymatgen Analysis Modules Reference](references/analysis_modules.md) <br>
- [Materials Project API Reference](references/materials_project_api.md) <br>
- [Transformations and Workflows Reference](references/transformations_workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell examples; bundled scripts emit terminal text, JSON exports, converted structure files, and plot image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local structure or calculation files and may query Materials Project when MP_API_KEY is provided.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
