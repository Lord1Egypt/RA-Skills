## Description:

Deep Research Pipeline turns broad questions into cited reports through planning, multi-query retrieval, chunk selection, analysis, reflection, writing, and optional verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vardhineediganesh877-ui](https://clawhub.ai/user/vardhineediganesh877-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research-oriented agents use this skill to run multi-source investigations, synthesize findings, track contradictions and gaps, and produce cited reports or structured research outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound web, GitHub, documentation, and LLM-provider requests.

Mitigation: Use it only in environments where that outbound access is acceptable, prefer trusted HTTPS endpoints, and review source lists before relying on generated research.

Risk: Research topics, retrieved content, and intermediate findings may be sent to configurable LLM endpoints.

Mitigation: Avoid confidential research topics unless you control or have approved the provider endpoint and workspace; review custom LLM_API_BASE, OPENAI_BASE_URL, OPENAI_API_BASE, and ZAI_API_ENDPOINT values before use.

Risk: Generated reports, checkpoints, and provenance files may retain sensitive research data.

Mitigation: Write outputs to approved locations, manage retention deliberately, and treat generated files as sensitive when the research topic is sensitive.

## Reference(s):

- [Deep Research Pipeline on ClawHub](https://clawhub.ai/vardhineediganesh877-ui/skills/deep-research-pipeline)
- [Deep Research Pipeline Skill Documentation](DOCS.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, executive summaries, bullet briefs, or structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports report, summary, brief, and json formats with checkpoint/resume, time limits, token budgets, and mock mode.]

## Skill Version(s):

2.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
