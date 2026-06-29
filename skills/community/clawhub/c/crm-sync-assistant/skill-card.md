## Description: <br>
Helps employees review visit-analysis records, prepare structured CRM lead follow-up entries, confirm them with the user, and sync or query CRM project data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, team leads, and managers use this skill to inspect CRM synchronization status, turn visit-analysis records into structured lead follow-up data, confirm proposed changes, and sync or review CRM projects within the user's permitted scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may be asked to enter CRM passwords in chat. <br>
Mitigation: Use only in organizations that explicitly approve this workflow, and prefer a secure authentication flow before broad deployment. <br>
Risk: Credentials and API traffic may be sent over plain HTTP. <br>
Mitigation: Require HTTPS for CRM API and H5 endpoints before handling production CRM credentials or customer data. <br>
Risk: Bearer tokens are cached locally and may be exposed in generated links. <br>
Mitigation: Protect and rotate cached tokens, prefer short-lived exchange codes, and remove bearer-token URL fallback where possible. <br>
Risk: CRM records can be created or updated after user confirmation. <br>
Mitigation: Keep explicit confirmation, scoped triggers, backend authorization checks, and review of proposed record changes before synchronization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/crm-sync-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, JSON payloads, structured CRM summaries, and generated project links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and python3 on Linux or macOS; outputs should be reviewed before CRM synchronization.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
