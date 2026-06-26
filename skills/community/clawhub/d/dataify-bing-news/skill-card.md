## Description: <br>
Use when a user wants to run a Bing News search through the Dataify Bing News API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert natural-language Bing News requests into Dataify API parameters, preview the request, and call the API after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Dataify during live Bing News API calls. <br>
Mitigation: Avoid private, regulated, or confidential search queries unless the deployment has approved that data flow. <br>
Risk: The skill handles a Dataify API token for authentication. <br>
Mitigation: Use DATAIFY_API_TOKEN or another secure secret mechanism instead of pasting tokens into chat prompts or command lines. <br>
Risk: The skill returns API responses directly, which may include raw JSON or HTML from the service. <br>
Mitigation: Review returned content before using it in downstream workflows, publications, or automated decisions. <br>


## Reference(s): <br>
- [Dataify Bing News API Reference](references/api.md) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-bing-news) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown parameter previews, shell commands, and raw Dataify API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live calls require a Dataify API token and user confirmation after previewing request parameters.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
