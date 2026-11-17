## Description:

Runs Cargo actions and workflows, launches batches, messages AI agents, builds and diagrams workflows, and queries orchestration history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to manage Cargo actions and workflows from an agent, including testing, batch execution, and run-history queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conflicting record-selection instructions and incomplete replay safeguards could lead to unintended processing or repeated business actions.

Mitigation: Before live runs, set filters to the intended audience and approve the exact records and cost. Check completed steps before retrying; use approved files and provider connections, restrict account permissions, and pin a reviewed CLI version.

## Reference(s):

- [Cargo Orchestration on ClawHub](https://clawhub.ai/cargo-ai/skills/cargo-orchestration)
- [Cargo skills project homepage (skill metadata)](https://github.com/getcargohq/cargo-skills)
- [Node selection guide](references/node-selection.md)
- [Node creation reference](references/nodes.md)
- [Batch and play examples](references/examples/plays.md)
- [Orchestration query examples](references/examples/queries.md)
- [Troubleshooting reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Text, Markdown]

**Output Format:** [Markdown with shell commands, JSON workflow definitions, SQL queries, and workflow diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may initiate live runs, batches, messages, or workflow changes when executed.]

## Skill Version(s):

1.18.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
