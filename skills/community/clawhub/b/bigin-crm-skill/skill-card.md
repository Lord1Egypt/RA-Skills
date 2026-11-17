## Description:

Manage Bigin CRM pipelines, contacts, companies, tasks, activities, reports, and sales automation through OAuth2-authenticated Bigin REST API commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lindy-dev](https://clawhub.ai/user/lindy-dev)

### License/Terms of Use:

MIT

## Use Case:

Sales teams, operators, and developers use this skill to connect an agent to Bigin CRM for managing customer records, pipeline stages, follow-up work, reporting, and CRM automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores offline Bigin CRM OAuth tokens and uses local OAuth client credentials.

Mitigation: Keep client secrets and token files out of shared repositories and backups, restrict local file permissions, use a sandbox first, and revoke or rotate tokens when access is no longer needed.

Risk: The requested OAuth scopes include broad module and settings access.

Mitigation: Review scopes before production use and remove unnecessary settings access where the target workflow does not need it.

Risk: Bulk update, auto-advance, delete, and close-won or close-lost commands can make live business-data changes.

Mitigation: Preview changes in a Bigin sandbox, require human approval for destructive or bulk operations, and export or back up affected CRM records before running production changes.

Risk: The OAuth callback flow needs stronger state validation and loopback binding before production use.

Mitigation: Add state validation and bind the callback listener to loopback-only interfaces before relying on the flow with production CRM data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lindy-dev/skills/bigin-crm-skill)
- [Bigin API v2 overview](https://www.bigin.com/developer/docs/apis/v2/)
- [Bigin Modules API](https://www.bigin.com/developer/docs/apis/v2/modules-api.html)
- [Bigin Bulk APIs](https://www.bigin.com/developer/docs/apis/v2/bulk-read/overview.html)
- [Bigin OAuth guide](https://www.bigin.com/developer/docs/apis/v2/oauth-overview.html)
- [Zoho API Console](https://api-console.zoho.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets, JSON/YAML configuration examples, and generated CRM reports in CSV or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update CRM records through API calls and may write local credential-token or report files when the documented commands are run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
