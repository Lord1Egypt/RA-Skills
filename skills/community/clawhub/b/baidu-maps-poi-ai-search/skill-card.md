## Description: <br>
Search and get details for POI (points of interest) using Baidu Maps API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archimondecy](https://clawhub.ai/user/archimondecy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Baidu Maps for places, restaurants, hotels, attractions, and other points of interest, then retrieve detailed POI information for a specified region. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, regions, and optional coordinates are sent to Baidu Maps. <br>
Mitigation: Use the skill only for searches that are appropriate to share with Baidu Maps, and avoid sensitive or precise home/work coordinates. <br>
Risk: The request body is printed to stderr, which can expose sensitive location details or an API key if the 'ak' JSON field is used. <br>
Mitigation: Set BAIDU_AK as an environment variable instead of passing an 'ak' field, and remove or redact request logging before sensitive use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archimondecy/baidu-maps-poi-ai-search) <br>
- [Baidu Maps multidimensional place search documentation](https://api.map.baidu.com/place/v3/multidimensional) <br>
- [Baidu Maps POI region API endpoint](https://api.map.baidu.com/api_place_pro/v1/region) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [JSON responses from the Baidu Maps API with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a BAIDU_AK credential.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
