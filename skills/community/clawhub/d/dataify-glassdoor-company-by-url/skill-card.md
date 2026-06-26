## Description: <br>
Prepare Dataify builder requests for the glassdoor.com scraper family rooted at glassdoor_company_by-url, including tool selection, saved parameter options, and scraperapi.dataify.com/builder curl generation with DATAIFY_API_TOKEN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to prepare authenticated Dataify builder requests for supported Glassdoor company and job-listing scraper tools. It helps collect user parameter values, normalize selectable options, and return a ready-to-run curl request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated curl output can expose a real DATAIFY_API_TOKEN if the token value is embedded in the Authorization header. <br>
Mitigation: Use commands that reference $DATAIFY_API_TOKEN where possible, run them only in a private terminal, and redact bearer tokens before sharing logs or generated commands. <br>
Risk: The published package appears incomplete because referenced catalog or helper files are missing. <br>
Mitigation: Confirm required referenced files are present before installation or execution, especially the tool parameter catalog used to build spider_parameters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/dataify-glassdoor-company-by-url) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify Builder API Endpoint](https://scraperapi.dataify.com/builder) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Dataify builder curl requests and may normalize spider_parameters JSON from user-supplied values.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
