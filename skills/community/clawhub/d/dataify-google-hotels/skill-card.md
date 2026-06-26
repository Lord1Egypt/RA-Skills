## Description: <br>
Dataify Google Hotels turns a user's hotel price or availability request into a confirmed Dataify Scraper API Google Hotels form POST. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare and run Google Hotels searches through Dataify, including destination, date, occupancy, currency, filtering, pagination, and detail lookup parameters. The skill requires a parameter review before each live API call and returns the API response body directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A live request can send hotel search parameters, travel dates, and an API credential to Dataify. <br>
Mitigation: Review the generated parameter table before confirming a call, keep DATAIFY_API_TOKEN out of shared chat logs, and use the environment variable or explicit token handling described by the skill. <br>
Risk: The skill returns the API response body directly, which may include third-party result data that has not been summarized or filtered. <br>
Mitigation: Inspect returned data before using it in downstream workflows, publications, or customer-facing decisions. <br>


## Reference(s): <br>
- [Dataify Google Hotels API](references/google_hotels_api.md) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown parameter table, Python command examples, and raw API response body] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN for live calls; performs a dry-run parameter review before sending requests.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
