## Description: <br>
Fetches weather information for a specified city, including temperature, conditions, wind, air quality, and practical daily suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiweiweilai](https://clawhub.ai/user/yiweiweilai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current weather for Chinese cities and save a local weather report with temperature, conditions, wind, AQI, and lifestyle suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the city name and a dedicated Juhe weather API key to apis.juhe.cn using the declared HTTP endpoint. <br>
Mitigation: Use a dedicated API key, avoid reusing sensitive secrets, and review network exposure before running the skill. <br>
Risk: The skill writes weather reports to a local output directory. <br>
Mitigation: Review generated report files before sharing or committing workspace contents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yiweiweilai/get-city-weather) <br>
- [Juhe simpleWeather query API endpoint](http://apis.juhe.cn/simpleWeather/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration guidance] <br>
**Output Format:** [Plain text weather report and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a UTF-8 .txt report under the skill output directory; requires a city name and a Juhe weather API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
