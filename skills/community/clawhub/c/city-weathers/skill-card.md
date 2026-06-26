## Description: <br>
Provides structured weather data including temperature, humidity, wind, precipitation, and clothing advice for specified cities and dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shilingong](https://clawhub.ai/user/shilingong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to answer city weather questions by extracting a city and date, then returning structured weather conditions and practical advice. It is useful for weather lookup workflows that need machine-readable output for today, tomorrow, the day after tomorrow, or a seven-day range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather responses may be simulated or depend on the configured weather provider. <br>
Mitigation: Confirm whether the deployment uses a real weather provider before relying on results for decisions. <br>
Risk: City and date queries can disclose location interests to a connected provider. <br>
Mitigation: Avoid sending locations considered sensitive unless the configured provider is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shilingong/city-weathers) <br>
- [API integration notes](artifact/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a city; date defaults to today when omitted. Weather values may come from a configured provider or simulated data depending on deployment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
