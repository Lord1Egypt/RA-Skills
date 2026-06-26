## Description: <br>
AI agent operating-authority management system for checking autonomy level before external actions, deciding level changes, and running weekly self-review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators and developers use this skill to gate an AI agent's external actions against an explicit autonomy level, approved channels, probation status, and review history. It is intended to keep final authority with the operator while documenting level changes and weekly self-evaluations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can allow external messages, deployment or service actions, and persistent self-governance logs without concrete operational boundaries. <br>
Mitigation: Define exact approved channels, approved templates, log retention rules, and redaction expectations before enabling it with real external tools. <br>
Risk: Autonomy level changes, service shutdowns, deployments, and spending could exceed the operator's intended authority model. <br>
Mitigation: Require explicit operator approval for level changes, service shutdowns, deployments, spending, account actions, irreversible deletion, and any action outside the approved channel list. <br>
Risk: The current state indicates L4a limited external behavior during probation, which permits approved-channel outbound actions after checks. <br>
Mitigation: Keep final authority with the operator, review probation status before each external action, and stop for approval when an action is not reversible or not covered by the approved channels and templates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/autonomy-gate) <br>
- [Autonomy state reference](references/state.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with JSON state references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces policy checks, approval prompts, level-change guidance, logging expectations, and state-file updates for agent autonomy governance.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
