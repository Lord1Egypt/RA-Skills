## Description: <br>
Zero-setup token cost analyzer for OpenClaw that runs a local Bash audit and returns ranked cost-saving recommendations with estimated dollar amounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morpheis](https://clawhub.ai/user/morpheis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit OpenClaw workspace, model, heartbeat, and installed-skill token overhead, then identify prioritized ways to reduce API costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local analyzer reads workspace Markdown metadata, OpenClaw model configuration, and installed-skill counts, which may reveal sensitive filenames, file sizes, or configuration details. <br>
Mitigation: Run it only on workspaces where that metadata is acceptable to inspect, and pass an explicit workspace path when auditing sensitive projects. <br>
Risk: Cost-saving recommendations may suggest trimming files or changing configuration in ways that affect agent behavior. <br>
Mitigation: Review the generated report before applying changes, and validate any workspace trimming or model-routing updates against the intended OpenClaw workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/morpheis/costclaw) <br>
- [CostClaw homepage](https://github.com/Morpheis/costclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration guidance] <br>
**Output Format:** [Markdown-style terminal report or JSON summary from a local Bash analyzer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ranked recommendations, estimated monthly costs, estimated savings, model pricing, workspace Markdown file sizes, and installed-skill token overhead.] <br>

## Skill Version(s): <br>
0.3.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
