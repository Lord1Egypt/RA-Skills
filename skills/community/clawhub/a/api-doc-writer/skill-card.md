## Description: <br>
API接口文档助手。用于编写REST API文档、定义接口规范、生成接口说明。当需要编写API文档、接口规范时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongjie666888](https://clawhub.ai/user/yongjie666888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to draft REST API documentation, including endpoint summaries, request and response examples, status codes, change records, and RESTful design guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated API documentation may include placeholder values, inaccurate endpoint behavior, or misleading examples if not checked against the real implementation. <br>
Mitigation: Review generated documentation against the implemented API contract, tests, and production behavior before publishing or sharing externally. <br>
Risk: The skill may guide agents through local CLI, GitHub, Convex, auth, or moderation workflows when asked, which can affect accounts, roles, deployments, or production data. <br>
Mitigation: Install only when the publisher is trusted and review commands before approving actions that change accounts, roles, deployments, or production data. <br>
Risk: API examples may expose sensitive authentication, personal data, or weak security patterns if copied directly from real systems. <br>
Mitigation: Use sanitized sample data and confirm that authentication, token expiry, rate limits, and input validation guidance match the target system's security requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yongjie666888/api-doc-writer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown API documentation templates and concise implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include REST endpoint examples, JSON request and response examples, status-code tables, and security recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
