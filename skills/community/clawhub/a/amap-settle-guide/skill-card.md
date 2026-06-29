## Description: <br>
Amap Settle Guide helps users choose rental areas near a workplace by comparing commute time, nearby amenities, rental value, and listing links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongdongyue](https://clawhub.ai/user/dongdongyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users looking for housing near a workplace use this skill to compare commute options, neighborhood amenities, rent value, and concrete listing links before choosing where to live. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML map output may expose map-related environment values to users. <br>
Mitigation: Use only intentionally public, domain-restricted AMap browser keys, avoid sensitive server-side secrets for AMAP_JSAPI_KEY or AMAP_SECURITY_JS_CODE, and rotate any key that has already been embedded in generated HTML. <br>
Risk: Rental listings, commute estimates, and neighborhood scores may depend on live API or scraped data that can be incomplete or outdated. <br>
Mitigation: Review generated recommendations against source listing links and current map results before making housing decisions. <br>


## Reference(s): <br>
- [Server-resolved source repository](https://github.com/dongdongyue/amap-settle-guide) <br>
- [ClawHub skill page](https://clawhub.ai/dongdongyue/skills/amap-settle-guide) <br>
- [Publisher profile](https://clawhub.ai/user/dongdongyue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration] <br>
**Output Format:** [Markdown report with CSV files and optional HTML map output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAP_API_KEY; optional map output may use AMAP_JSAPI_KEY and AMAP_SECURITY_JS_CODE.] <br>

## Skill Version(s): <br>
0.1.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
