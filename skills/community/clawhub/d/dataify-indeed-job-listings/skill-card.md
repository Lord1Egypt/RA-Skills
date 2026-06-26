## Description: <br>
Collect Indeed job listings through Dataify Scraper API from one or more Indeed job URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and recruiting teams use this skill to create Dataify collection tasks for Indeed job listings by URL. It helps users review required parameters, confirm defaults, submit Dataify builder requests, and report task identifiers and status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dataify API tokens are sensitive and may be exposed if passed or displayed carelessly. <br>
Mitigation: Use DATAIFY_API_TOKEN through a secure local environment or secret mechanism when possible, avoid echoing tokens, and only save a provided token after explicit user consent. <br>
Risk: The skill can submit Indeed job URLs to Dataify and create external collection tasks. <br>
Mitigation: Show the required Markdown confirmation table, review exact parameters with the user, and call the API only after explicit confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-indeed-job-listings) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill) <br>
- [Dataify builder endpoint](https://scraperapi.dataify.com/builder?platform=1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, confirmation tables, shell commands, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts users to confirm parameters before API calls and reports task ID or status fields when available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
