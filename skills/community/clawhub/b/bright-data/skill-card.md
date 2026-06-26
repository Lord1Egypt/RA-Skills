## Description: <br>
Provides web scraping and Google search through Bright Data APIs, returning scraped pages as Markdown and search results as structured JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MeirKaD](https://clawhub.ai/user/MeirKaD) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to search Google and retrieve webpage content through Bright Data when they need structured search results or Markdown page extracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, target URLs, and search queries may expose sensitive information or create unintended Bright Data usage costs. <br>
Mitigation: Use a scoped Bright Data API key and zone, avoid confidential URLs or queries, and monitor usage and billing. <br>
Risk: Web scraping and search activity may violate applicable law or target-site rules if used outside approved policies. <br>
Mitigation: Confirm that each use complies with applicable law, Bright Data terms, and the target site's rules before running the scripts. <br>


## Reference(s): <br>
- [Bright Data Dashboard](https://brightdata.com/cp) <br>
- [Bright Data Request API Endpoint](https://api.brightdata.com/request) <br>
- [ClawHub Skill Page](https://clawhub.ai/MeirKaD/bright-data) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Configuration] <br>
**Output Format:** [JSON search results or Markdown scraped page content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRIGHTDATA_API_KEY and BRIGHTDATA_UNLOCKER_ZONE; accepts either a search query with optional cursor or a webpage URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
