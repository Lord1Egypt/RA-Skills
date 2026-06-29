## Description: <br>
古董鉴定估价全流程助手，覆盖藏品信息采集、初步评估报价、支付订单生成和鉴定报告输出，并支持微信小程序和 Web 终端自适应呈现。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Collectors, sellers, and appraisal-service operators use this skill to collect item photos and provenance, produce an AI-assisted preliminary appraisal, guide service selection and payment, and output a Chinese-language appraisal report. The report is reference guidance and should not replace qualified in-person appraisal for high-value, legal, insurance, or transaction decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded photos and provenance can expose sensitive ownership, identity, or location details. <br>
Mitigation: Avoid sharing personal identifiers, exact addresses, or legally sensitive ownership details when requesting an appraisal. <br>
Risk: The payment-style workflow can be misunderstood as a live paid service in environments where it is only simulated. <br>
Mitigation: Confirm whether the payment flow is demo or live, and review pricing and payment terms before proceeding. <br>
Risk: AI-assisted estimates may be inaccurate for high-value, legal, insurance, or transaction decisions. <br>
Mitigation: Treat generated reports as reference material and rely on a qualified in-person appraisal for consequential decisions. <br>
Risk: Some antiques or cultural-property items may be subject to legal restrictions on sale, transfer, or appraisal. <br>
Mitigation: Follow applicable cultural heritage and trading laws before relying on the report for sale or transfer. <br>


## Reference(s): <br>
- [Antique Knowledge Base](references/antique-knowledge.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Chinese-language conversational guidance, compact cards, and HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Adapts report presentation for WeChat mini-program and Web/WorkBuddy environments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
