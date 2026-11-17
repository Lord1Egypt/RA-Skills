## Description:

古董鉴定估价全流程助手。覆盖藏品信息采集→初步评估报价→支付订单生成→鉴定报告输出4大阶段。支持微信小程序和非微信终端双环境，智能识别用户设备环境自适应输出格式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and collecting workflows use this Chinese-language skill to collect antique details, produce AI-assisted appraisal and price-range guidance, guide service selection, and generate a final appraisal report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow includes payment-style steps that could be confused with a real merchant checkout.

Mitigation: Review the release before installation and verify any real merchant identity, payment destination, or payment confirmation flow before users pay.

Risk: Generated HTML reports can include user-supplied appraisal text and item details.

Mitigation: Escape or sanitize user-provided content and render reports in a sandboxed viewer before opening or sharing generated HTML.

Risk: AI-assisted antique estimates may be inaccurate or unsuitable for legal, insurance, investment, or transaction decisions.

Mitigation: Present appraisals as reference only, preserve uncertainty, and direct high-value or regulated items to qualified appraisal and legal review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/antique-appraisal)
- [Publisher profile](https://clawhub.ai/user/bettermen)
- [古董鉴定知识库](references/antique-knowledge.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Chinese-language conversational guidance, structured markdown-style cards, and generated HTML appraisal reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapts report presentation for WeChat mini-program style cards or full Web/WorkBuddy HTML output.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
