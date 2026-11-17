## Description:

Figma Implement Design guides an agent through using Figma MCP design context, screenshots, and assets to translate Figma nodes into production-ready code with close visual fidelity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tbeard602](https://clawhub.ai/user/tbeard602)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement Figma frames or components in an existing codebase by fetching design context, screenshots, and assets, then adapting them to project conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow connects the agent to Figma MCP and may expose Figma design context or screenshots to the agent.

Mitigation: Install only when Figma MCP access is acceptable, and verify the open Figma file, URL, node ID, or selected desktop node before fetching context or screenshots.

Risk: Generated UI code can diverge from the source design or project accessibility requirements.

Mitigation: Validate the implementation against the Figma screenshot, design context, project design system, responsive behavior, and accessibility checks before accepting the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tbeard602/skills/figma-implement-design)
- [Figma MCP Server Documentation](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma MCP Server Tools and Prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
- [Guide to Variables in Figma](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline commands and code-oriented implementation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authorized Figma MCP connection and a target Figma URL, node ID, or desktop selection.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
