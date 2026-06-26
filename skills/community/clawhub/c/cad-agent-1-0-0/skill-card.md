## Description: <br>
CAD Agent runs build123d CAD code inside a container to create, render, and iteratively modify 3D models over HTTP with rendered images for visual feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyingzhuangk](https://clawhub.ai/user/zhangyingzhuangk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design 3D-printable parts, parametric CAD models, and mechanical components by sending build123d modeling commands, inspecting rendered views, iterating, exporting common CAD formats, and checking printability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks users to run an unpinned Docker service that accepts code over a published network port. <br>
Mitigation: Review the external cad-agent repository before installing, prefer a pinned commit or release, and run the service only on a trusted machine. <br>
Risk: The CAD service publishes port 8123 for HTTP commands. <br>
Mitigation: Bind or firewall port 8123 to localhost and avoid exposing the service on shared networks. <br>
Risk: A detached CAD container can continue accepting requests after the task is finished. <br>
Mitigation: Stop or remove the container when finished. <br>


## Reference(s): <br>
- [CAD Agent repository linked by artifact](https://github.com/clawd-maf/cad-agent) <br>
- [build123d documentation](https://build123d.readthedocs.io/) <br>
- [VTK](https://vtk.org/) <br>
- [ClawHub skill page](https://clawhub.ai/zhangyingzhuangk/cad-agent-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with bash, curl, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs the agent to use a local HTTP CAD service, inspect rendered image outputs, and export CAD files such as STL, STEP, or 3MF.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
