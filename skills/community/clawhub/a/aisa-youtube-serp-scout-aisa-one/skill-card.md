## Description: <br>
Search YouTube videos, channels, and trends through the AIsa YouTube SERP client for content research, competitor tracking, and trend discovery without managing Google credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and research agents use this skill to run YouTube search, channel discovery, trend monitoring, top-video lookup, and competitor research through the AIsa API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and competitor research terms are sent to AIsa's API with an AISA_API_KEY. <br>
Mitigation: Use a dedicated, revocable AIsa API key where possible, and avoid submitting confidential campaign names, private competitor research, secrets, or other sensitive data in queries. <br>
Risk: The skill can return external YouTube search data that may be incomplete, stale, or unsuitable for final competitor conclusions without review. <br>
Mitigation: Review returned results before relying on trend or competitor analysis, and do not claim analysis succeeded until the client returns data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aisadocs/aisa-youtube-serp-scout-aisa-one) <br>
- [AIsa Homepage](https://aisa.one) <br>
- [AIsa YouTube Search API Endpoint](https://api.aisa.one/apis/v1/youtube/search) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples; bundled Python client returns JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and sends YouTube search requests to the AIsa API.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
