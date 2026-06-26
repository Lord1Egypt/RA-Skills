## Description: <br>
Guides an agent in using the Cargo CLI to run actions, workflows, batches, AI-agent messages, orchestration SQL queries, segment fetches, and model inspections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cargo-ai](https://clawhub.ai/user/cargo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to operate Cargo orchestration from an agent: discovering resources, running tools, actions, workflows, and batches, monitoring asynchronous work, querying runtime history, and troubleshooting workflow behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Cargo credentials and can let an agent operate a Cargo workspace. <br>
Mitigation: Use least-privilege Cargo tokens or OAuth sessions, verify the active workspace with cargo-ai whoami, and revoke credentials when agent access is no longer needed. <br>
Risk: Commands can run or modify Cargo workflows and may write to CRM-connected or other integrated systems. <br>
Mitigation: Test workflow, batch, and CRM-writing examples in a sandbox first, validate node graphs before deployment, and review proposed commands before execution. <br>
Risk: Workflow and segment operations can process sensitive or regulated data. <br>
Mitigation: Avoid uploading regulated or sensitive data unless Cargo and connected third-party services are approved by the organization. <br>


## Reference(s): <br>
- [Cargo Orchestration listing](https://clawhub.ai/cargo-ai/cargo-orchestration) <br>
- [Cargo skills homepage](https://github.com/getcargohq/cargo-skills) <br>
- [Action examples](references/examples/actions.md) <br>
- [Tool examples](references/examples/tools.md) <br>
- [Play examples](references/examples/plays.md) <br>
- [AI agent examples](references/examples/agents.md) <br>
- [Orchestration query examples](references/examples/queries.md) <br>
- [Segment data examples](references/examples/segments.md) <br>
- [Orchestration templates](references/examples/templates.md) <br>
- [Creating nodes](references/nodes.md) <br>
- [Node selection](references/node-selection.md) <br>
- [Filter syntax](references/filter-syntax.md) <br>
- [Async polling reference](references/polling.md) <br>
- [Response shapes](references/response-shapes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Cargo CLI commands that execute or modify workflows and connected data when run with valid credentials.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
