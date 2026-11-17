## Description:

今日宜出门 - 黄历+农历+天气综合出门建议。用户问「今天适合出门吗/宜出门/黄历/今日宜忌/适合买东西吗」时使用。结合个人八字（生肖冲煞）给定制化建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangmengyang](https://clawhub.ai/user/zhangmengyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to answer daily Chinese almanac, lunar-calendar, weather, and outing-suitability questions, optionally personalized from a local birth-profile file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store birth date, birth time, city, longitude, zodiac, and bazi profile details locally for personalization.

Mitigation: Run it only where local profile storage is acceptable, review or set DAILY_GUIDE_BAZI for the profile path, and remove the profile when personalization is no longer needed.

Risk: Weather and almanac cross-checks contact third-party services, and default weather lookup may rely on IP-based location.

Mitigation: Set DAILY_GUIDE_CITY before use when location control matters, and account for third-party service availability and policy requirements.

Risk: The installed npm dependency and cached almanac data affect the generated guidance.

Mitigation: Review the lunar-javascript dependency and cached data source under local supply-chain controls before deployment.

## Reference(s):

- [ClawHub daily-guide skill page](https://clawhub.ai/zhangmengyang/skills/daily-guide)
- [ClawHub publisher profile](https://clawhub.ai/user/zhangmengyang)
- [Tianqi static almanac data endpoint](https://staticwnl.tianqistatic.com/Home/js/api/yjs/${year}.js)
- [wttr.in weather service](https://wttr.in/)
- [lunar-javascript 1.7.7 package artifact](https://registry.npmmirror.com/lunar-javascript/-/lunar-javascript-1.7.7.tgz)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable Chinese report or structured JSON from command-line execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include lunar-calendar details, almanac cross-checks, weather conditions, matter-specific recommendations, and local-profile personalization status.]

## Skill Version(s):

1.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
