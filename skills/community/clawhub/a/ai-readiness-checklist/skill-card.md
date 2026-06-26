## Description: <br>
Conducts a 15-question AI readiness assessment, scores enterprise adoption maturity across five dimensions, and produces a prioritized action plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[filipbl4gojevic](https://clawhub.ai/user/filipbl4gojevic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Enterprise leaders, AI program owners, and governance teams use this skill to assess organizational readiness for AI adoption, identify readiness gaps, and prioritize practical next steps before scaling AI deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The assessment may collect sensitive details about internal data, security, governance, compliance, and AI deployment maturity. <br>
Mitigation: Avoid entering secrets, customer records, regulated data, or confidential implementation details unless the agent environment is approved for that information. <br>
Risk: The report is strategic guidance based on self-reported answers and can be incomplete or misleading if answers are inaccurate or partial. <br>
Mitigation: Review recommendations with responsible business, legal, security, and technical owners before using them for deployment decisions. <br>


## Reference(s): <br>
- [AI Readiness Checklist release page](https://clawhub.ai/filipbl4gojevic/ai-readiness-checklist) <br>
- [Common AI Readiness Patterns](references/readiness-patterns.md) <br>
- [Assessment report template](templates/assessment-report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown assessment report with score tables, blocker analysis, pattern flags, and a prioritized action plan.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses 15 multiple-choice readiness answers; can also produce partial or dimension-specific assessments when fewer answers are provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
