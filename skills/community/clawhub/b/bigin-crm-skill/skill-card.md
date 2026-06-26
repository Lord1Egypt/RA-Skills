## Description: <br>
Manage pipelines, contacts, companies, tasks, and activities in Bigin CRM using an OAuth2-authenticated API for small business sales automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lindy-dev](https://clawhub.ai/user/lindy-dev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and sales operations teams use this skill to let agents authenticate with Bigin CRM and manage pipeline records, contacts, companies, tasks, events, calls, automation, and reports through CLI and programmatic workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadly read, change, delete, and automate Bigin CRM records. <br>
Mitigation: Start in a sandbox or least-privilege OAuth app, and require dry-run, approval, and recovery procedures before production bulk updates, delete commands, or automation workflows. <br>
Risk: Reports and API responses may contain sensitive CRM data. <br>
Mitigation: Review generated reports and JSON output before sharing them outside the intended sales or operations audience. <br>
Risk: Debug output or stored credentials could expose access details. <br>
Mitigation: Avoid enabling DEBUG and protect the local OAuth credential file used by the skill. <br>


## Reference(s): <br>
- [Bigin API v2 Overview](https://www.bigin.com/developer/docs/apis/v2/) <br>
- [Bigin Modules API](https://www.bigin.com/developer/docs/apis/v2/modules-api.html) <br>
- [Bigin Bulk APIs](https://www.bigin.com/developer/docs/apis/v2/bulk-read/overview.html) <br>
- [Bigin OAuth Guide](https://www.bigin.com/developer/docs/apis/v2/oauth-overview.html) <br>
- [Zoho API Console](https://api-console.zoho.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, Python, JSON, and CSV examples; runtime scripts return JSON and optional CSV reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May authenticate to Zoho/Bigin APIs and create, update, delete, bulk import, automate, or report on CRM records.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
