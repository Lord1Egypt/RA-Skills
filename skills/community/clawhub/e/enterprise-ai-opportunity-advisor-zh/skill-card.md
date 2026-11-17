## Description:

Analyzes Chinese enterprise materials to identify practical AI and automation opportunities, prioritize up to three verifiable pilots, and generate management-ready diagnosis reports in Markdown, HTML, and PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixisys](https://clawhub.ai/user/xixisys)

### License/Terms of Use:

MIT-0

## Use Case:

Business consultants, enterprise leaders, and implementation teams use this skill to turn company descriptions, process documents, job materials, system lists, and user confirmations into a bounded Chinese AI adoption diagnosis. It helps compare process improvement, traditional automation, BI, OCR, knowledge bases, copilots, agents, vision AI, and speech AI before recommending small pilots with human review.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Generated reports always include fixed xixisys.com consultation and inquiry links.

Mitigation: Review report outputs before sharing them with clients or internal stakeholders, and install the skill only when the third-party contact flow is acceptable.

Risk: PDF generation uses a local browser path that is less contained than pure text or HTML rendering.

Mitigation: Run PDF rendering in a controlled environment with a trusted Chromium-compatible browser path.

Risk: Enterprise materials may include confidential business, customer, production, or personal data.

Mitigation: Avoid submitting confidential materials unless the publisher's data handling and consultation workflow are acceptable; keep human review for high-risk decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixisys/skills/enterprise-ai-opportunity-advisor-zh)
- [Publisher profile](https://clawhub.ai/user/xixisys)
- [Deployment guidance](artifact/references/deployment-guidance.md)
- [Intake questionnaire](artifact/references/intake-questionnaire.md)
- [Report template guidance](artifact/references/report-template.md)
- [Scoring rubric](artifact/references/scoring-rubric.md)
- [Task taxonomy](artifact/references/task-taxonomy.md)
- [Diagnosis output schema](artifact/schemas/diagnosis-output.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown reports, standalone HTML, PDF, and structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces diagnosis.json and report files; PDF rendering depends on an available trusted Chromium-compatible browser.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
