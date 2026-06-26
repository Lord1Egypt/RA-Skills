## Description: <br>
Queries CPBL Chinese Professional Baseball League scores, schedules, live games, standings, player stats, news, and Taiwan baseball history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ichendong](https://clawhub.ai/user/ichendong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Taiwan CPBL questions about live scores, schedules, standings, game results, player stats, recent news, and historical baseball facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents stealth-browser access to a protected third-party wiki. <br>
Mitigation: Prefer the bundled CPBL scripts and ordinary web search; use the Scrapling workflow only with authorization and after reviewing the source site's terms. <br>
Risk: Live sports data and official-site HTML fragments may lag, change structure, or return partial results. <br>
Mitigation: Treat script output as time-sensitive, state gaps when data is missing, and cross-check important answers against official CPBL pages or documented fallback sources. <br>
Risk: Some schedule, stats, and historical-data flows depend on brittle AJAX endpoints, CSRF handling, or protected pages. <br>
Mitigation: Use the narrowest script for the query, avoid inventing missing values, and fall back to documented references or user-visible source links when retrieval fails. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ichendong/cpbl) <br>
- [API endpoint notes](references/api-endpoints.md) <br>
- [Implementation summary](references/summary.md) <br>
- [Test report](references/test-report.md) <br>
- [Test log](references/test-log.txt) <br>
- [CPBL official news](https://cpbl.com.tw/news) <br>
- [CPBL official standings](https://www.cpbl.com.tw/standings/season) <br>
- [Taiwan Baseball Wiki MVP page](https://twbsball.dils.tku.edu.tw/wiki/index.php?title=中華職棒年度最有價值球員) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON responses with optional shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on live CPBL site responses, official-site HTML fragments, web search for news, and optional browser-based retrieval for protected historical pages.] <br>

## Skill Version(s): <br>
1.5.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
