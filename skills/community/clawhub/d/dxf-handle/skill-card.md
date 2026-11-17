## Description:

Dxf Handle helps agents process DWG/DXF CAD drawings with ezdxf to traverse configured layers and calculate room areas or perimeters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapleslove](https://clawhub.ai/user/mapleslove)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and CAD workflow maintainers use this skill to run local DWG/DXF measurement commands against configured room layers, then report area or perimeter results and optionally export CSV data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local CAD files and can write CSV output to a user-specified path.

Mitigation: Run it in a virtual environment, review the input and output paths before execution, and avoid writing CSV files over important local files.

Risk: The skill depends on ezdxf for CAD parsing.

Mitigation: Install ezdxf in an isolated environment and consider pinning it to a reviewed version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mapleslove/skills/dxf-handle)
- [Layer configuration example](artifact/references/layers.json)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, CSV]

**Output Format:** [Markdown guidance with command examples, terminal output, and optional CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local DWG/DXF files and a JSON layer configuration; optional CSV export writes to the user-specified output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
