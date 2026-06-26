## Description: <br>
Fetches BlockBeats crypto news, filters items by keyword, removes HTML from text fields, formats timestamps, and returns structured JSON for downstream automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leesen86](https://clawhub.ai/user/leesen86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to retrieve recent BlockBeats crypto news, filter it by one or more keywords, and pass the cleaned JSON results into summarization, translation, notification, or other workflow steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled Feishu push scripts include hardcoded gateway credentials and a default recipient. <br>
Mitigation: Use only the core news fetcher unless Feishu delivery is explicitly needed; remove or rotate embedded credentials and require explicit recipient selection before sending messages. <br>
Risk: The push script invokes the news fetcher through shell command construction. <br>
Mitigation: Prefer argument-based process execution and validate user-provided keyword and count inputs before enabling push automation. <br>
Risk: Fetched news depends on the BlockBeats API shape and availability. <br>
Mitigation: Treat returned fields as variable, validate the JSON array before downstream processing, and handle API failures or empty results. <br>


## Reference(s): <br>
- [BlockBeats Open Flash API](https://api.theblockbeats.news/v1/open-api/open-flash) <br>
- [ClawHub release page](https://clawhub.ai/leesen86/get-news) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Guidance] <br>
**Output Format:** [JSON array emitted to stdout, with command examples documented in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [News items have text fields cleaned of HTML and timestamp fields formatted while preserving raw timestamp values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
