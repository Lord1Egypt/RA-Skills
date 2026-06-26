## Description: <br>
Processes DWG/DXF CAD drawings with ezdxf to inspect configured layers and calculate area or perimeter values for room measurement workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapleslove](https://clawhub.ai/user/mapleslove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, CAD users, and automation agents use this skill to measure configured room layers in local DWG/DXF files and report area or perimeter totals. It can query one room or all configured layers and optionally export results to CSV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted or malformed CAD files may produce unreliable parsing results or expose the local parser to unsafe inputs. <br>
Mitigation: Run the tool only on CAD files from trusted sources, preferably in a constrained local environment. <br>
Risk: CSV export can overwrite an existing file at the selected output path. <br>
Mitigation: Choose the output path deliberately and check for existing files before using the --output option. <br>
Risk: The tool depends on the external Python package ezdxf. <br>
Mitigation: Install ezdxf from a trusted Python package source and keep dependency management under the user's normal review process. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mapleslove/dxf-handle) <br>
- [Layer configuration reference](references/layers.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Console text with optional CSV file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local DWG/DXF input file and layer configuration; CSV export writes to the user-selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
