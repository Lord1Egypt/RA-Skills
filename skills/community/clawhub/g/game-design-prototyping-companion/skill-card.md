## Description: <br>
Helps agents track game design prototype ideas, branching outcomes, dead ends, baselines, next experiments, and optional SVG branch maps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game designers, developers, and agent-assisted teams use this skill to preserve prototype decision trees, record what each branch taught, and decide which paths to pursue, park, or revisit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional visualization workflow writes local files and could expose or overwrite sensitive locations if paths are chosen carelessly. <br>
Mitigation: Use explicit non-sensitive input and output paths, avoid private directories, and review the generated SVG before sharing it. <br>


## Reference(s): <br>
- [Branch Map Format](references/branch-map-format.md) <br>
- [Example Branch Map](references/example-branch-map.json) <br>
- [State Labels](references/state-labels.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown responses, optional JSON branch-map data, and an SVG file path when visualization is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write branch-map JSON and render a local SVG from explicit input and output paths when visualization is requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
