## Description:

Teaches agents how to query, expand, and cleanly commit technical, design, and product constraints to the Elen SQLite decision graph via the Elen Context Server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicoizco](https://clawhub.ai/user/nicoizco)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to make agents query prior Elen decisions before substantial work and record new technical, design, security, or product decisions in a local decision graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the external @learningnodes/elen-mcp@0.1.1 npm package for MCP server behavior.

Mitigation: Install only after reviewing the package source and dependencies, and run it with minimal filesystem and environment access.

Risk: Agents may store technical, security, design, and product decisions in a persistent local decision graph.

Mitigation: Avoid storing secrets or sensitive vulnerability details, and require explicit user review before committing decisions.

Risk: The skill encourages broad workflow changes around agent decision capture with limited scoping and user-control guidance.

Mitigation: Apply the skill to meaningful decisions only and keep user approval in the loop for consequential commits or superseded decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicoizco/skills/elen-decision-network)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON configuration snippets and MCP tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an external Elen MCP server package and a persistent local SQLite decision graph.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
