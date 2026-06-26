## Description: <br>
Adds causal reasoning to agent actions by logging interventions and outcomes, estimating treatment effects, planning counterfactuals, debugging failures, and backfilling activity history for analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oswalpalash](https://clawhub.ai/user/oswalpalash) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to add causal logging, counterfactual reasoning, and treatment-effect estimation to high-level actions such as communication, scheduling, files, deployments, purchases, and task workflows. It supports planning interventions, debugging failed outcomes, and backfilling historical activity into local causal logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can import sensitive email, calendar, and message history into persistent local causal logs. <br>
Mitigation: Use narrow time ranges and allowed domains, review what will be imported before backfilling, and delete temporary exports after use. <br>
Risk: Backfill scripts may use local provider CLIs such as gog or wacli, which could access whichever accounts are configured on the machine. <br>
Mitigation: Confirm the configured provider accounts before running backfills and avoid broad imports unless the user explicitly approved them. <br>
Risk: The skill applies to high-impact actions such as purchases, deployments, permission changes, and communication-history imports. <br>
Mitigation: Require explicit approval before executing those actions and treat causal estimates as advisory rather than automatic authorization. <br>


## Reference(s): <br>
- [Causal Inference on ClawHub](https://clawhub.ai/oswalpalash/causal-inference) <br>
- [Do-Calculus Reference](references/do-calculus.md) <br>
- [Treatment Effect Estimation](references/estimation.md) <br>
- [Introduction to Causal Inference](https://www.bradyneal.com/causal-inference-course) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, YAML, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local causal logs, graph definitions, estimates, and configuration files when the agent follows the skill.] <br>

## Skill Version(s): <br>
0.2.0 (source: server evidence release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
