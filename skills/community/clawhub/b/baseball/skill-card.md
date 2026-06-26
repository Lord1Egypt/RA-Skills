## Description: <br>
Fetch MLB game schedules, live game status, box scores, player search, and season statistics via the MLB Stats API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khaney64](https://clawhub.ai/user/khaney64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer baseball schedule, score, live game, player lookup, and season-stat questions from public MLB data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public MLB Stats API endpoints, so availability, latency, and returned data are outside the skill's control. <br>
Mitigation: Handle failed or empty lookups gracefully and confirm important game or player facts against the source data before relying on them. <br>
Risk: Excessive polling or bulk requests may trigger blocking by the upstream MLB service. <br>
Mitigation: Limit live-game polling to the documented interval and avoid bulk scraping workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/khaney64/baseball) <br>
- [MLB Stats API schedule endpoint](https://statsapi.mlb.com/api/v1/schedule/games) <br>
- [MLB Stats API live game endpoint](https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live) <br>
- [MLB Stats API player search endpoint](https://statsapi.mlb.com/api/v1/people/search) <br>
- [MLB copyright notice](http://gdx.mlb.com/components/copyright.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text tables or JSON from Python command-line scripts, with Markdown command examples in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and network access to public MLB Stats API endpoints; no API key is documented.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
