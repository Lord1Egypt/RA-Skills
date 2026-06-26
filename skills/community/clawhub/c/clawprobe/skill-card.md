## Description: <br>
Clawprobe monitors OpenClaw agent health, token usage, API cost, context window state, compaction events, and optimization suggestions from the CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuhao6741](https://clawhub.ai/user/liuhao6741) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect their own OpenClaw runtime health, context utilization, estimated costs, active suggestions, and compaction history before or during expensive work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external npm package and linked repository that are outside NVIDIA ownership. <br>
Mitigation: Verify the `clawprobe` npm package, linked repository, and selected version before installation. <br>
Risk: The monitoring daemon runs in the background after it is started. <br>
Mitigation: Understand how to stop or uninstall the daemon before enabling monitoring in an agent environment. <br>
Risk: JSON output from session, context, and compaction commands may expose sensitive operational details. <br>
Mitigation: Treat command output as sensitive and avoid sharing it outside trusted logs or workflows. <br>


## Reference(s): <br>
- [ClawProbe homepage](https://github.com/seekcontext/ClawProbe) <br>
- [ClawHub skill page](https://clawhub.ai/liuhao6741/clawprobe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON command output may include session, context, cost, compaction, and suggestion details.] <br>

## Skill Version(s): <br>
0.6.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
