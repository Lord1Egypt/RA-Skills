## Description: <br>
泛微 e-office 协同办公系统 OpenAPI - 用户管理、部门管理、审批流程、考勤等企业级 API <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quanruxiaohong](https://clawhub.ai/user/quanruxiaohong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and administrators use this skill to let an agent query and operate an e-office OA deployment, including users, departments, workflow approvals, attendance, notifications, customers, contracts, attachments, and custom modeling data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to enterprise OA accounts, approvals, files, and business data. <br>
Mitigation: Install only for deliberate OA automation use, configure a dedicated least-privilege OA application, restrict the OA whitelist, and avoid administrator credentials unless they are required. <br>
Risk: Create, edit, delete, approval, upload, and bulk actions may change production OA records. <br>
Mitigation: Require human confirmation and audit logging for sensitive or destructive actions before execution. <br>
Risk: Misconfigured base URLs or exposed secrets could route requests to the wrong system or disclose OA credentials. <br>
Mitigation: Protect secret configuration, verify the configured OA base URL, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quanruxiaohong/eoffice-api) <br>
- [Project homepage](https://github.com/yourname/eoffice-skill) <br>
- [e-office OpenAPI complete interface documentation](references/api.md) <br>
- [OA open platform application management documentation](https://service.e-office.cn/knowledge/detail/49/ke7d0a3) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance for authenticated e-office API operations; actual API effects depend on configured OA credentials and permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
