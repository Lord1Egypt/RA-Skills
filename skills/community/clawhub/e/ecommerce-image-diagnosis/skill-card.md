## Description:

电商主图详情页诊断 helps ecommerce sellers and operators analyze product hero images, detail-page screenshots, search-result screenshots, or product links and generate a structured HTML diagnosis report with scores, findings, and prioritized improvement actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, marketers, and operators use this skill to review listing images, detail pages, and search-result presentation across platforms such as Taobao, Pinduoduo, Douyin Ecommerce, and JD. It supports CTR and CVR improvement planning by producing dimension scores, a grade, key findings, and P0/P1/P2 action lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can turn untrusted product or user text into active browser content.

Mitigation: Use only trusted product data and diagnosis text, and avoid opening or sharing generated HTML reports from untrusted inputs until report generation escapes HTML and validates URLs.

## Reference(s):

- [电商主图详情页诊断框架](references/diagnosis_framework.md)
- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/ecommerce-image-diagnosis)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, HTML files, guidance]

**Output Format:** [Structured diagnosis JSON, generated HTML report, and concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes main-image and detail-page scores, an overall grade, key findings, and P0/P1/P2 prioritized actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
