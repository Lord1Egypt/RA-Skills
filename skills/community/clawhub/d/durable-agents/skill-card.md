## Description: <br>
Build autonomous multi-agent pipelines with Mastra for agents and Trigger.dev for durable workflows, task retries, handoffs, database persistence, and permissioned tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ainakwalamonk](https://clawhub.ai/user/ainakwalamonk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design and scaffold durable multi-agent pipelines with Mastra agents, Trigger.dev tasks, typed tool contracts, handoffs, persistence, and review checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can give an agent broad local authority over credentials, databases, Docker resources, and authentication tokens. <br>
Mitigation: Install only in an isolated development environment, provide dedicated scoped LLM credentials, and require manual approval before Docker volume deletion, database authentication changes, token regeneration, or writing credentials. <br>
Risk: The skill depends on external setup commands and a cloned project that should not be trusted blindly. <br>
Mitigation: Review and pin the external repository before running setup, then inspect generated configuration and command effects before using the pipeline. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ainakwalamonk/durable-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include setup commands, architecture patterns, schemas, and permission-gating guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
