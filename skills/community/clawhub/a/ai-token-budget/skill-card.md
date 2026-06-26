## Description: <br>
TokenBudget helps an agent estimate token use, enforce session budget limits, and choose lower-cost model tiers when budget is tight. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenrl2006](https://clawhub.ai/user/wenrl2006) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add per-task token-budget checks, budget status commands, and model-tier selection guidance to agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence model choice and budget handling across the whole agent session. <br>
Mitigation: Install it only when session-wide budget control is intended, and prefer explicit user confirmation before disabling budget limits. <br>
Risk: The skill includes an automatic localhost TokenBroker health check and installation recommendation. <br>
Mitigation: Review or remove the localhost broker behavior before use, especially in environments where local services or install prompts are restricted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wenrl2006/ai-token-budget) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript helper code and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces budget estimates, model-tier recommendations, budget status text, and session-scoped configuration guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
