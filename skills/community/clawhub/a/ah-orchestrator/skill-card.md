## Description: <br>
Coordinates agent work by routing tasks to specialists, planning sequential or parallel execution, adding quality checks, and introducing human checkpoints for complex decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to plan and coordinate multi-agent software work, including routing tasks, sequencing dependent phases, identifying parallel workstreams, and adding review checkpoints before major decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routing and orchestration suggestions may be unsuitable for high-impact security, deployment, architecture, or large code-change decisions if accepted automatically. <br>
Mitigation: Review suggested routing, execution plans, and checkpoints before acting on security-sensitive, deployment, architecture, or broad code-change work. <br>
Risk: Prompts or checkpoint summaries could expose secrets or confidential project details if users paste sensitive data into the agent conversation. <br>
Mitigation: Avoid including secrets in prompts or checkpoint summaries, and redact sensitive project data before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mtsatryan/ah-orchestrator) <br>
- [Reference examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown plans, routing recommendations, checkpoints, and command-style agent invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; does not execute tools or install code by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
