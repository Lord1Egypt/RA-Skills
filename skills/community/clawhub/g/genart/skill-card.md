## Description: <br>
Generate algorithmic visual art -- flow fields, fractals, cellular automata, circle packing, wave patterns. SVG + PNG output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eliot-onbox](https://clawhub.ai/user/eliot-onbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, artists, and agent users use GenArt to create deterministic SVG or PNG visual art from configurable procedural algorithms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated output can overwrite files when an existing output path is reused. <br>
Mitigation: Choose dedicated output paths and review file destinations before running generation commands. <br>
Risk: Glitch input mode reads and rewrites SVG or XML content supplied by the user. <br>
Mitigation: Use glitch input only with SVG or XML files intended for modification, and keep an original copy when needed. <br>
Risk: PNG export may invoke the system rsvg-convert renderer if it is installed. <br>
Mitigation: Use a trusted local renderer for PNG conversion, or keep SVG output when raster conversion is not needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated artifacts are SVG or PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic generation is seed-based. Users choose output paths, and PNG export may use the local rsvg-convert renderer when available.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
