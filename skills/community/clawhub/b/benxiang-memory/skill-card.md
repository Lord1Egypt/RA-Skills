## Description:

Shadow Memory helps agents persist project world state in a Benxiang .origin package through an MCP server, so new sessions can recover state, commit semantic transactions, inspect history, and trace why current values changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when project progress, decisions, tasks, risks, facts, and module state need to survive across new sessions or multiple collaborating agents. It guides agents to query persisted state at session start and commit concluded work as structured transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill asks users to run and register unpinned executable code from a mutable external GitHub repository.

Mitigation: Audit or pin the referenced repository to a reviewed commit before installation, verify dependencies, and register the MCP server with only the intended .origin package access.

Risk: The MCP server persists project state, so incorrect commits or overly broad package access could affect future sessions and collaborating agents.

Mitigation: Use the skill's state, why, history, and diagnose workflows to inspect changes, and restrict the server to the intended package path without unnecessary credentials or network access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongsheng123132/skills/benxiang-memory)
- [Publisher profile](https://clawhub.ai/user/dongsheng123132)
- [Referenced Benxiang protocol repository](https://github.com/dongsheng123132/2origin.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and MCP tool descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on a Node.js MCP server registered over stdio and a local .origin package path.]

## Skill Version(s):

1.1.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
