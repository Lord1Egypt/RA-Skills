## Description: <br>
Provides methods and tools for obtaining local host CST (China Standard Time). Invoke when user needs to get current CST time, convert time zones, or work with China Standard Time in scripts and applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuanpass](https://clawhub.ai/user/xuanpass) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to get the current China Standard Time, convert between CST and other time zones, and add CST-aware formatting or scheduling behavior to scripts and applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Online API examples may send requests to external services or expose API keys if copied directly into shell commands. <br>
Mitigation: Use the local run.sh or OS/runtime timezone examples for normal CST checks; only run online API examples intentionally, prefer HTTPS, and avoid placing real API keys directly in shell history. <br>
Risk: The CST abbreviation can be confused with other time zones in some contexts. <br>
Mitigation: Use the Asia/Shanghai IANA time zone ID or UTC+8 offset when precision matters. <br>


## Reference(s): <br>
- [World Time API Asia/Shanghai endpoint](http://worldtimeapi.org/api/timezone/Asia/Shanghai) <br>
- [TimezoneDB Asia/Shanghai example endpoint](http://api.timezonedb.com/v1/get-time-zone?key=YOUR_API_KEY&by=zone&zone=Asia/Shanghai) <br>
- [Google Maps Time Zone API example endpoint](https://maps.googleapis.com/maps/api/timezone/json?location=39.9042,116.4074&timestamp=1331161200&key=YOUR_API_KEY) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local shell commands, timezone identifiers, formatting patterns, and optional external API examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
