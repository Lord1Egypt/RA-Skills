## Description: <br>
Plans driving routes in China and helps drivers reduce highway tolls by considering local ring-road free-passage policies, vehicle plate rules, and Amap navigation links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liumeixin](https://clawhub.ai/user/liumeixin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External drivers or agents assisting them use this skill to plan China highway trips, estimate tolls, check destination driving restrictions, and identify route combinations that may reduce toll costs. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Route planning may send origins, destinations, coordinates, and waypoints to Amap or search services. <br>
Mitigation: Use the skill only when this location-data sharing is acceptable, and avoid entering sensitive trips or addresses. <br>
Risk: Hardcoded map API keys can expose credentials. <br>
Mitigation: Configure the Amap key with the AMAP_WEBSERVICE_KEY environment variable instead of placing it directly in skill text or code. <br>
Risk: Cached toll-free highway and driving-restriction policies may become stale. <br>
Mitigation: Refresh policy data when it is older than one month and verify important toll or restriction results against official sources before travel. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liumeixin/china-highway-route) <br>
- [Amap Geocoding API](https://restapi.amap.com/v3/geocode/geo?address={address}&key={API_KEY}) <br>
- [Amap Driving Direction API](https://restapi.amap.com/v3/direction/driving?origin={origin}&destination={destination}&key={API_KEY}) <br>
- [Amap Driving Direction API with Waypoints](https://restapi.amap.com/v3/direction/driving?origin={origin}&destination={destination}&waypoints={waypoints}&key={API_KEY}) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls] <br>
**Output Format:** [Markdown route plan with route segments, toll estimates, restriction notices, savings comparisons, and Amap navigation links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on current policy searches and cached highway-policy data; results should be checked against official sources before travel.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
