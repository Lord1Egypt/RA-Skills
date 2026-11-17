## Description:

Build agent product UIs with Candor UI, a shadcn/ui registry of React components for agents that do real work - approvals, plans, diffs, run logs, chat and tool calls, traces and evals, and the app shell around them. Use when building or changing a React or Next.js interface for an AI agent, when the project's components.json lists the @candor registry, or when the user mentions Candor. Covers installing components, choosing the right one, wiring the Vercel AI SDK, Claude Agent SDK or AG-UI adapter, and the honesty rules every Candor screen follows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arunk3](https://clawhub.ai/user/arunk3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building React or Next.js agent interfaces use Candor UI to add components for conversations, approvals, plans, diffs, run activity, traces, and evaluations, and connect those interfaces to the Vercel AI SDK, Claude Agent SDK, or AG-UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting the remote MCP server may send data to an external service.

Mitigation: Review the remote setup and data handling before connecting, and proceed only if the data sent is acceptable.

Risk: The theme workflow may share local CSS with an external service.

Mitigation: Inspect the CSS and what will be sent; remove sensitive content or avoid sharing it if the transfer is not acceptable.

Risk: Commands that use changeable package versions can install code that differs between runs; the security review also reports incomplete analysis.

Mitigation: Use exact, reviewed package versions and review fetched package content before running installation commands.

## Reference(s):

- [Candor UI components](references/components.md)
- [Candor UI design system](references/design.md)
- [Candor principles](https://candor.themethodic.com/principles)
- [Candor documentation index](https://candor.themethodic.com/llms.txt)
- [Candor UI docs MCP server](https://candor.themethodic.com/mcp)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [React and TypeScript code, configuration examples, shell commands, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

6.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
