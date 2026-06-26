## Description: <br>
Aiding Shifu helps users find installation technicians, log in to the Aiding Shifu platform, dispatch orders, and manage home decoration installation work orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinhuihua](https://clawhub.ai/user/yinhuihua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and service operators use this skill to search for home decoration installation technicians, authenticate to Aiding Shifu, dispatch work orders, and check work-order status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release handles Aiding Shifu account tokens and includes evidence of bundled credentials. <br>
Mitigation: Review credentials before installation, rotate any exposed tokens, and prefer a revised release that removes bundled credentials and avoids printing, copying, or displaying raw tokens. <br>
Risk: Login pages store tokens in browser localStorage and send login messages with a wildcard postMessage target. <br>
Mitigation: Use a version that stores secrets outside localStorage and restricts postMessage to trusted origins, or disable the browser login helpers until they are revised. <br>
Risk: Work-order flows may send customer names, phone numbers, and addresses to the Aiding Shifu service. <br>
Mitigation: Ask for clear user confirmation before transmitting customer data and minimize personal data included in requests. <br>
Risk: QR code generation can use a third-party QR service for login URLs. <br>
Mitigation: Generate QR codes locally or through a first-party service before using QR-based login in production. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yinhuihua/aiding-shifu) <br>
- [Publisher profile](https://clawhub.ai/user/yinhuihua) <br>
- [Aiding Shifu homepage](https://asf.dderp.cn) <br>
- [Aiding Shifu API documentation](https://mes.dderp.cn/mob/swagger-ui/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with API details and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May handle account tokens and customer work-order data when used for login, technician search, or dispatch workflows.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
