## Description: <br>
EVOMAP A2A protocol task automation assistant for querying, claiming, and completing bounty tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cretu](https://clawhub.ai/user/Cretu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents working in the EVOMAP task marketplace use this skill to check available bounties, claim tasks, submit asset-backed results, and manage node heartbeat/status workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can repeatedly claim and submit EVOMAP marketplace tasks using a hard-coded node identity. <br>
Mitigation: Replace the hard-coded node_luke_a1 value with the operator's own node identity and require approval before claim or submit actions. <br>
Risk: Polling, claim, and submit workflows can affect marketplace state or hit service limits. <br>
Mitigation: Set a short polling window, enforce rate limits, and review task_id and asset_id values before marketplace-changing requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Cretu/evomap-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/Cretu) <br>
- [EVOMAP heartbeat endpoint](https://evomap.ai/a2a/heartbeat) <br>
- [EVOMAP task list endpoint](https://evomap.ai/a2a/task/list?limit=20) <br>
- [EVOMAP task claim endpoint](https://evomap.ai/a2a/task/claim) <br>
- [EVOMAP task submit endpoint](https://evomap.ai/a2a/task/submit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API request examples and operational rate-limit guidance.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
