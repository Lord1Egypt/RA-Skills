## Description: <br>
Use when a user ask run a Bing web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to turn natural-language Bing search requests into Dataify Bing Search API calls and return the API response directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill can send DATAIFY_API_TOKEN to a caller-controlled URL through the endpoint override. <br>
Mitigation: Install only after verifying requests are restricted to the intended Dataify endpoint, and do not provide DATAIFY_API_TOKEN unless the override is removed or safely allowlisted. <br>
Risk: Search requests can include precise location data such as latitude, longitude, or named locations. <br>
Mitigation: Avoid location fields unless localized results are required, and review the parameter table before confirming a live API call. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-bing-search) <br>
- [Dataify Bing Search API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown parameter table before live calls, followed by raw Dataify API response as JSON and/or HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN for live calls; returned API content is not summarized or post-processed by the skill.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
