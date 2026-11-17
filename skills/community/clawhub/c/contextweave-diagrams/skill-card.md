## Description:

Contextweave Diagrams helps agents transform complex text, architecture notes, business processes, mind maps, and knowledge-base content into structured diagram-generation requests for ContextWeave.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qhyw99](https://clawhub.ai/user/qhyw99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to convert complex requirements, system logic, or long-form knowledge into structured diagram requests and returned generation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the current diagram request to a configured ContextWeave backend, which may expose sensitive document content if users submit confidential material.

Mitigation: Confirm the backend is trusted and that its privacy and retention terms are acceptable before using confidential or regulated inputs.

Risk: The skill creates request files in the current workspace and attempts a Node-based generation command during normal use.

Mitigation: Review generated request files and run the skill in a workspace where those files and command execution are expected.

## Reference(s):

- [Contextweave Diagrams on ClawHub](https://clawhub.ai/qhyw99/skills/contextweave-diagrams)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Single JSON object with request-file path, execution status, session identifier, result fields, and error details when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node, CONTEXTWEAVE_MCP_API_KEY, and CONTEXTWEAVE_API_URL; request files are created in the current workspace before backend generation.]

## Skill Version(s):

0.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
