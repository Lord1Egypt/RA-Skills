## Description: <br>
Query AV new releases, rankings, and actress info from FANZA GraphQL API. No authentication required. Supports direct curl queries and optional Discord/Telegram bot deployment. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[zxcnny930](https://clawhub.ai/user/zxcnny930) <br>

### License/Terms of Use: <br>
PolyForm Noncommercial 1.0.0 <br>


## Use Case: <br>
External adult users and developers use this skill to query FANZA AV releases, rankings, actress information, and product metadata through curl-based GraphQL examples. Users must be 18+ and comply with applicable local laws. <br>

### Deployment Geography for Use: <br>
Global, subject to local adult-content laws and service availability <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries adult-content metadata and may expose user interest in adult material to FANZA/DMM. <br>
Mitigation: Use only if the user is 18+ and comfortable sending adult-content queries to FANZA/DMM, and follow applicable local laws. <br>
Risk: Optional Discord or Telegram bot deployment requires bot tokens and persistent service configuration. <br>
Mitigation: Keep tokens out of source control and logs, restrict configuration file permissions, rotate exposed tokens, and run services under a dedicated unprivileged user. <br>
Risk: The FANZA GraphQL endpoint is described by the artifact as undocumented and unofficial, so responses or availability may change. <br>
Mitigation: Handle empty results, GraphQL errors, rate limits, and service outages as expected operating conditions before relying on results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zxcnny930/avbuzz) <br>
- [FANZA GraphQL API Endpoint](https://api.video.dmm.co.jp/graphql) <br>
- [DMM FANZA Product Detail URL Pattern](https://www.dmm.co.jp/digital/videoa/-/detail/=/cid={id}/) <br>
- [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include FANZA result summaries, curl commands, GraphQL query payloads, and optional Discord or Telegram bot configuration guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
