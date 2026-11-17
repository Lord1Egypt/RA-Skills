## Description:

酒店聚合助手，整合分贝通、携程、美团、同程、华住会、锦江等多个酒店数据源，提供统一的酒店搜索、房型查询、预订服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

Travel agents, business travelers, and travel-support workflows can use this skill to request hotel searches, compare room and price data across named Chinese travel platforms, and format aggregated hotel results. Release metadata names the skill as flight-status related, but the artifact evidence describes hotel aggregation behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release metadata names a flight-status skill while the artifact implements hotel aggregation, which can mislead users about the skill's purpose.

Mitigation: Review the release title, slug, and public description before publication so they match the packaged artifact.

Risk: Security evidence says the skill overstates real provider search, room lookup, price comparison, and booking capabilities.

Mitigation: Present the skill as unfinished until live provider integrations are implemented and verified.

Risk: Future real provider calls may disclose travel-search details to third-party platforms.

Mitigation: Document which hotel platforms receive user search details and require review of platform-specific data handling before enabling live calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/flight-status-check)
- [Publisher profile](https://clawhub.ai/user/ryan-zry)
- [Fenbeitong OpenAPI endpoint](https://openapiv2.fenbeitong.com)
- [Ctrip API endpoint](https://api.ctrip.com)
- [Meituan API endpoint](https://api.meituan.com)
- [Tongcheng API endpoint](https://api.tongcheng.com)
- [Huazhu API endpoint](https://api.huazhu.com)
- [Jinjiang API endpoint](https://api.jinjiang.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, API Calls, guidance]

**Output Format:** [Markdown tables, JSON-like result objects, and function-call responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; current provider-search implementations return empty results until real platform API integrations are completed.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
