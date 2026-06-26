## Description: <br>
Provides real-time live cricket scores, detailed scorecards, upcoming matches, recent results, IPL standings, and match alerts using the CricketData.org API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harshilmathur](https://clawhub.ai/user/harshilmathur) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and cricket followers use this agent skill to retrieve live scores, scorecards, schedules, recent results, IPL standings, and cron-ready match alerts from CricketData.org through shell scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a CricketData.org API key, and the service uses API-key query parameters. <br>
Mitigation: Prefer CRICKET_API_KEY over saving the key in config, use a free or limited key, avoid shared multi-user machines where process arguments or temporary files may be visible, and rotate the key if exposed. <br>
Risk: The skill writes local cache and alert state under /tmp by default. <br>
Mitigation: Use the default only on trusted single-user systems or set an appropriate cache location for the runtime environment. <br>


## Reference(s): <br>
- [CricketData.org API](https://cricketdata.org) <br>
- [ClawHub skill page](https://clawhub.ai/harshilmathur/cricket-live) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Messaging-friendly text with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local caching and requires a CricketData.org API key for live API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
