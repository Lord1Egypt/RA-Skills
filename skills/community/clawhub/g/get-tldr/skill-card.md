## Description: <br>
Provide the summary returned by the get-tldr.com summarize API without further summarization; the skill should format the API output for readability but must not change its content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itobey](https://clawhub.ai/user/itobey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to obtain the get-tldr.com summary for a supplied URL while preserving the API-provided summary text. It is useful when an agent needs to fetch a concise link summary without rewriting or further compressing the service response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs are sent to get-tldr.com for summarization and may disclose sensitive link targets or query strings. <br>
Mitigation: Use the skill only for URLs that are appropriate to share with get-tldr.com, and avoid links containing private tokens or sensitive query parameters. <br>
Risk: The bundled script can store submitted URLs and returned summaries in a local log file. <br>
Mitigation: Configure the logfile path deliberately, restrict access to it, or delete/disable the log when summarized links or summaries may be sensitive. <br>
Risk: The skill requires a get-tldr API key that could be exposed through local configuration or environment files. <br>
Mitigation: Use a dedicated API key and keep config, environment, and .env files private. <br>


## Reference(s): <br>
- [ClawHub get-tldr release page](https://clawhub.ai/itobey/get-tldr) <br>
- [get-tldr summarize API endpoint](https://www.get-tldr.com/api/v1/summarize) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown summary text returned to the user; the bundled script prints JSON from the API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a URL input and a get-tldr API key. The agent should preserve the API summary content and only remove unwanted code-block wrapping so Markdown renders normally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
