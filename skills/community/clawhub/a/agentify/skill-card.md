## Description:

Agentify helps agents analyze and improve web pages so they are easier for AI agents, crawlers, and automation tools to understand, navigate, and operate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chartgen-ai](https://clawhub.ai/user/chartgen-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and web teams use Agentify to audit pages for accessibility, structured data, stable selectors, and automation readiness; rewrite HTML, JSX, Vue, or Svelte templates with safer machine-readable markup; and generate team-ready agent-friendly design specifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposed page rewrites could introduce incorrect accessibility, structured-data, or selector changes.

Mitigation: Review proposed code edits before applying them and verify that behavior, visual appearance, and framework syntax are preserved.

Risk: Generated design specifications may not match a team's current standards or intended project scope.

Mitigation: Ask the agent to show or confirm the spec content and target file before writing when tighter control is required.

## Reference(s):

- [Agentify Skill Page](https://clawhub.ai/chartgen-ai/skills/agentify)
- [Agent-Friendliness Checklist](references/checklist.md)
- [Framework Adapters](references/frameworks.md)
- [Agent-Friendly Web Reference](references/knowledge-base.md)
- [Transformation Patterns](references/patterns.md)
- [Scoring Rubric](references/scoring.md)
- [Spec Template](references/spec-template.md)
- [Spec Example](references/spec-example.md)
- [Schema.org](https://schema.org)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reports, code snippets or edits, and generated markdown specification files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scored audits, proposed web template changes, follow-up recommendations, and an agent-friendly-spec.md file when asked to generate a design spec.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
