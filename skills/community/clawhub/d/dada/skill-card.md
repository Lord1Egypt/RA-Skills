## Description: <br>
Dada helps developers integrate with the Dada instant delivery API for order creation, status queries, cancellation, fee estimation, callback handling, merchant onboarding, and store management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration engineers use this skill to plan and implement Dada delivery workflows, including API authentication, delivery order lifecycle handling, callbacks, and operational error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API secrets or delivery personal data could be exposed in chats, prompts, or logs during integration work. <br>
Mitigation: Keep API secrets out of chats and logs, and redact or minimize customer and courier names, phone numbers, addresses, coordinates, signatures, and order identifiers. <br>
Risk: Live order creation, cancellation, or callback processing could affect real delivery operations if tested carelessly. <br>
Mitigation: Test against the QA endpoint first, confirm before live order or cancellation actions, protect callback endpoints, and validate callback signatures. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhangifonly/dada) <br>
- [Dada Production API Endpoint](https://newopen.imdada.cn) <br>
- [Dada QA API Endpoint](https://newopen.qa.imdada.cn) <br>
- [Dada Add Order Endpoint](https://newopen.imdada.cn/api/order/addOrder) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with API examples and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes request examples, signature guidance, callback handling notes, and status tables.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
