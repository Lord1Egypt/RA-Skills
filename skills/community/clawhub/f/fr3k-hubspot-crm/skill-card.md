## Description: <br>
Full HubSpot CRM automation -- contacts, deals, companies, activities, and pipeline reports via the HubSpot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fr3kstyle](https://clawhub.ai/user/fr3kstyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, sales operations teams, and agents use this skill to manage HubSpot CRM contacts, deals, companies, activities, associations, and pipeline reporting from command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete live HubSpot CRM records when used with a powerful private app token. <br>
Mitigation: Use a dedicated least-privilege HubSpot private app token, test on sandbox or test records first, and require human confirmation before update, association, activity logging, stage-move, or delete commands. <br>
Risk: Unused or overly broad HubSpot scopes can expose more CRM and email data than the workflow needs. <br>
Mitigation: Grant only the HubSpot scopes required for the intended commands and avoid unused email-related scopes unless they are necessary. <br>


## Reference(s): <br>
- [Hubspot Crm on ClawHub](https://clawhub.ai/fr3kstyle/fr3k-hubspot-crm) <br>
- [HubSpot API endpoint](https://api.hubapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell-command guidance for setup and use, with JSON responses from HubSpot CRM operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a HubSpot Private App bearer token in HUBSPOT_API_KEY and can operate on live CRM contacts, deals, companies, activities, and associations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
