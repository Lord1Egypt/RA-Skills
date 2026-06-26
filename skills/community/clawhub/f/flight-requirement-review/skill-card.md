## Description: <br>
机票产品需求评审 Agent，对前端、后端、运营类机票需求文档进行结构化评审打分，并支持独立的流程图治理评审。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arisefx](https://clawhub.ai/user/arisefx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, engineers, QA reviewers, and operations teams use this skill to review flight product requirement documents, prototypes, and process models. It classifies frontend, backend, and operations requirements, scores them against documented dimensions, and returns concrete issues and improvement suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill produces evaluative review guidance that may be incorrect or incomplete if the submitted requirement document lacks context. <br>
Mitigation: Use the generated scores and recommendations as review input, and have product, engineering, QA, and compliance owners confirm conclusions before acting on them. <br>
Risk: Requirement documents can include sensitive passenger, payment, itinerary, or business data. <br>
Mitigation: Review inputs for confidential data and avoid sharing production credentials or unnecessary personal data with the reviewing agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arisefx/flight-requirement-review) <br>
- [review-standards.md](artifact/review-standards.md) <br>
- [tech-doc-template.md](artifact/tech-doc-template.md) <br>
- [example-review.md](artifact/example-review.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, configuration] <br>
**Output Format:** [Structured Markdown review reports with scoring tables, findings, recommendations, and optional technical-document templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts Markdown, image, and HTML requirement evidence when available to the agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
