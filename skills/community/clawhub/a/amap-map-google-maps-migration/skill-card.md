## Description: <br>
Guides developers through migrating Google Maps Platform usage to AMap across Web Service APIs, JavaScript maps, and Android and iOS SDKs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbs-amap](https://clawhub.ai/user/lbs-amap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert Google Maps API, JavaScript map, and mobile SDK patterns into AMap equivalents with region-aware endpoints, parameter mappings, and code examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes public promotional API keys intended for development and testing, which may have quota, traceability, or production suitability limits. <br>
Mitigation: Verify the keys with AMap for testing and create dedicated restricted keys for production use. <br>
Risk: Some geolocation guidance involves sensitive device identifiers and a Non-Mainland endpoint documented as HTTP. <br>
Mitigation: Avoid collecting MAC or IMEI values unless strictly necessary, obtain user consent, minimize retained data, and prefer HTTPS-capable endpoints where supported. <br>
Risk: Migration mappings and sample code can become stale as Google Maps or AMap APIs change. <br>
Mitigation: Review generated changes against current provider documentation and test migrated API calls before deployment. <br>


## Reference(s): <br>
- [Skill listing](https://clawhub.ai/lbs-amap/amap-map-google-maps-migration) <br>
- [Web Service API parameter mapping](references/web-api-params.md) <br>
- [JavaScript API migration details](references/js-api-detail.md) <br>
- [Android and iOS SDK migration details](references/sdk-migration.md) <br>
- [AMap Overseas](https://mapsplatform.opnavi.com/) <br>
- [AMap Developer Console](https://lbs.amap.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with API mapping tables, code snippets, endpoint guidance, and migration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for developer region and development type before producing migration guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
