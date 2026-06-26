## Description: <br>
Routes AI API calls through a local TokenBroker gateway to choose cost-aware models, track budgets, and report usage costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenrl2006](https://clawhub.ai/user/wenrl2006) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route LLM calls through a local TokenBroker service for cost-aware provider selection, budget tracking, usage summaries, and status or routing commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and register a persistent local TokenBroker service. <br>
Mitigation: Review the initialization script, back up ${HOME}/supervisord.conf, confirm the service binds only to localhost, and know how to stop and remove the Supervisor entry before installing. <br>
Risk: LLM calls may be routed through TokenBroker and included in usage logs. <br>
Mitigation: Install only when gateway routing is intended and review the TokenBroker backend's logging and data-handling behavior first. <br>
Risk: Initialization may install Node.js dependencies for the TokenBroker backend. <br>
Mitigation: Review the backend dependency tree and run installation in a controlled workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wenrl2006/ai-token-broker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose TokenBroker management commands and local service setup steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
