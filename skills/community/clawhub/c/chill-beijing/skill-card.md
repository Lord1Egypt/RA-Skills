## Description: <br>
Chill Beijing recommends after-work and weekend activities in Beijing, including films, comedy, performances, city walks, nearby trips, and social activities using live data from third-party platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoyachao](https://clawhub.ai/user/caoyachao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate current Beijing leisure recommendations for workdays, Fridays, and weekends. It is intended for local activity discovery and itinerary guidance, not authoritative booking, pricing, or availability decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User queries and activity preferences may be used for live lookups against third-party platforms. <br>
Mitigation: Avoid submitting sensitive personal information and review which sites the skill contacts before use. <br>
Risk: Browser-based scraping can return stale, incomplete, or failed results when third-party pages change or block automation. <br>
Mitigation: Verify recommendations, prices, schedules, and availability directly with the listed platform or venue before acting on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/caoyachao/chill-beijing) <br>
- [Publisher Profile](https://clawhub.ai/user/caoyachao) <br>
- [wttr.in Beijing Weather Endpoint](https://wttr.in/Beijing?format=j1) <br>
- [Maoyan Film Listings](https://maoyan.com/films?showType=1&offset=0&limit=10) <br>
- [Damai Beijing Performance Search](https://www.damai.cn/search.htm?spm=a2oeg.home.category.ditem_1.591b23e1xT9zBv&ctl=%E6%BC%94%E5%87%BA%E4%BC%9A&order=1&cty=%E5%8C%97%E4%BA%AC) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, code] <br>
**Output Format:** [Markdown recommendations by default, with optional JSON output and JavaScript API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live results may vary by date, third-party platform availability, and page structure changes.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
