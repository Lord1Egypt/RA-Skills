## Description: <br>
Automatically detects and repairs conflicting Feishu channel configuration in OpenClaw, preserving the complete channel and helping restore bot responsiveness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuxuebin20260309](https://clawhub.ai/user/liuxuebin20260309) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and maintainers use this skill to clean duplicate Feishu channel entries in the local OpenClaw configuration, merge allowlists and direct-message policy, and prepare the gateway for restart. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite ~/.openclaw/openclaw.json, remove one duplicate Feishu channel entry, and clean unrecognized fields. <br>
Mitigation: Use it only to repair Feishu channel conflicts in OpenClaw and keep the generated .bak backup available in case gateway behavior changes after restart. <br>


## Reference(s): <br>
- [Feishu Channel Cleaner on ClawHub](https://clawhub.ai/liuxuebin20260309/feishu-channel-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text status messages and configuration file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a .bak backup before updating the OpenClaw configuration.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
