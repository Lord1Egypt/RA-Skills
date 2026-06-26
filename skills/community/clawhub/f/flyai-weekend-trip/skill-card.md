## Description: <br>
周末去哪儿2天1夜说走就走方案助手。输入出发城市和本周末日期，一次性生成3个"说走就走"的周末方案，每个包含目的地+航班/高铁+酒店+精选景点+总价估算。当用户提到"周末去哪"、"周末出游"、"2天1夜"、"说走就走"、"周末旅行"、"这周末出去玩"、"短途游"时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers use this skill to plan short weekend trips by giving a departure city, dates, budget, and travel preferences. The agent gathers current FlyAI travel search results and returns three actionable 2-day, 1-night itinerary packages with transportation, hotel, attractions, booking links, and estimated cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow guidance suggests a sudo-based global install path for the FlyAI CLI. <br>
Mitigation: Review installation steps before use and prefer a user-scoped Node environment such as nvm instead of sudo. <br>
Risk: The workflow guidance suggests setting NODE_TLS_REJECT_UNAUTHORIZED=0 after TLS certificate failures. <br>
Mitigation: Keep TLS verification enabled; resolve certificate or network trust issues before running travel search commands. <br>
Risk: The skill can store personal travel profile details in memory or a local file. <br>
Mitigation: Save profile details only after explicit user confirmation and avoid storing sensitive travel or identity information. <br>


## Reference(s): <br>
- [AI Search reference](reference/ai-search.md) <br>
- [Keyword Search reference](reference/keyword-search.md) <br>
- [Flight Search reference](reference/search-flight.md) <br>
- [Hotel Search reference](reference/search-hotel.md) <br>
- [Marriott Hotel Search reference](reference/search-marriott-hotel.md) <br>
- [Marriott Package Search reference](reference/search-marriott-package.md) <br>
- [POI Search reference](reference/search-poi.md) <br>
- [Train Search reference](reference/search-train.md) <br>
- [User Profile Storage reference](reference/user-profile-storage.md) <br>
- [Workflow reference](reference/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown travel recommendations with inline FlyAI shell commands and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live FlyAI search results when available and may read or save a user travel profile after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
