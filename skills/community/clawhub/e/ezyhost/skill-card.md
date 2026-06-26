## Description: <br>
Deploy, manage, and monitor static websites via the EzyHost API, including file uploads, AI site generation, analytics, domains, QR codes, email capture, and team collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AraratDev](https://clawhub.ai/user/AraratDev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and site operators use this skill to deploy, update, and administer static websites on EzyHost. It supports project creation, file upload, SEO analysis, analytics review, domain management, version rollback, QR codes, email capture, team management, and AI-generated site files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform powerful EzyHost account actions, including deleting projects or files, rolling back versions, changing teams, domains, or API keys, and exporting captured emails. <br>
Mitigation: Use a dedicated revocable API key, verify target project IDs before changes, and require explicit user confirmation for destructive, account, domain, team, rollback, key, or email export actions. <br>
Risk: Authenticated API access can modify public hosted site content and settings. <br>
Mitigation: Preview request payloads and affected resources before uploads, AI deployments, SEO auto-fixes, domain changes, or visibility changes. <br>


## Reference(s): <br>
- [EzyHost homepage](https://ezyhost.io) <br>
- [EzyHost API base URL](https://ezyhost.io/api) <br>
- [EzyHost API keys dashboard](https://ezyhost.io/dashboard/api-keys) <br>
- [ClawHub EzyHost skill page](https://clawhub.ai/AraratDev/ezyhost) <br>
- [Publisher profile](https://clawhub.ai/user/AraratDev) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration, Code] <br>
**Output Format:** [Markdown guidance with HTTP endpoints, JSON request and response examples, and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EZYHOST_API_KEY and network access to ezyhost.io; some actions require paid EzyHost plans.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
