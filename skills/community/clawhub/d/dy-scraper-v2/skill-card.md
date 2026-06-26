## Description: <br>
Searches Douyin for popular video and caption data from natural-language search intents, extracts keywords, and can retrieve hot-list results. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents can use this skill to search Douyin topics or hot lists and present video metadata for research-oriented content review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Networked searches may send search terms to Douyin and sometimes Brave Search. <br>
Mitigation: Avoid sensitive search terms, review platform rules before use, and run with conservative limits and delays. <br>
Risk: The skill may use a BRAVE_API_KEY from the environment. <br>
Mitigation: Scope the key to this runtime, avoid sharing it in logs or prompts, and rotate it if exposure is suspected. <br>
Risk: Installation and execution may add Playwright/Chromium browser tooling. <br>
Mitigation: Install and run the skill in an isolated environment where browser downloads and network access are expected. <br>
Risk: Returned results can be live Douyin data, Brave Search results, or sample data. <br>
Mitigation: Treat results as unverified unless the response clearly identifies the source and freshness. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/dy-scraper-v2) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Playwright documentation](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown search results with console text and optional JSON or CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may come from Douyin, Brave Search fallback, or sample data when live retrieval fails.] <br>

## Skill Version(s): <br>
1.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
