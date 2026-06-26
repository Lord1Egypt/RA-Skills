## Description: <br>
Reports AI agent status, heartbeat events, and current task summaries to a ClawHQ dashboard through authenticated API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zachmael](https://clawhub.ai/user/zachmael) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to make agent activity visible in ClawHQ by reporting session state, task descriptions, and heartbeat timestamps. It is intended for teams that want lightweight operational monitoring of agent status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task summaries, status updates, and heartbeat data are sent to ClawHQ. <br>
Mitigation: Use the skill only when off-device monitoring is intended, and avoid including secrets or customer-sensitive details in task descriptions. <br>
Risk: The required CLAWHQ_API_KEY can authorize reporting to the dashboard if exposed. <br>
Mitigation: Store CLAWHQ_API_KEY in environment or secret management and do not paste it into prompts, task summaries, logs, or shared files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zachmael/clawhq-dashboard) <br>
- [ClawHQ dashboard](https://app.clawhq.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash and PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWHQ_API_KEY and sends HTTPS API requests to ClawHQ.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
