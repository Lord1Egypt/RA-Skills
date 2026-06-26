## Description: <br>
Monitors and maintains health and connectivity for the Axioma Stellaris cluster agents Merlin, Ezekiel, and Morgana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check local Axioma Stellaris service health, inspect cluster connectivity, and plan remediation for Merlin, Ezekiel, and Morgana. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move beyond monitoring into administrative remediation such as service restarts, SSH tunnel changes, process termination, data deletion, or writing incident notes. <br>
Mitigation: Require explicit user approval before any state-changing action and treat generated remediation as an operations runbook for the named local services. <br>
Risk: Broad remediation guidance without clear safe limits can affect the wrong local service or cluster component. <br>
Mitigation: Verify the target service, port, and cluster agent before running commands, and prefer read-only health checks before proposing changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/chinese-axioma-cluster-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local service health summaries, endpoint checks, and operational remediation suggestions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence; artifact text lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
