## Description:

Batteries-included React/Next.js agent component from ui.inference.sh with runtime, tool lifecycle UI, streaming, approvals, widgets, and client-side tools built in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add and configure an agent UI in React/Next.js applications for AI chat interfaces, SaaS copilots, assistants, and agentic workflows with human approval and client-side tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install commands for registry components and npm packages can introduce unreviewed or changing third-party code.

Mitigation: Review and pin package and component versions before running install commands, and inspect generated files before committing them.

Risk: The integration requires an INFERENCE_API_KEY, which could be exposed if handled outside a protected environment.

Mitigation: Keep the API key in a secret-managed environment and avoid exposing it in client-side code or commits.

Risk: Client-side tools and form filling can act within the browser context and may affect user-visible page state.

Mitigation: Enable client-side tools only with clear user consent and narrow page or form scope.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/okaris/skills/agent-ui)
- [Agent Component Docs](https://ui.inference.sh/blocks/agent)
- [Agents Overview](https://inference.sh/docs/agents/overview)
- [Agent SDK](https://inference.sh/docs/api/agent/overview)
- [Human-in-the-Loop](https://inference.sh/docs/runtime/human-in-the-loop)
- [Agents That Generate UI](https://inference.sh/blog/ux/generative-ui)
- [Agent UX Patterns](https://inference.sh/blog/ux/agent-ux-patterns)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, TypeScript, and TSX code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install commands, Next.js proxy route setup, environment variable guidance, React component examples, props, related skills, and documentation links.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
