## Description: <br>
Bailian Usage Proxy helps teams share an Alibaba Bailian account by proxying OpenAI-compatible API calls, tracking per-user token usage, enforcing quotas, and exposing usage reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bjmfjoy](https://clawhub.ai/user/bjmfjoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to deploy and operate a proxy for shared Alibaba Bailian accounts so they can attribute usage by user, model, and time period, manage quotas, and export usage reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Admin and reporting functions can expose user management and usage data without clear access control. <br>
Mitigation: Add admin authentication and authorization, restrict network access, and keep admin routes off public networks until those controls are in place. <br>
Risk: The upstream Bailian API key and generated user keys can enable unauthorized model usage or account spend if exposed. <br>
Mitigation: Store upstream credentials in a protected secret store or locked-down environment variables, rotate keys printed or shared during setup, and revoke unused internal keys. <br>
Risk: The proxy records usage metadata and may process model traffic for multiple users. <br>
Mitigation: Define allowed retention and logging scope before deployment, minimize stored request details, and limit access to usage logs and exports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bjmfjoy/bailian-usage-proxy) <br>
- [API Reference](references/api.md) <br>
- [Architecture Reference](references/architecture.md) <br>
- [Database Reference](references/database.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local service setup steps, proxy configuration, user-management commands, and usage-report guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and app package __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
