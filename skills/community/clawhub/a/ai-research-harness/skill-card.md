## Description:

Cognitive discipline for AI-native scientific experimentation, used when setting up controlled experiments with LLM agents, designing reproducible evaluation pipelines, or structuring research workspaces for long-running agent collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhelunsun](https://clawhub.ai/user/zhelunsun)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and research agents use this skill to structure AI-native scientific experiments with reproducible evaluation, protected research surfaces, evidence status gates, and agent handoff practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompts, claims, rubrics, schemas, or baselines may be accepted as research-ready without sufficient review.

Mitigation: Review generated prompts before printing or sharing them, and keep the human-review gates for claims, rubrics, schemas, and baselines in place.

Risk: Research agents may overstate evidence or scale experiments before claim boundaries, artifacts, and provenance are checked.

Mitigation: Use the skill's documented calibration step before scaling: lock down claim boundaries, audit artifacts, and fix provenance gaps.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhelunsun/skills/ai-research-harness)
- [Scientific Thinking Patterns for AI-Conducted Research](references/scientific-thinking.md)
- [Experiment Design Methodology](references/experiment-design.md)
- [Methodology Grounding for Research Design](references/methodology-grounding.md)
- [Agent Collaboration & Governance](references/agent-collaboration.md)
- [Repo Architecture & Governance](references/repo-architecture.md)
- [Scoring & Statistics](references/scoring-statistics.md)
- [Agent Harness Engineering project page](https://picrew.github.io/LLM-Harness/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured schemas, checklists, workflow steps, and optional command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no installed code, hidden hooks, credential handling, or external tool calls are bundled.]

## Skill Version(s):

1.3.2 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
