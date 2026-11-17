## Description:

Audits LLM-powered agent codebases against the 12-Factor Agents methodology and produces evidence-based compliance findings and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review LLM-powered or agentic codebases against the 12-Factor Agents framework. It guides structured scanning, per-factor evidence collection, compliance scoring, gap analysis, and prioritized recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Architecture findings or recommendations may be incorrect if source evidence is incomplete or interpreted out of context.

Mitigation: Require file-level evidence for each score and review generated recommendations before applying code changes.

Risk: The skill reads source files under the codebase path provided by the user and runs search commands for evidence.

Mitigation: Run it only on intended repositories and exclude secrets or unrelated private files from the analysis scope.

## Reference(s):

- [Agent Architecture Analysis on ClawHub](https://clawhub.ai/anderskev/skills/agent-architecture-analysis)
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents)
- [Per-Factor Analysis Framework](references/factors.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with tables, file references, code snippets, compliance scores, gaps, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided codebase path and may use search commands to gather evidence before scoring.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
