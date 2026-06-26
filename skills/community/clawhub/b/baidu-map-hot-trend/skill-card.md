## Description: <br>
Registers a Baidu Maps skill for lightweight access to public Baidu Maps POI, route, and coordinate information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to summarize public Baidu Maps POI details, compare transit and driving routes, and annotate BD-09 coordinates for lightweight, manually triggered workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Addresses, routes, and precise travel details may be location data shared with Baidu Maps. <br>
Mitigation: Avoid entering sensitive home, workplace, or precise travel details unless sharing them with Baidu Maps is acceptable. <br>
Risk: Bulk scraping or unattended collection could violate platform expectations or trigger access controls. <br>
Mitigation: Use the skill only for manual, lightweight lookups with rate limiting and human-triggered collection. <br>
Risk: BD-09 coordinates can differ from GCJ-02 or WGS-84 coordinates and may cause location errors if mixed without conversion notes. <br>
Mitigation: Label coordinate-system sources clearly and include conversion caveats when reporting or annotating coordinates. <br>


## Reference(s): <br>
- [Baidu Maps](https://map.baidu.com/) <br>
- [Baidu Maps Directions](https://map.baidu.com/direction) <br>
- [Baidu Maps Search](https://map.baidu.com/search) <br>
- [ClawHub Skill Page](https://clawhub.ai/CodeKungfu/baidu-map-hot-trend) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown or structured text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include POI fields, route details, source links, report timestamps, and coordinate-system notes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
