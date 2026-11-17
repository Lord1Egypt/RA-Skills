## Description:

Evaluates a single drug across R&D, clinical, regulatory, competitive, deal, and preliminary patent evidence for asset decisions, pipeline reviews, and BD due diligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and internal life-science, R&D, BD, portfolio, commercial, or investment-screening teams use this skill to normalize a drug entity and assemble decision-ready evidence across lifecycle milestones, indications, clinical data, competitors, deals, and preliminary IP signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deep HTML reports are instructed to load mutable third-party ECharts JavaScript from a CDN, which could expose sensitive pipeline, BD, investment, or patent content when opened.

Mitigation: Review generated reports before sharing and prefer a release that vendors ECharts locally or pins an exact CDN version with Subresource Integrity.

Risk: Drug lifecycle reports may be mistaken for medical, investment, legal, or freedom-to-operate advice.

Mitigation: Preserve the skill's disclaimers, keep patent conclusions labeled as preliminary IP signals, and route claim-level patent risk or FTO questions to qualified counsel or a dedicated FTO workflow.

## Reference(s):

- [Legacy deep single-drug report specification](references/legacy-report-spec.md)
- [ClawHub release page](https://clawhub.ai/yuanzhian-patsnap/skills/drug-lifecycle-evaluation)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [HTML report with evidence tables, chart code, source register, disclaimers, and decision-support summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports screen, standard, and deep report depths; deep reports use the legacy HTML report specification.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
