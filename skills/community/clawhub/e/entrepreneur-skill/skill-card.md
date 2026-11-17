## Description:

An AI founder partner for building and scaling startups that diagnoses stage, designs hypothesis experiments, supports pricing and growth-loop decisions, and produces weekly execution reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neiljo-gy](https://clawhub.ai/user/neiljo-gy)

### License/Terms of Use:

MIT-0

## Use Case:

Founders, founder teams, and agents supporting startup operations use this skill to diagnose company stage and bottlenecks, design 7-day experiments, make pricing and growth-loop decisions, and generate weekly continue/stop/pivot reviews with human approval gates for irreversible decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad command, network, write, memory, and remote-agent capabilities can expose unrelated credentials or private projects if installed into an unsafe workspace.

Mitigation: Install only in a sandboxed workspace with no unrelated credentials or private projects, and require explicit approval before external connections, package execution, file writes outside a report directory, or optional dependency loading.

Risk: Business recommendations can be incorrect, misleading, or too consequential for autonomous execution.

Mitigation: Require human approval for financing, equity, legal, compliance, hiring, firing, irreversible external actions, and high-risk budget or brand decisions.

Risk: Weekly reviews can produce poor continue/stop/pivot decisions when metrics, baselines, or evidence quality are missing or inaccurate.

Mitigation: Use the documented metric contract, required-field checks, fraction validation, stable baselines, and explicit evidence notes before acting on review recommendations.

## Reference(s):

- [Stage Diagnosis](references/stage-diagnosis.md)
- [Hypothesis Lab](references/hypothesis-lab.md)
- [Pricing Decision](references/pricing-decision.md)
- [Growth Loop Design](references/growth-loop-design.md)
- [Weekly Founder Review](references/weekly-founder-review.md)
- [Agent Org Governance](references/agent-org-governance.md)
- [Metrics Baseline](references/metrics-baseline.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and reports with optional JSON inputs and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weekly review automation reads structured JSON metrics and writes Markdown reports; optional external integrations are opt-in.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
