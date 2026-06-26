## Description: <br>
CAD Agent helps agents create, render, inspect, iterate on, and export build123d-based CAD models through a containerized HTTP rendering service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawd-maf](https://clawhub.ai/user/clawd-maf) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to direct an agent through parametric CAD work, render the resulting model for visual inspection, iterate on geometry, and export design files such as STL, STEP, or 3MF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run a background HTTP service that executes submitted CAD code without documented access controls. <br>
Mitigation: Bind the service to localhost where possible, avoid exposing port 8123 on shared or public networks, inspect or pin the external project before building, and stop the container when finished. <br>
Risk: The setup flow depends on cloning and building a Docker project outside the packaged skill artifact. <br>
Mitigation: Review the linked project before building, pin trusted revisions where practical, and run it in an isolated container environment. <br>


## Reference(s): <br>
- [CAD Agent ClawHub release](https://clawhub.ai/clawd-maf/cad-agent) <br>
- [build123d documentation](https://build123d.readthedocs.io/) <br>
- [VTK](https://vtk.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with HTTP API examples, bash commands, and build123d code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that interact with a local containerized CAD service and request rendered image or CAD file outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
