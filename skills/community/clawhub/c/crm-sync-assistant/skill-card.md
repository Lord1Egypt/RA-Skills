## Description:

CRM Sync Assistant helps employees turn visit-analysis records into structured CRM lead records, review them for confirmation, sync them to CRM, and inspect synced or unsynced projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and sales managers use this skill to authenticate to a CRM service, query visit-analysis and lead records, review generated lead summaries, sync confirmed records, and inspect project data within documented subordinate-access permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles employee passwords, bearer tokens, and CRM records.

Mitigation: Install only for trusted CRM operators, replace chat-based password collection with a secure login flow, and store tokens in a credential store or locked-down file.

Risk: The artifact describes HTTP service endpoints and a fallback that can place a full token in a URL.

Mitigation: Require HTTPS for production use and remove token-in-URL fallback before deployment.

Risk: Broad trigger phrases and manager/subordinate data access can expose CRM records beyond the user's intent.

Mitigation: Narrow triggers and document manager/subordinate access rules clearly before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/crm-sync-assistant)
- [Publisher profile](https://clawhub.ai/user/vivalavida-say-hi)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, API calls, Guidance]

**Output Format:** [Markdown status reports and CRM record summaries, with JSON payloads and shell commands for authenticated API calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include markdown links to CRM and visit-board pages; requires curl, jq, and python3 on Linux or macOS.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
