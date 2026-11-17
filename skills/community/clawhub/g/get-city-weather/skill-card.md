## Description:

Fetches weather information for a specified city in China, including temperature, conditions, wind, air quality, and lifestyle suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiweiweilai](https://clawhub.ai/user/yiweiweilai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch current weather for cities in China and save a local report with temperature, weather conditions, wind, AQI, and lifestyle suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's Juhe weather API key over unencrypted HTTP.

Mitigation: Use a throwaway or tightly limited Juhe weather API key and prefer a version that uses HTTPS.

Risk: The skill reads API keys from environment variables or a local .env file.

Mitigation: Avoid production credentials and remove local .env secrets before sharing or republishing the artifact.

Risk: Dependencies are not pinned in the artifact instructions.

Mitigation: Install dependencies in an isolated environment and prefer a release with pinned dependency versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiweiweilai/skills/get-city-weather)
- [Juhe Simple Weather API endpoint](http://apis.juhe.cn/simpleWeather/query)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration]

**Output Format:** [Plain text weather report and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a city name and a Juhe weather API key; writes reports under output/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
