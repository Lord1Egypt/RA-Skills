## Description: <br>
AI image geolocation via visual analysis, with no GPS or EXIF metadata required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samtin0x](https://clawhub.ai/user/samtin0x) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and investigators use this skill to submit local image files to GeoInfer and receive location predictions with coordinates and confidence scores. It supports OSINT, digital forensics, investigative journalism, and security workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local images are sent to an external GeoInfer API for geolocation analysis. <br>
Mitigation: Use only images approved for external processing, avoid private or confidential images unless authorized, and keep GEOINFER_API_KEY in the environment rather than pasting it into chat. <br>


## Reference(s): <br>
- [GeoInfer API key setup](https://app.geoinfer.com/en/api) <br>
- [ClawHub skill page](https://clawhub.ai/samtin0x/geoinfer-image-geolocation) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON responses from GeoInfer API commands, with Markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEOINFER_API_KEY; prediction commands accept a local image path, optional model_id, and optional top_n value from 1 to 15.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
