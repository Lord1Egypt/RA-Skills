## Description: <br>
Action Guard helps agents avoid duplicate external actions by checking a local action log before acting and recording successful actions afterward. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wrentheai](https://clawhub.ai/user/wrentheai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to reduce repeat posts, replies, messages, transfers, deployments, and webhook calls across sessions. It is intended for workflows where an agent should check whether an external action was already completed before attempting it again. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local action log can contain sensitive targets or notes if users record them directly. <br>
Mitigation: Keep the .action-guard directory private and avoid recording secrets or highly sensitive personal details in notes or target IDs. <br>
Risk: Duplicate-action checks do not replace review for irreversible actions. <br>
Mitigation: Keep normal human approval for money movement, public posts, emails, production deploys, and other irreversible actions. <br>


## Reference(s): <br>
- [Action Guard on ClawHub](https://clawhub.ai/wrentheai/action-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and CLI output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The record command appends local JSONL entries under .action-guard/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
