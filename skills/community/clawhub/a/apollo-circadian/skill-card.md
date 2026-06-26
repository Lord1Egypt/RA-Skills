## Description: <br>
Helps an agent choose suitable work rhythms by identifying when to do deep thinking, routine work, or cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to align task selection with a configured circadian schedule, including deep-work windows, low-effort periods, cleanup windows, and emergency-only hours. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation triggers and heartbeat integration may cause the skill to influence routine task scheduling more often than intended. <br>
Mitigation: Review the configured triggers and heartbeat behavior before enabling the skill in shared or high-volume agent environments. <br>
Risk: The skill uses a hardcoded Asia/Shanghai personal schedule, which may produce unsuitable recommendations for other users or time zones. <br>
Mitigation: Confirm the schedule and time zone match the intended user before relying on the recommendations. <br>
Risk: The helper writes local phase-state data under a root-oriented workspace path. <br>
Mitigation: Review the state path before use in non-root or shared environments and adjust deployment permissions accordingly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nic-yuan/apollo-circadian) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/nic-yuan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style circadian reports, shell command output, and local JSON phase-state metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured Asia/Shanghai schedule and reports the current phase, recommended task class, efficiency match, and time until the next phase.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
