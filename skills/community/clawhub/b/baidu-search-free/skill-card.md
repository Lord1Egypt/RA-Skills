## Description: <br>
Free Baidu web search, no API key required, supports time range filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoxh](https://clawhub.ai/user/guoxh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run Baidu web searches from an agent workflow, including Chinese or English queries, result-count limits, and freshness filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Baidu and may reveal private or sensitive intent. <br>
Mitigation: Avoid private or sensitive queries and review organizational policy before using the skill. <br>
Risk: Network behavior and search results depend on Baidu availability, anti-scraping checks, and the trustworthiness of any proxy or VPN used. <br>
Mitigation: Expect occasional failures, review returned links before relying on them, and use only trusted network providers. <br>
Risk: The skill depends on third-party Python packages and performs live web requests. <br>
Mitigation: Install in a virtual environment and prefer pinned, current dependency versions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoxh/baidu-search-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON search results with title, URL, snippet, and time fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and sends search queries to Baidu over the network.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
