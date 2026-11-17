## Description:

Provides agents with structured China A-share market data, company fundamentals, financial statements, shareholder and fund-holding signals, institutional activity, event tracking, news, and announcements through the Equal Data service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kanjiujing](https://clawhub.ai/user/kanjiujing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external agent users can use this skill to retrieve China A-share quotes, historical K-line data, fundamentals, financial metrics, shareholder data, institutional holdings, event-driven signals, and related financial news for research, screening, monitoring, and report generation. The artifact describes the data use as market-data retrieval and not trade execution.

### Deployment Geography for Use:

Global; data coverage focuses on China A-share markets.

## Known Risks and Mitigations:

Risk: The external equal-data Python package and Equal Data service receive EQUAL_DATA_API_KEY.

Mitigation: Use a virtual environment, prefer a narrowly scoped or low-value key if available, avoid committing or logging the key, and rotate the key if exposure is suspected.

Risk: The security review notes dependency, provenance, and activation-scope concerns.

Mitigation: Review package provenance before deployment, pin and hash-lock dependencies for production, keep dependencies updated, and enable the skill only in environments where this data access is intended.

Risk: The skill returns financial market data and analysis that may be incomplete, delayed, or unsuitable as standalone investment guidance.

Mitigation: Validate important outputs against trusted sources and require human review before using results for financial decisions or reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kanjiujing/skills/equal-data-skill)
- [Equal Data introduction](https://equaldata.kanjiujing.cn/equal/dist/introduction)
- [Equal Data website](https://equaldata.kanjiujing.cn)
- [equal-data PyPI package](https://pypi.org/project/equal-data/)
- [Skill quick start and interface index](artifact/skill.md)
- [Data interface catalog](artifact/reference/数据接口.md)
- [Individual stock analysis API](artifact/reference/场景Agent/个股详情分析.md)
- [Realtime quote API](artifact/reference/行情数据/实时行情列表.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with Python examples, shell commands, configuration snippets, and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the equal-data Python package and an EQUAL_DATA_API_KEY; most API calls return structured financial records.]

## Skill Version(s):

0.0.29 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
