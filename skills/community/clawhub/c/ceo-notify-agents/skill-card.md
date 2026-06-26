## Description: <br>
Enables a CEO user to notify other agents by writing messages to shared memory notification logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Stingan](https://clawhub.ai/user/Stingan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Operators and developers using multi-agent workflows can send short notifications from a CEO role to named agents for later retrieval through shared memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes persistent cross-agent memory from notification inputs. <br>
Mitigation: Review before installing, use only trusted messages, and ask before writing persistent shared memory. <br>
Risk: Target agent names and message content are not validated or escaped before being used in shell-managed log writes. <br>
Mitigation: Use known simple agent names, validate target names, and escape message content in a revised version. <br>
Risk: The implementation relies on hardcoded personal filesystem and OpenClaw executable paths. <br>
Mitigation: Declare shell, filesystem, and OpenClaw requirements, and replace hardcoded paths with configured environment-specific paths before use. <br>


## Reference(s): <br>
- [Ceo Notify Agents on ClawHub](https://clawhub.ai/Stingan/ceo-notify-agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text status message with persistent notification log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes per-agent and aggregate notification logs under a hardcoded shared-memory path and indexes OpenClaw memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
