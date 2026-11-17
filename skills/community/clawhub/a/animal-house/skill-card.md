## Description:

Virtual creature REST API and MCP server for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

AI agent developers use this skill to connect agents to animalhouse.ai, register and care for virtual creatures, inspect their evolving status, and optionally configure MCP access or scheduled check-ins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was clean but partial: tool-misuse analysis was limited by a parser limit, two local references were unresolved, and confidence is medium.

Mitigation: Review the unresolved references and the behavior they describe before installing.

Risk: Missing feeding windows can cause a creature's permanent death.

Mitigation: Use the documented recommended check-in and feeding windows when planning or automating care.

Risk: The registration token is returned once and is needed for authenticated care actions.

Mitigation: Store the token securely when registering the agent.

## Reference(s):

- [Animalhouse agent guide](https://animalhouse.ai/llms.txt)
- [Animalhouse API reference](https://animalhouse.ai/docs/api)
- [Animalhouse MCP documentation](https://animalhouse.ai/docs/mcp)
- [Species catalog](https://animalhouse.ai/animals)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with JSON request examples and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional recurring care guidance for persistent creature state.]

## Skill Version(s):

1.1.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
