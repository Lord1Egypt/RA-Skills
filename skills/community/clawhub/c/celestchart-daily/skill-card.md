## Description: <br>
Gets daily personal horoscope forecasts and birth chart readings through the CelestChart Astrology API; daily forecasts require a VIP account and API key, while birth chart readings are public. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maye08](https://clawhub.ai/user/maye08) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to fetch CelestChart-powered daily astrology forecasts and natal chart data for personalized horoscope responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends birth date, birth time, approximate birthplace coordinates, timezone, and a CelestChart API key to xp.broad-intelli.com. <br>
Mitigation: Install only if this data sharing is acceptable, use a dedicated CelestChart API key, and revoke the key if it is exposed. <br>
Risk: Casual horoscope prompts may trigger the skill and send the configured profile data. <br>
Mitigation: Review prompts and environment configuration before use, and avoid configuring sensitive birth details on shared systems. <br>


## Reference(s): <br>
- [CelestChart homepage](https://xp.broad-intelli.com) <br>
- [ClawHub skill page](https://clawhub.ai/maye08/celestchart-daily) <br>
- [Publisher profile](https://clawhub.ai/user/maye08) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON from the API call, then human-facing Markdown or text interpretation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, CELESTCHART_API_KEY for daily forecasts, and birth-date, birth-time, location, and timezone environment variables.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
