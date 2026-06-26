## Description: <br>
Query weather via Amap (高德) Weather API for China locations, including real-time conditions and 4-day forecasts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyatt88](https://clawhub.ai/user/wyatt88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up current weather or four-day forecasts for Chinese cities or Amap adcodes and format the results for users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Amap API key exposure or over-permissioning. <br>
Mitigation: Use a dedicated restricted Amap Web Services API key and prefer AMAP_API_KEY over passing the key on the command line. <br>
Risk: Weather requests send the selected city or adcode and API key to Amap and may count against the account quota. <br>
Mitigation: Use the skill only for intended China weather lookups and monitor Amap API quota usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wyatt88/amap-weather) <br>
- [Amap Weather API reference](references/api-docs.md) <br>
- [Amap Web Services](https://lbs.amap.com) <br>
- [Amap adcode download](https://lbs.amap.com/api/webservice/download) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance plus plain-text or JSON weather output from the bundled Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAP_API_KEY; sends the selected city or adcode and API key to Amap Weather API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
