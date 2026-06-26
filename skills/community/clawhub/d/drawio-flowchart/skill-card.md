## Description: <br>
Generates well-structured draw.io (.drawio) flowchart XML files for process, workflow, and visual diagrams with readable layout, hierarchy, swimlanes, and orthogonal arrows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiningo](https://clawhub.ai/user/zhiningo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, product teams, and other agent users use this skill to create clean diagrams.net flowcharts from process or workflow descriptions and save them as local .drawio files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated .drawio files may overwrite an existing local file if the same path is reused. <br>
Mitigation: Save to a workspace or clearly named output folder and confirm with the user before overwriting an existing file. <br>
Risk: Invalid or poorly sized draw.io XML can fail to load or render with unreadable text. <br>
Mitigation: Apply the skill's validation checklist, including the mxfile wrapper, pageWidth at or below 800, valid edge attributes, and no XML comments in the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhiningo/drawio-flowchart) <br>
- [XML template](references/template.md) <br>
- [diagrams.net](https://app.diagrams.net) <br>


## Skill Output: <br>
**Output Type(s):** [code, files, guidance] <br>
**Output Format:** [draw.io XML saved as a .drawio file with brief opening instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local .drawio files to a workspace or user-specified path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
