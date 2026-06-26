## Description: <br>
Ask non-blocking clarifying questions during agent workflows when agents need user input without halting execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennyzir](https://clawhub.ai/user/kennyzir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this local helper to ask users for deployment decisions, code review confirmations, data validation choices, and security-related answers while an agent workflow continues. It returns a selected or default answer with timeout metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Timeout defaults can stand in for explicit human approval in sensitive workflows. <br>
Mitigation: Use fail-closed defaults such as no, skip, or staging, and avoid timeout defaults for production, deletion, credential, account, or security actions. <br>
Risk: Question context is displayed in local console or log output. <br>
Mitigation: Do not place secrets, credentials, customer data, or incident details in the question or context fields. <br>


## Reference(s): <br>
- [btw command on ClawHub](https://clawhub.ai/kennyzir/btw-command) <br>
- [btw GitHub project](https://github.com/kennyzir/btw) <br>
- [Claw0x skills](https://claw0x.com/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object with answer, answered_at, timed_out, and response_time_ms fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the user answer or configured default after timeout; context may be surfaced in local logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
