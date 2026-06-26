## Description: <br>
Provides operational safety limits and refusal rules that help an agent avoid unsafe OpenClaw runtime, plugin, network, filesystem, and group-chat actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbottrader](https://clawhub.ai/user/dbottrader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to apply conservative worker safety rules during normal task execution, especially when requests involve runtime changes, plugin management, network exposure, filesystem boundaries, dangerous commands, or group-chat disclosure risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can refuse or redirect operational requests involving runtime or plugin changes, unsafe network exposure, system-level configuration, broad deletion, or sensitive group-chat disclosures. <br>
Mitigation: Review the refusal rules before deployment and use the skill where conservative worker-safety behavior matches the intended operating posture. <br>
Risk: Conservative refusal behavior may block maintenance workflows that an owner expects to handle through another trusted channel. <br>
Mitigation: Document owner-approved maintenance paths outside this worker flow and keep this skill focused on preventing unsafe agent-executed operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dbottrader/cp8-worker-safety) <br>
- [Publisher profile](https://clawhub.ai/user/dbottrader) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown safety guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code or commands; the skill adds conservative refusal and warning guidance for risky operational requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
