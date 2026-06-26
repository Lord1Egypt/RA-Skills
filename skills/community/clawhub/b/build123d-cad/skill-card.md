## Description: <br>
Parametric 3D CAD via build123d. Generate STEP, STL, SVG from Python scripts. Use when the user asks to design, model, create, or export 3D parts, enclosures, mounts, brackets, or mechanical components. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wngfra](https://clawhub.ai/user/wngfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, measure, validate, and export parametric mechanical parts and assemblies from build123d Python scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs locally generated Python CAD scripts with weak isolation. <br>
Mitigation: Review generated CAD scripts before execution and run the skill in a separate sandboxed workspace or container when sensitive files or credentials are present. <br>
Risk: Exported CAD files may be written outside the documented output folder. <br>
Mitigation: Review generated filenames and output paths before execution, and set or restrict the CAD workspace to an expected directory. <br>
Risk: Untrusted CAD scripts can create local execution and data exposure risk. <br>
Mitigation: Avoid running untrusted CAD scripts and install the skill only when local Python execution for CAD work is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wngfra/build123d-cad) <br>
- [build123d Documentation](https://build123d.readthedocs.io) <br>
- [build123d GitHub Repository](https://github.com/gumyr/build123d) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with Python scripts, shell commands, JSON command output, and exported STEP, STL, or SVG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated CAD scripts use millimeter dimensions and can report artifact paths, bounding boxes, measurements, cross-sections, and validation verdicts.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
