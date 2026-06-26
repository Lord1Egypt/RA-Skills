## Description: <br>
CRMy agent — manages contacts, accounts, deals, and pipeline using the CRMy CRM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codycharris](https://clawhub.ai/user/codycharris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and customer-facing teams use this skill to search, create, update, and summarize CRM contacts, accounts, opportunities, activities, and pipeline status in CRMy. It guides agents to search before creating records, log meaningful interactions, link related CRM objects, and suggest next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent CRM changes, including creating contacts, linking accounts, logging activities, changing deal stages, and performing scoped updates. <br>
Mitigation: Preview and confirm write actions, especially bulk updates, before allowing the assistant to submit them. <br>
Risk: The skill sends CRM data and authenticated requests to the configured CRMy server URL. <br>
Mitigation: Use a trusted CRMy server URL and protect the CRMY API key in configuration, environment variables, and local files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or concise text summaries backed by CRMy REST API tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify persistent CRM records when the configured CRMy server accepts authenticated write requests.] <br>

## Skill Version(s): <br>
0.5.11 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
