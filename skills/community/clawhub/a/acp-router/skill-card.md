## Description: <br>
Routes plain-language requests for supported coding harnesses into OpenClaw ACP runtime sessions or direct acpx-driven sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yimeihuang1999-leaves](https://clawhub.ai/user/yimeihuang1999-leaves) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to route coding-agent thread requests to ACP-backed harness sessions and to recover or fall back to direct acpx sessions when runtime support is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to install tooling, restart services, run direct acpx commands, or alter ACPX configuration during recovery. <br>
Mitigation: Require explicit user confirmation before npm installs, gateway restarts, direct exec-based acpx commands, or changes to ~/.acpx/config.json. <br>
Risk: Persistent harness sessions may retain prompts or receive sensitive workspace context. <br>
Mitigation: Avoid sending secrets into persistent harness sessions and keep session names and working directories scoped to the intended task. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides routing and recovery guidance for ACP sessions and direct acpx flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
