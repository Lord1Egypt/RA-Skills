## Description:

Chill Beijing generates Beijing after-work and weekend leisure recommendations with weather and browser-scraped source data when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoyachao](https://clawhub.ai/user/caoyachao)

### License/Terms of Use:

MIT-0

## Use Case:

Beijing residents, visitors, and agents assisting them use this skill to produce leisure recommendations for workday evenings, Fridays, and weekends across movies, comedy, performances, city walks, short trips, and social activities.

### Deployment Geography for Use:

Global; recommendations are scoped to Beijing, China.

## Known Risks and Mitigations:

Risk: Live browser scraping is run with unsafe browser settings.

Mitigation: Run the skill only in an isolated environment without sensitive files or credentials.

Risk: Recommendations may present hard-coded event times, prices, availability, or venue details as current.

Mitigation: Verify event details directly with the listed platforms or venues before relying on them.

Risk: External pages can fail, change structure, require login, or return incomplete scraped data.

Mitigation: Treat missing or fallback output as incomplete and confirm recommendations through primary sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/caoyachao/skills/chill-beijing)
- [wttr.in Beijing Weather Endpoint](https://wttr.in/Beijing?format=j1)
- [Maoyan Films Source](https://maoyan.com/films?showType=1&offset=0&limit=10)
- [Damai Beijing Performances Source](https://www.damai.cn/search.htm?spm=a2oeg.home.category.ditem_1.591b23e1xT9zBv&ctl=%E6%BC%94%E5%87%BA%E4%BC%9A&order=1&cty=%E5%8C%97%E4%BA%AC)
- [Meituan Leisure Source](https://www.meituan.com/xiuxianyule/)
- [Xiaohongshu Search Source](https://www.xiaohongshu.com/search_result)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text printed to stdout or returned as a string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch Puppeteer and make live network requests; event times, prices, availability, and venue claims require source verification.]

## Skill Version(s):

1.4.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
