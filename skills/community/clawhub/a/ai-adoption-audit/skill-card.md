## Description:

Generates a company AI adoption maturity report from a company name and optional context, covering sponsorship, deployment model, model choices, use cases, rollout scope, ROI, risks, lessons learned, and source reliability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenwang-dev](https://clawhub.ai/user/kenwang-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, analysts, and customer-facing teams use this skill to research how a company is adopting AI and to produce either a market-research view or a customer-reference view. It can also compare multiple companies across AI maturity dimensions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save company AI-audit reports locally and reuse recent reports for follow-up requests.

Mitigation: Do not include confidential customer notes or sensitive internal company context unless local report archiving and reuse are acceptable.

Risk: Reports depend on public information and may miss private deployments, non-indexed sources, or undisclosed ROI details.

Mitigation: Treat outputs as research aids, keep source reliability labels, and verify important claims against primary sources before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenwang-dev/skills/ai-adoption-audit)
- [Publisher profile](https://clawhub.ai/user/kenwang-dev)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with summary card, structured sections, tables, source notes, optional change summary, and optional comparison table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save local report archives and reuse recent reports for follow-up requests.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
