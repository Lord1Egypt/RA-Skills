## Description: <br>
Track football teams and return last match, next match, kickoff time, broadcasters, standings, and recent news in a compact emoji-formatted summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geison-paitra](https://clawhub.ai/user/geison-paitra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to track football clubs and FIFA World Cup 2026 national teams, including recent results, upcoming fixtures, venues, standings, broadcasters, and news in English or Portuguese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires and stores a football-data.org API key for club lookups. <br>
Mitigation: Use a dedicated low-privilege key, remove stored keys when no longer needed, and rotate any key that was accidentally bundled or pasted into chat. <br>
Risk: Football match, standings, broadcaster, and news data may be incomplete or unavailable from upstream sources. <br>
Mitigation: Review the returned N/A or unavailable fields before relying on the summary, especially for time-sensitive match and broadcast information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/geison-paitra/football-tracker) <br>
- [FIFA World Cup 2026 match schedule](http://digitalhub.fifa.com/asset/4b5d4417-3343-4732-9cdf-14b6662af407/FWC26-Match-Schedule_English.pdf) <br>
- [English output pack](references/locales/en.md) <br>
- [Portuguese output pack](references/locales/pt-br.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Compact Markdown-style text with emoji-labeled sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Portuguese output; club lookups may require a football-data.org API key, while supported World Cup 2026 national team lookups use bundled schedule data.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and artifact config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
