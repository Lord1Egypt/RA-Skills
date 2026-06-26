## Description: <br>
FlyClaw is a Python flight-search skill that aggregates public sources for flight status, schedules, prices, live positions, nonstop filtering, round trips, cabin class, and city or IATA queries without requiring user login or API keys. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[ai4mse](https://clawhub.ai/user/ai4mse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query flight status, schedules, prices, live aircraft position data, nonstop or connecting routes, round trips, cabin class, and city-level airport expansion from a command-line Python workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default Fliggy integration may create a persistent device identifier and send device/context metadata during searches. <br>
Mitigation: Review before installing, run in an isolated Python environment, pin dependencies where possible, and disable the Fliggy source in config.yaml unless this metadata sharing is acceptable. <br>
Risk: The skill queries external flight-data and fare services, so searches may disclose route, date, passenger, cabin, or flight-number details to those services. <br>
Mitigation: Use the skill only for flight queries that are acceptable to send to configured external sources, and review enabled sources in config.yaml before use. <br>
Risk: Fare, availability, delay, aircraft, and live-position data are sourced from multiple third-party services and may be incomplete, stale, or inconsistent. <br>
Mitigation: Treat results as reference data, compare sources when possible, and confirm itinerary details with the airline or booking provider before making travel decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ai4mse/flyclaw) <br>
- [Publisher profile](https://clawhub.ai/user/ai4mse) <br>
- [README_EN.md](README_EN.md) <br>
- [SKILL_EN.md](SKILL_EN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Guidance, Configuration] <br>
**Output Format:** [JSON records by default, with optional table text and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight-price records include source-specific fields such as currency, route segments, layover details, and optional return-trip segments.] <br>

## Skill Version(s): <br>
0.4.4 (source: evidence.release.version, SKILL.md frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
