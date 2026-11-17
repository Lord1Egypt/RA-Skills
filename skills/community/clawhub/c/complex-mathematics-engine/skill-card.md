## Description:

Complex Mathematics Engine lets an agent evaluate mathematical expressions through AgentPMT-hosted remote tool calls using SymPy for symbolic math, NumPy for numerical work, or SciPy for scientific computing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route calculus, algebra, linear algebra, statistics, optimization, and scientific-computing expressions to the AgentPMT Complex Mathematics Engine. It is useful when an agent needs a documented remote calculate action, input schema, setup path, and response-handling guidance for math requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags broad activation terms and unpinned setup-install commands for review.

Mitigation: Review activation behavior before deployment and prefer pinned or verified install sources for referenced setup skills.

Risk: Math expressions are sent to AgentPMT-hosted remote tool calls and may consume credits.

Mitigation: Avoid secrets or sensitive business data in expressions, confirm credit costs before use, and keep inputs limited to the minimum needed for the calculation.

## Reference(s):

- [Complex Mathematics Engine schema](artifact/schema.md)
- [Complex Mathematics Engine marketplace page](https://www.agentpmt.com/marketplace/complex-mathematics-engine)
- [Complex Mathematics Engine ClawHub page](https://clawhub.ai/agentpmt/skills/complex-mathematics-engine)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown instructions with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The remote calculate action returns JSON-serializable math results with the original expression, engine used, execution timing, result fields, and metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
