## Description: <br>
Analyzes e-commerce main images, detail-page screenshots, search-result screenshots, or product links to score click-through and conversion potential and generate a structured HTML diagnosis report with findings and prioritized improvement actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators, marketers, designers, and listing optimization teams use this skill to evaluate product visuals and detail pages for marketplace readiness, conversion blockers, compliance concerns, and concrete next-step improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product-link diagnosis can involve fetching external product pages, which may expose submitted URLs or page content to the agent workflow. <br>
Mitigation: Use public product URLs only; avoid private, internal, or sensitive links. <br>
Risk: Generated scores and recommendations may be incorrect or depend on marketplace context not visible in the supplied images. <br>
Mitigation: Review the generated diagnosis and priority actions before changing listings or treating compliance observations as final. <br>


## Reference(s): <br>
- [完整诊断框架和评分标准](references/diagnosis_framework.md) <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/ecommerce-image-diagnosis) <br>
- [Publisher profile](https://clawhub.ai/user/bettermen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured diagnosis data, generated HTML report, and concise text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a local HTML report file and prioritized P0/P1/P2 recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
