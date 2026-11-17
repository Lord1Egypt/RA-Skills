## Description:

检索 PubMed 文献、临床指南与试验注册信息，提取证据摘要并生成 Research Grounding 建议（推荐终点定义、时间窗、混杂因素）。当用户需要做文献检索或证据 grounding 时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergenceronearth](https://clawhub.ai/user/emergenceronearth)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, clinicians, and developers use this skill to inspect a prepared evidence dataset covering PubMed literature, clinical guidelines, and trial registrations. It summarizes sources and evidence details, then suggests research grounding items such as endpoints, time windows, candidate confounders, and cautions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends run-status messages to a localhost reporting service on port 5001.

Mitigation: Install and run it only where that local reporting service is expected.

Risk: The skill relies on a fixed mock evidence file rather than live PubMed retrieval.

Mitigation: Confirm that the prepared evidence dataset is current and suitable before using its grounding recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emergenceronearth/skills/agentic-evidence-retriever)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evidence source counts, evidence summaries, research grounding recommendations, and local status-reporting commands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
