## Description: <br>
Prepare Dataify builder requests for the crunchbase.com scraper family rooted at crunchbase_company_by-url. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to choose a supported Dataify Crunchbase scraper, collect the required parameters, and produce a builder request for Dataify's scraper API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated curl commands may include the actual Dataify bearer token when DATAIFY_API_TOKEN is set. <br>
Mitigation: Use a session-scoped token or credential manager where practical, and avoid sharing generated curl commands. <br>
Risk: Shell profile setup can persist DATAIFY_API_TOKEN in files that may later be committed or shared. <br>
Mitigation: Do not commit shell profiles or other configuration files that contain DATAIFY_API_TOKEN. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-crunchbase-company-by-url) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash or PowerShell commands and JSON-form request parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a Dataify bearer token in generated curl commands when the token is present in the environment.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
