## Description: <br>
一个功能完整的星座 MCP (Model Context Protocol) 服务，提供星座信息查询、运势分析、配对测试等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up zodiac details, daily horoscope information, compatibility analysis, zodiac signs by date, and rising-sign information through the XiaoBenYang service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a XiaoBenYang API key and can store it in a local .env file. <br>
Mitigation: Use only an API key you are authorized to use, protect the .env file from disclosure, and rotate the key if it may have been exposed. <br>
Risk: Horoscope requests are sent to the XiaoBenYang service, and the rising-sign feature can include birth date, exact birth time, and location coordinates. <br>
Mitigation: Use the rising-sign feature only when sharing that information with the API provider is acceptable, and avoid providing more precise personal data than needed. <br>
Risk: The reviewed release contains copied gaokao naming leftovers that may make configuration and trust review less clear. <br>
Mitigation: Review the configured API endpoint and requested parameters before deployment, and prefer a publisher update that removes stale naming. <br>


## Reference(s): <br>
- [星座服务 on ClawHub](https://clawhub.ai/alinklab/constellation) <br>
- [XiaoBenYang API key portal](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Text or Markdown summaries derived from JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a XiaoBenYang API key and may save it to a local .env file.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
