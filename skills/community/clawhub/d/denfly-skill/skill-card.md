## Description: <br>
Get current weather and forecasts with no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[denfly618](https://clawhub.ai/user/denfly618) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to fetch current weather summaries and forecasts with curl. It supports wttr.in for quick text or PNG output and Open-Meteo for JSON weather data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries may disclose requested locations to public weather services. <br>
Mitigation: Use coarse locations instead of exact home or work coordinates when privacy matters. <br>
Risk: The skill depends on public weather services for availability and forecast accuracy. <br>
Mitigation: Verify weather information with an authoritative source before using it for safety-critical decisions. <br>
Risk: The listing name differs from the artifact's weather skill name, which can make publisher review less obvious. <br>
Mitigation: Confirm the ClawHub publisher and listing before installing when identity matters. <br>


## Reference(s): <br>
- [wttr.in Help](https://wttr.in/:help) <br>
- [Open-Meteo Forecast API Documentation](https://open-meteo.com/en/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text, JSON] <br>
**Output Format:** [Markdown with bash code blocks and example weather service responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for command examples; weather services may return text summaries, JSON, or PNG images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
