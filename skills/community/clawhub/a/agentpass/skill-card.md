## Description: <br>
Control Home Assistant devices through the agentpass security gateway, including read-only device queries and approval-gated state changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[torbenwetter](https://clawhub.ai/user/torbenwetter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Home Assistant device state and route smart home control requests through the agentpass gateway with Telegram approval for state-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The AGENT_TOKEN environment variable can authorize access to the configured agentpass gateway. <br>
Mitigation: Treat AGENT_TOKEN as sensitive, restrict its scope where possible, and install the CLI only in trusted agent environments. <br>
Risk: Read-only Home Assistant queries can expose device names, occupancy signals, history, logbook entries, and configuration. <br>
Mitigation: Limit use to trusted users and avoid sharing command output outside the intended Home Assistant administration context. <br>
Risk: State-changing Home Assistant service calls can affect physical smart home devices. <br>
Mitigation: Use the approval-gated commands as documented and verify tool names and arguments before submitting control requests. <br>


## Reference(s): <br>
- [ClawHub agentpass skill page](https://clawhub.ai/torbenwetter/agentpass) <br>
- [agentpass GitHub homepage declared by the skill](https://github.com/TorbenWetter/agentpass) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [State-changing commands can block for up to 15 minutes while Telegram approval resolves.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
