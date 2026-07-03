## Description: <br>
Provides a Claude Desktop MCP-style helper that returns current date and time strings in multiple requested formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Desktop users use this skill to request a date or time format and receive the corresponding formatted current timestamp. It supports common date, time, compact, filename, ISO-like, and log-oriented formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a remote API key and may store XBY_APIKEY in a local .env file. <br>
Mitigation: Use only where the publisher and xiaobenyang.com are intentionally trusted, and prefer environment-scoped secret handling or a local formatter that does not persist secrets. <br>
Risk: Date/time formatting requests are sent to an external service for functionality that can usually be handled locally. <br>
Mitigation: Review data-sharing expectations before use and prefer a local date/time formatter when a remote API is not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/datetime) <br>
- [XiaoBenYang API key site](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Dictionary/JSON result with raw API payload, success flag, and status message; the agent presents formatted date/time text to the user.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a format parameter and an XBY_APIKEY before the remote API call can succeed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
