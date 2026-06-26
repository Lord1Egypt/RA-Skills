## Description: <br>
Run structured multi-step workflows through the FlowForge engine so agents can follow ordered YAML workflows without skipping required steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kagura-agent](https://clawhub.ai/user/kagura-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run ordered FlowForge workflows for multi-step work such as code contribution, research, and review tasks. It is useful when tasks need explicit sequencing, branching, sub-agent delegation, and persisted workflow state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External CLI execution can be triggered by broad workflow requests. <br>
Mitigation: Install the FlowForge npm CLI only from a trusted source, verify the workflow selected before starting it, and review each CLI action before advancing. <br>
Risk: Workflow YAML can direct sub-agent actions, code pushes, PR creation, deployment, deletion, public posting, or credential use. <br>
Mitigation: Review workflow YAML before running it and require explicit approval gates for impactful or credential-bearing steps. <br>
Risk: FlowForge state and daily logs may retain sensitive task summaries. <br>
Mitigation: Avoid storing secrets or sensitive details in workflow results, treat local FlowForge state as retained records, and clear local state when it is no longer needed. <br>


## Reference(s): <br>
- [FlowForge Skill Listing](https://clawhub.ai/kagura-agent/agent-flowforge) <br>
- [FlowForge Setup Guide](setup.md) <br>
- [FlowForge YAML Format](references/yaml-format.md) <br>
- [Code Contribution Workflow Example](references/examples/code-contribution.yaml) <br>
- [Research Workflow Example](references/examples/research.yaml) <br>
- [Review Workflow Example](references/examples/review.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses FlowForge CLI JSON actions to guide workflow execution and advancement.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
