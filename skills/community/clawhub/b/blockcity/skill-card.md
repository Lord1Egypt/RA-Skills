## Description: <br>
区块城市 retrieves BlockCity city ranking and detail data from blockcity.vip, including rank, population, opened blocks, fund balance, remaining popularity, and city officials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgta23](https://clawhub.ai/user/hgta23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch, filter, and serialize public BlockCity city ranking and city-detail data for analysis, reporting, or downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to blockcity.vip and may use scraper dependencies including Playwright. <br>
Mitigation: Run it only in environments where outbound access to blockcity.vip is approved, and review site terms and request volume before scheduled or high-volume use. <br>
Risk: City-detail fields such as fund balance, remaining popularity, mayor, and block counts may be incomplete, defaulted, or stale. <br>
Mitigation: Validate important results against the live BlockCity page or another trusted source before using them for decisions. <br>
Risk: Fallback mock data can be returned when live data fetching fails. <br>
Mitigation: Disable fallback mock data for workflows that require live-only results, or label fallback results clearly in downstream output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgta23/blockcity) <br>
- [BlockCity ranking page](https://www.blockcity.vip/pages/block/area) <br>
- [BlockCity website](https://www.blockcity.vip) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python dictionaries and JSON strings, with usage guidance in Markdown and Python examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports in-memory caching, configurable cache TTL, city filtering, and optional fallback mock data.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
