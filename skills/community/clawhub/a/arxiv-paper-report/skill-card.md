## Description:

Search arXiv and, when needed, verify external academic sources to update field beliefs and one primary decision through testable propositions, capability frontiers, explicitly labeled mechanism models, technical options, transition theses, five-dimensional maturity, leading indicators, and a restrained bilingual standalone HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yofine](https://clawhub.ai/user/yofine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, strategists, and due-diligence analysts use this skill to turn an arXiv-centered corpus into evidence-bounded field beliefs and one actionable research, architecture, product, or investment decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research synthesis can overstate what arXiv submissions prove, especially when evidence is limited to abstracts, recent papers, or shared author narratives.

Mitigation: Apply the skill's evidence ceilings, proposition status rules, source locators, and external verification requirements; state insufficient evidence instead of filling gaps with plausible synthesis.

Risk: The workflow searches arXiv or academic sources and saves raw, normalized, JSON, and HTML artifacts in the local workspace.

Mitigation: Run it only where local research artifacts are acceptable, preserve raw responses for auditability, and review each paper's license before reuse or redistribution.

Risk: The workflow depends on the separate literature-search-arxiv skill and uv; missing prerequisites can make a report incomplete.

Mitigation: Check dependencies before starting and stop rather than replacing the prescribed helper when prerequisites are unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yofine/skills/arxiv-paper-report)
- [README](README.md)
- [Analysis rubric](references/analysis-rubric.md)
- [Report schema](references/report.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Validated JSON research record plus deterministic standalone HTML report; agent-facing responses may include Markdown, command snippets, and arXiv source URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves raw and normalized search artifacts locally, uses Simplified Chinese report prose with original English paper titles, and requires sequential arXiv requests.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
