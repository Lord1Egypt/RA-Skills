## Description: <br>
Croatia Weather gives agents command-line access to official DHMZ Croatian weather, forecast, warning, agriculture, maritime, hydrology, environment, climate, and European weather feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikolicjakov](https://clawhub.ai/user/nikolicjakov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Croatian weather questions, check official DHMZ forecasts and warnings, and retrieve agriculture, maritime, hydrology, environment, and climate summaries. Developers can configure a home station through documented environment variables. <br>

### Deployment Geography for Use: <br>
Croatia and Europe <br>

## Known Risks and Mitigations: <br>
Risk: Weather, maritime, flood, heat, fire, and health-related outputs may be incomplete, delayed, or unsuitable as the sole basis for safety-critical decisions. <br>
Mitigation: Treat outputs as informational, check timestamps and official DHMZ or emergency sources, and follow local safety guidance for severe conditions. <br>
Risk: The Python script makes outbound requests to public weather feed domains and reads optional home-station environment variables. <br>
Mitigation: Allow network access only to the documented public weather sources and configure DHMZ_HOME_* values with station names or aliases only. <br>


## Reference(s): <br>
- [ClawHub Croatia Weather listing](https://clawhub.ai/nikolicjakov/croatia-weather) <br>
- [README](README.md) <br>
- [DHMZ Quick Guide](references/quick-guide.md) <br>
- [DHMZ Station Cross-Reference](references/stations.md) <br>
- [DHMZ XML feed reference](https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text weather reports with Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and outbound access to public DHMZ feeds; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
