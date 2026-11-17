## Description:

Assess enterprise AI and automation opportunities from company materials, prioritize up to three testable pilots, and generate evidence-bounded Markdown, HTML, and PDF management reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixisys](https://clawhub.ai/user/xixisys)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and consultants use this skill to analyze enterprise materials, identify AI and automation opportunities, and prioritize up to three bounded pilots for management review. It emphasizes evidence boundaries, human review, and deployment decisions for sensitive company data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports always include fixed third-party consultation links and contact details.

Mitigation: Review reports before sharing and install only if those links are appropriate for the deployment context.

Risk: The skill processes company materials that may include confidential or sensitive business data.

Mitigation: Use a tightly scoped, authorized input set and avoid confidential data unless the user has approval and an appropriate deployment boundary.

Risk: PDF rendering uses a local browser path and report-generation script.

Mitigation: Run report rendering in a controlled environment with a trusted Chrome, Chromium, or Edge installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixisys/skills/enterprise-ai-opportunity-advisor)
- [Deployment guidance](artifact/references/deployment-guidance.md)
- [Intake questionnaire](artifact/references/intake-questionnaire.md)
- [Report template](artifact/references/report-template.md)
- [Scoring rubric](artifact/references/scoring-rubric.md)
- [Task taxonomy](artifact/references/task-taxonomy.md)
- [Diagnosis output schema](artifact/schemas/diagnosis-output.schema.json)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured diagnosis JSON plus Markdown, self-contained HTML, and PDF report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits recommendations to up to three pilots; PDF generation requires Chrome, Chromium, or Edge and must produce a valid non-empty PDF.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
