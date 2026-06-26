## Description: <br>
firstdata helps agents find official portals, APIs, and download paths for 1000+ authoritative primary data sources, including governments, international organizations, and research institutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ningzimu](https://clawhub.ai/user/ningzimu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to locate authoritative primary data sources, compare source authority, and obtain official access paths, API documentation, and download methods for evidence-chain workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects agents to a hosted FirstData lookup service, so queries may leave the local environment. <br>
Mitigation: Install only if the hosted service is trusted and avoid sending secrets or regulated data through the MCP unless approved. <br>
Risk: The FIRSTDATA_API_KEY token grants access to the FirstData service. <br>
Mitigation: Treat the token like a password, keep it out of logs and shared files, and rotate it if exposed. <br>
Risk: Using an unpinned setup command may install a newer CLI version than expected. <br>
Mitigation: Prefer manual MCP configuration or a pinned CLI version when deployment reproducibility matters. <br>


## Reference(s): <br>
- [FirstData project homepage](https://github.com/MLT-OSS/FirstData) <br>
- [FirstData MCP endpoint](https://firstdata.deepminer.com.cn/mcp) <br>
- [FirstData registration guide](references/firstdata-register.md) <br>
- [ClawHub skill page](https://clawhub.ai/ningzimu/firstdata) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with API endpoints, MCP configuration examples, and source-navigation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require FIRSTDATA_API_KEY and curl for connecting to the hosted FirstData MCP service.] <br>

## Skill Version(s): <br>
0.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
