## Description: <br>
Prepares Dataify builder requests for Airbnb scraper tools rooted at airbnb_product_by-searchurl, guiding tool selection, parameter collection, and curl generation with DATAIFY_API_TOKEN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Dataify builder curl requests for Airbnb scraping workflows, including tool choice, saved parameter options, and multi-row spider_parameters payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated curl output can expose a real Dataify API token if shared or logged. <br>
Mitigation: Prefer commands that reference $DATAIFY_API_TOKEN, review generated output before sharing, and avoid storing token-bearing curl commands in tickets, logs, or documentation. <br>
Risk: The packaged artifact appears to be missing the parameter catalog required by the documented workflow. <br>
Mitigation: Confirm that references/tool-params.json is available before relying on saved tool parameters, or provide parameter values explicitly during use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-airbnb-product-by-searchurl) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify builder endpoint](https://scraperapi.dataify.com/builder) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces curl requests and setup guidance; generated commands can contain sensitive Dataify token material if the helper expands the environment variable.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
