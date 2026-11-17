## Description:

基于GTFS数据的Caltrain火车时刻查询服务，提供实时火车时刻表、站点查询和时间特定查询功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to answer Caltrain station and scheduled departure questions by calling a XiaoBenYang-hosted API after configuring an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a third-party XiaoBenYang API key and stores it in a project .env file in plaintext.

Mitigation: Use only when the key requirement is understood; prefer session-only or secret-manager storage and avoid committing .env files.

Risk: The server security summary marks the release suspicious because the Caltrain skill depends on a third-party service and includes unrelated Gaokao references.

Mitigation: Review the skill before installation, confirm the external service is acceptable, and prefer a version with the unrelated references removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/caltrain)
- [XiaoBenYang API key service](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration guidance]

**Output Format:** [Markdown or text summarizing JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns Caltrain station lists or scheduled departures based on origin, destination, and optional ISO-8601 time.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
