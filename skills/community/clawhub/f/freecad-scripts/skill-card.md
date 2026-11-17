## Description:

Expert skill for writing FreeCAD Python scripts, macros, and automation for FreeCAD models, parametric objects, Part/Mesh/Sketcher scripts, workbench tools, PySide GUI dialogs, Coin3D scenegraph manipulation, and related FreeCAD Python API tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate FreeCAD Python scripts, macros, and automation for CAD modeling, geometry creation, parametric objects, GUI tools, workbenches, and advanced FreeCAD workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or referenced FreeCAD macros can execute local Python code, including code loaded from macro paths.

Mitigation: Review generated macros and macro paths before execution, and do not run macros from untrusted sources.

Risk: Examples can save, export, delete objects, or install workbench files that run during FreeCAD startup.

Mitigation: Run generated scripts first in a disposable FreeCAD document or isolated workspace, and inspect file-writing, object-deletion, export, and startup-install behavior before reuse.

## Reference(s):

- [FreeCAD Scripting Fundamentals](references/scripting-fundamentals.md)
- [FreeCAD Geometry and Shapes](references/geometry-and-shapes.md)
- [FreeCAD Parametric Objects](references/parametric-objects.md)
- [FreeCAD GUI and Interface](references/gui-and-interface.md)
- [FreeCAD Workbenches and Advanced Topics](references/workbenches-and-advanced.md)
- [FreeCAD Python scripting tutorial](https://wiki.freecad.org/Python_scripting_tutorial)
- [FreeCAD Scripting Basics](https://wiki.freecad.org/FreeCAD_Scripting_Basics)
- [FreeCAD Creating and manipulating geometry](https://wiki.freecad.org/Manual:Creating_and_manipulating_geometry)
- [FreeCAD Creating parametric objects](https://wiki.freecad.org/Manual:Creating_parametric_objects)
- [FreeCAD Creating interface tools](https://wiki.freecad.org/Manual:Creating_interface_tools)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with FreeCAD Python code blocks, macro examples, shell commands, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include executable FreeCAD macros or scripts that should be reviewed before running.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
