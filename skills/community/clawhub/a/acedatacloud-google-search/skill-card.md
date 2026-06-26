## Description: <br>
Search the web using Google via AceDataCloud API for web pages, images, news, maps, local places, or videos, with localization, time filtering, pagination, and structured result data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Germey](https://clawhub.ai/user/Germey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Google SERP searches through AceDataCloud for web, image, news, maps, places, and video results with localization, time filtering, and pagination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, localization parameters, URLs, or business context may be sent to AceDataCloud. <br>
Mitigation: Do not use secrets, private URLs, internal identifiers, or sensitive personal or business data unless that third-party transmission is approved. <br>
Risk: The AceDataCloud API token can grant access to paid or private API usage if exposed. <br>
Mitigation: Store the token as a protected environment secret and avoid committing, logging, or sharing it. <br>
Risk: The optional MCP package or hosted MCP service adds another third-party component to the workflow. <br>
Mitigation: Review the MCP package or hosted service before enabling it in a production agent. <br>


## Reference(s): <br>
- [ClawHub Google Search release](https://clawhub.ai/Germey/acedatacloud-google-search) <br>
- [AceDataCloud Google SERP API](https://api.acedata.cloud/serp/google) <br>
- [AceDataCloud hosted SERP MCP](https://serp.mcp.acedata.cloud/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ACEDATACLOUD_API_TOKEN; search parameters include query, search_type, country, language, time_range, number, and page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; skill metadata version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
