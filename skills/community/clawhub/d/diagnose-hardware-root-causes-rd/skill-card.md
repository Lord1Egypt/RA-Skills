## Description:

Diagnose hardware performance shortfalls with measurable problem definition, first-principles models, equation-led decomposition, 5M1E coverage, multidisciplinary review and evidence-ranked causal trees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn hardware performance shortfalls into measurable problem statements, evidence-ranked causal trees, prioritized hypotheses, validation experiments, and engineering questions. It is suited for root-cause analysis of thermal, structural, acoustic, electrical, EMC, materials, manufacturing, measurement, and environmental issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic conclusions may be mistaken for certification, regulatory sign-off, or proof of causation.

Mitigation: Treat outputs as diagnostic support; have safety-critical or regulated findings reviewed by qualified engineers before decisions or release.

Risk: Large or untrusted causal-tree JSON inputs can create unreliable or resource-heavy PNG export runs.

Mitigation: Run the PNG exporter only on trusted or reasonably sized JSON inputs, avoid maximum DPI for large trees, and review generated figures before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/diagnose-hardware-root-causes-rd)
- [Publisher profile](https://clawhub.ai/user/yuanzhian-patsnap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured RCA sections, Mermaid diagrams, JSON causal-tree examples, and optional shell commands for PNG export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include causal trees, evidence tables, hypothesis rankings, experiment plans, engineering questions, and local PNG export guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
