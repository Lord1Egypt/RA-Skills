## Description: <br>
Address Extractor helps agents extract, clean, standardize, and geocode Chinese address information from unstructured text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouyouwen](https://clawhub.ai/user/zhouyouwen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to turn customer records, order text, document notes, and logistics data into structured address components and optional map coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real addresses can be personal or sensitive data, and optional geocoding sends address queries to AMap. <br>
Mitigation: Run local parsing without an AMap API key when external geocoding is not required, and enable geocoding only with permission to send the address data to AMap. <br>
Risk: Parsed or geocoded address results may be unsuitable for critical routing, delivery, or customer-record decisions without review. <br>
Mitigation: Validate important standardized addresses and coordinate results before using them in production workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhouyouwen/address-extractor) <br>
- [Address Extraction Reference](references/README.md) <br>
- [Configuration Template](references/config_template.json) <br>
- [Amap Open Platform](https://lbs.amap.com/) <br>
- [Amap Geocoding API](https://restapi.amap.com/v3/geocode/geo) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Code, API Calls, Configuration] <br>
**Output Format:** [Python dictionary or JSON-like structured address data with optional coordinate fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates are returned only when an Amap API key is configured and geocoding succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
