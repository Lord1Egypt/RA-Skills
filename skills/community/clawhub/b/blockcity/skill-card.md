## Description:

BlockCity区块城市数据获取Skill，支持从排名页获取城市排名、居民人数、开启区块数，从城市详情页获取基金余额、剩余人气值等信息.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve BlockCity city ranking data, look up cities by name or rank, filter returned city records, and serialize results for downstream use. Detail-page outputs should be treated cautiously because server security evidence notes that some detail fields may be placeholders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detail-page fields such as fund balance and remaining popularity may be zero, mock, or placeholder values while appearing in normal output.

Mitigation: Treat detail-page results as unverified, validate them against BlockCity directly before use, and prefer ranking-page fields for workflows that require live data.

Risk: The skill performs network requests to a public website and depends on that site's response format.

Mitigation: Install in an isolated Python environment, pin dependencies, use reasonable request rates, and review outputs when the BlockCity site changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hgta23/skills/blockcity)
- [BlockCity Ranking Page](https://www.blockcity.vip/pages/block/area)
- [BlockCity Site](https://www.blockcity.vip)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON-shaped data outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch public BlockCity data over HTTP and may fall back to cached or mock values when live data is unavailable.]

## Skill Version(s):

1.2.0 (source: frontmatter, setup.py, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
