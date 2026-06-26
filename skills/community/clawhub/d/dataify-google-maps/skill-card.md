## Description: <br>
When the user requests "call Google Maps" or "map search/location details", or explicitly mentions the map search field, the dataify-google-maps skill is triggered. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert Google Maps search or place-detail requests into Dataify Scraper API form submissions. It guides parameter selection, asks for confirmation, and returns the API response body directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map search terms, addresses, coordinates, place IDs, and related parameters are sent to Dataify. <br>
Mitigation: Use the skill only for data that may be shared with Dataify, and avoid submitting sensitive personal or precise-location information unless approved. <br>
Risk: API tokens may be exposed if pasted into chat or passed directly on a command line. <br>
Mitigation: Prefer DATAIFY_API_TOKEN from a protected environment variable and avoid echoing tokens in prompts, logs, or final responses. <br>
Risk: The required confirmation table is hardcoded in Chinese, which can reduce review quality for non-Chinese users. <br>
Mitigation: Have a user who can read the confirmation table review parameters before approving API calls, or translate the table before operational use. <br>


## Reference(s): <br>
- [Dataify Google Maps API Reference](references/google_maps_api.md) <br>
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request) <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-google-maps) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown confirmation table and raw Dataify API response body, often JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before API calls and returns the API response directly without summarization.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
