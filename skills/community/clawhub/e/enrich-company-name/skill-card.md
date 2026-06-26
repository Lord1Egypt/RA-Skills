## Description: <br>
Populate missing contact company name fields from associated company records using a HubSpot workflow with optional API backfill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CRM operators, marketing operations teams, and developers use this skill to populate missing HubSpot contact company-name fields from associated company records and verify enrichment coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow or optional API backfill can update HubSpot contact records incorrectly if filters, copy actions, or company associations are wrong. <br>
Mitigation: Review workflow filters and copy-property settings before activation, preserve a rollback path for affected contacts, and spot-check enriched records against associated companies. <br>
Risk: HubSpot credentials used by the audit scripts can expose or modify CRM data if over-privileged. <br>
Mitigation: Use a least-privilege HubSpot token, store it in the local environment file, and avoid sharing generated audit files outside approved CRM operations workflows. <br>
Risk: Large backfills may take hours, hit API limits, or leave recently associated contacts incomplete. <br>
Mitigation: Respect HubSpot rate limits, segment large API runs by created-date ranges, and monitor the after-state audit plus workflow history after activation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomgranot/enrich-company-name) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code] <br>
**Output Format:** [Markdown guidance with Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CRM audit CSV outputs when the bundled before and after scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
