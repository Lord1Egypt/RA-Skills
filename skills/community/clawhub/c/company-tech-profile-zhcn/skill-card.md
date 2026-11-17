## Description:

A Chinese-language workflow for producing an evidence-based technology profile and R&D assessment of one company for a specified technology topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Technology leaders, analysts, and investment screening teams use this skill to evaluate a single company's technical position, R&D direction, and evidence-supported strengths and limitations for a specified technology topic. It is intended for company technology analysis, technology due diligence briefs, partner assessment, and single-company investment screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may use external search or research tools for company and technology topics that could be sensitive.

Mitigation: Confirm that external research is acceptable for the target company, topic, and decision context before running the skill.

Risk: The skill can write local evidence and report files in the working directory.

Mitigation: Run it in an appropriate writable project directory and review generated files before sharing or committing them.

Risk: Weak or degraded evidence paths can lead to overconfident company technology conclusions.

Mitigation: Use the built-in source index, claim ledger, method decisions, and quality gates to distinguish verified facts, evidence-supported inferences, and open gaps.

Risk: The workflow is not intended for legal patent opinions, FTO, infringement, or litigation analysis.

Mitigation: Route legal patent questions to qualified legal review instead of presenting this skill's output as legal advice.

Risk: The default output and workflow are Chinese-language.

Mitigation: Use this release when Chinese output is desired, or request a different language workflow before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/company-tech-profile-zhcn)
- [Workflow](references/workflow.md)
- [Source Routing](references/source-routing.md)
- [Evidence Schema](references/evidence-schema.md)
- [Quality Gates](references/quality-gates.md)
- [Method Benchmark](references/method-benchmark.md)
- [Domain Playbooks](references/domain-playbooks.md)
- [Deliverables](references/deliverables.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown report with supporting CSV evidence ledgers and optional docx/pdf exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local files such as request.md, workplan.md, method_decisions.md, query_log.csv, source_index.csv, claim_ledger.csv, and report.md.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
