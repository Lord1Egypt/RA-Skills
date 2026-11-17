## Description:

Provides structured multi-criteria decision analysis for ranking options using weights, constraints, confidence, tradeoff reasoning, sensitivity analysis, and explainable recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimgouso](https://clawhub.ai/user/dimgouso)

### License/Terms of Use:


## Use Case:

Developers, operators, and business users use this skill to turn structured or freeform tradeoff problems into auditable ranked recommendations for decisions such as vendor selection, procurement, route planning, hiring shortlists, tool comparison, and prioritization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rank high-impact decisions, including hiring shortlists, where under-scoped criteria may create compliance or fairness risk.

Mitigation: Require lawful, job-related criteria, explicit user approval, and compliance review before relying on rankings in regulated or high-impact decisions.

Risk: CLI fallback may write temporary local files containing confidential candidate or business data on shared machines.

Mitigation: Avoid confidential data on shared systems unless local temporary-file handling is acceptable, or use a controlled environment.

Risk: Incomplete or ambiguous inputs can produce misleading recommendations.

Mitigation: Validate requests first, clarify missing criteria, directions, constraints, and values, and present confidence and sensitivity caveats.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dimgouso/skills/adi-decision-engine)
- [Request Schema](references/request_schema.md)
- [Result Interpretation](references/result_interpretation.md)
- [Policy Guide](references/policy_guide.md)
- [Use Cases](references/use_cases.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown decision-support responses with optional JSON output from local helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local python3 and either the adi-decision package or adi CLI; no API keys or network access are required for the core workflow.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
