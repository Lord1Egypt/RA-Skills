## Description:

钓鱼热点智能推送，自动聚合钓鱼社区、搜索引擎、天气 API 和位置数据，帮助用户发现附近钓点、实时鱼情并生成可视化报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect fishing hotspot signals for a target city, rank likely fishing locations using weather, distance and report freshness, and produce commands or reports for trip planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fishing-related city or location queries and extracted place names may be sent to Amap and QWeather.

Mitigation: Use the skill only when sharing those queries with the configured third-party API providers is acceptable.

Risk: The skill can read API keys from an existing fishing-trip-planner configuration.

Mitigation: Review local configuration files and API-key scopes before running setup or hotspot analysis.

Risk: Generated HTML reports may include outside data that has not been safely escaped or path-restricted.

Mitigation: Treat generated reports as untrusted local files and review report output paths before opening or sharing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/fishing-hotspot-push)
- [Project Homepage](https://github.com/bettermen/fishing-hotspot-push)
- [API Key Guide](references/api_guide.md)
- [Amap Developer Platform](https://lbs.amap.com/)
- [QWeather Developer Platform](https://dev.qweather.com/)
- [fishing-trip-planner Integration](https://github.com/bettermen/fishing-trip-planner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, configuration notes, and generated local HTML report paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Amap and QWeather APIs, use agent-supplied search text, and archive generated HTML reports locally.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
