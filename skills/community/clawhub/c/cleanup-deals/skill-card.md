## Description: <br>
Standardize deal pipelines, remove test deals, and address deals with missing amounts or close dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and revenue operations teams use this skill to audit HubSpot deals, clean test or stale records, fill missing amount and close-date gaps, and coordinate Salesforce-synced changes before relying on pipeline reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead users to delete, close, archive, or modify real HubSpot CRM records, including records that may sync to Salesforce. <br>
Mitigation: Use a dedicated least-privilege HubSpot token, export exact deal and pipeline IDs for dry-run review, get written approval from deal owners or admins, and coordinate with Salesforce admins for synced records. <br>
Risk: Stage and property changes can affect forecasts and may not have a bulk undo path. <br>
Mitigation: Run before-and-after audits, keep exports of changed records, scope changes to approved deals only, and use recycle-bin or manual rollback steps where available. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tomgranot/cleanup-deals) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown instructions with Python HubSpot API snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes audit, cleanup, verification, rollback, and Salesforce coordination guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
