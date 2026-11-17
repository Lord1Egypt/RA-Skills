## Description:

Technology-sector competitive landscape analysis with player tiering, route differentiation, and white-space identification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce evidence-driven competitive landscape reports for defined technology sectors, including player discovery, tiering, route differentiation, top-player profiles, and white-space opportunities for strategic planning, market entry, investment screening, and R&D direction setting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lower-confidence retrieval lanes can reduce player completeness and route-breadth confidence.

Mitigation: Record the tool tier and downgrade reason in method_decisions.md, lower confidence on completeness claims, and present candidate tiers plus evidence gaps when coverage is insufficient.

Risk: Competitive tiers, route matrices, or white-space claims can mislead readers if they are not traceable to evidence.

Mitigation: Use source_index.csv and claim_ledger.csv to connect major rankings and conclusions to patent, paper, product, official, or web source identifiers before finalizing report.md.

Risk: Generated local reports and evidence files may include weak or noisy sources.

Mitigation: Review report.md and the evidence logs for source quality before relying on strategic planning, market entry, investment, or R&D recommendations.

## Reference(s):

- [Workflow](references/workflow.md)
- [Source Routing](references/source-routing.md)
- [Quality Gates](references/quality-gates.md)
- [Evidence Schema](references/evidence-schema.md)
- [Method Benchmark](references/method-benchmark.md)
- [Domain Playbooks](references/domain-playbooks.md)
- [Deliverables](references/deliverables.md)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/competitive-landscape)
- [Publisher profile](https://clawhub.ai/user/yuanzhian-patsnap)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Structured Markdown report with CSV evidence logs and optional docx/pdf exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local run-folder files such as request.md, workplan.md, method_decisions.md, query_log.csv, source_index.csv, claim_ledger.csv, and report.md.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
