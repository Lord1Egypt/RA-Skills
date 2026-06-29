## Description: <br>
Use the folkctl CLI to inspect and update folk.app CRM data without third-party connectors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j-edel](https://clawhub.ai/user/j-edel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CRM operators use this skill to inspect and update folk.app CRM records through the folkctl CLI and first-party folk API. It supports work with people, companies, groups, deals, users, notes, reminders, interactions, and webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured folk API key can read and change CRM records, notes, reminders, interactions, and webhooks. <br>
Mitigation: Confirm the folkctl package source before installation, keep the API key out of chat and logs, and use least-privilege credentials where available. <br>
Risk: Create, update, or delete commands can change CRM data. <br>
Mitigation: Use dry-run previews for changes, summarize the affected resource and request before execution, and require explicit confirmation for deletes. <br>


## Reference(s): <br>
- [folkctl GitHub project](https://github.com/j-edel/folkctl) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FOLK_API_KEY; recommends dry-run previews and explicit confirmation before destructive changes.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
