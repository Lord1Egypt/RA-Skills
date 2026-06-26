## Description: <br>
Check if AC Milan played yesterday and send the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paoloxiamn](https://clawhub.ai/user/paoloxiamn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Fans and automation users use this skill to run a daily AC Milan match check and forward a concise result message when the club played the previous day. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled execution makes public web requests to ESPN and Google News. <br>
Mitigation: Install only if these public requests fit the deployment environment, and keep cron or nodes.run configured to the reviewed check_match.py path. <br>
Risk: The schedule updater rewrites the bundled schedule.json file. <br>
Mitigation: Run update_schedule.py only when automatic schedule refresh is desired, and review the changed schedule before relying on it for notifications. <br>
Risk: The notifier may include related YouTube highlight search and Google News links in addition to match results. <br>
Mitigation: Forward the output only when those related links are appropriate for the recipient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paoloxiamn/acmilan-match-monitor) <br>
- [ESPN AC Milan schedule endpoint](https://site.api.espn.com/apis/site/v2/sports/soccer/ita.1/teams/103/schedule?limit=5) <br>
- [Google News RSS search endpoint](https://news.google.com/rss/search?q={news_query}&hl=en&gl=US&ceid=US:en) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text match notification with links, plus Markdown and JSON setup examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Silent when no scheduled previous-day match is found; may include a YouTube highlights search link and up to three Google News links.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
