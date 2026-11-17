## Description:

Guides agents in designing AI/LLM-capable systems that handle uncertainty, select agent patterns, expose AI-friendly APIs, and plan context engineering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ganjiakoun16](https://clawhub.ai/user/ganjiakoun16)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to decide when AI-friendly architecture is appropriate and to design agent layers, model management, context engineering, API boundaries, evaluation, and fallback patterns for LLM-enabled systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Architecture recommendations may be unsuitable if applied without considering the project domain, constraints, or evaluation results.

Mitigation: Review proposed designs against project requirements, regulatory constraints, and measurable evaluation criteria before implementation.

Risk: Optional LLM evaluation integration can introduce dependency and credential exposure risks.

Mitigation: Run optional provider integrations in an isolated environment with pinned dependencies and keep credentials out of prompts, artifacts, and logs.

Risk: If the API error-handling guidance is applied literally, detailed stack traces could be exposed to users or agents.

Mitigation: Return concise errors to users and agents while keeping detailed diagnostics in protected logs.

## Reference(s):

- [Article Summary](references/article-summary.md)
- [Evaluation Criteria and Benchmark Tests](references/evals.md)
- [Test Scenarios](references/test-scenarios.md)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [Skill Authoring Guide](https://github.com/GanJiaKouN16/Function-Point-Skill/blob/main/skill-authoring-guide.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with architecture recommendations, decision criteria, and code or configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include architecture diagrams, decision tables, API shape examples, and evaluation suggestions.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
