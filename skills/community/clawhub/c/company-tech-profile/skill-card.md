## Description:

Single-company technology profile and R&D assessment for a defined technology topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Technical leaders, analysts, and investment screeners use this skill to produce evidence-driven company technology profiles for due diligence, partnership screening, investment screening, and R&D direction assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs external research and creates local report and evidence files.

Mitigation: Run it in an appropriate workspace and review generated request, workplan, source index, claim ledger, and report files before relying on the output.

Risk: A company-only prompt may cause the skill to infer the technology topic.

Mitigation: Provide an explicit company, technology topic, purpose, and time window, or review the inferred scope before using the report.

Risk: Downgraded retrieval paths can reduce coverage for patent, paper, and public-signal evidence.

Mitigation: Check method_decisions.md for the retrieval tier used and treat conclusions from lower-confidence source paths with appropriate caution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/company-tech-profile)
- [Workflow](references/workflow.md)
- [Source Routing](references/source-routing.md)
- [Quality Gates](references/quality-gates.md)
- [Evidence Schema](references/evidence-schema.md)
- [Deliverables](references/deliverables.md)
- [Method Benchmark](references/method-benchmark.md)
- [Domain Playbooks](references/domain-playbooks.md)

## Skill Output:

**Output Type(s):** [markdown, text, configuration, guidance]

**Output Format:** [Structured Markdown report with CSV evidence files and optional document exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces request, workplan, method decision, query log, source index, claim ledger, and report files in a writable run folder.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
