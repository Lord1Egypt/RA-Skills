## Description:

基于高德地图开放平台的 AI 盲人无障碍出行 Skill，支持周边搜索、无障碍设施查询、步行与公交路线规划、当前定位与一键紧急求助，输出面向语音播报优化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wukongmazi](https://clawhub.ai/user/wukongmazi)

### License/Terms of Use:

MIT-0

## Use Case:

External users who are blind, have low vision, or need mobility support use this skill to request location-aware navigation, nearby facility search, transit summaries, accessibility-oriented searches, and SOS location messages through voice-first responses.

### Deployment Geography for Use:

Global, subject to Gaode Maps service coverage and local requirements for location sharing and emergency assistance.

## Known Risks and Mitigations:

Risk: The skill handles precise user location and sends coordinates to Gaode services for navigation.

Mitigation: Require clear user consent for location use and disclose that Gaode receives coordinates before live navigation or search calls.

Risk: SOS behavior can disclose precise location with weak user control.

Mitigation: Require explicit consent before SOS or location disclosure unless a separately reviewed emergency policy permits immediate sharing.

Risk: Accessibility-priority routing claims may exceed implemented route-planning behavior.

Mitigation: Describe routes as suggested navigation from available map data and avoid claiming guaranteed accessible paths unless that routing is implemented and tested.

Risk: Raw API failures or emergency-tool import problems could affect safety-critical use.

Mitigation: Test emergency tool imports before release and sanitize API error messages shown or spoken to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wukongmazi/skills/blind-nav-gaode)
- [ClawHub publisher profile](https://clawhub.ai/user/wukongmazi)
- [Gaode Web Services API endpoint](https://restapi.amap.com/v3)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON strings containing voice_friendly, voice_summary, or voice_alert text for TTS-oriented agent responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GAODE_API_KEY and user location inputs for live navigation results.]

## Skill Version(s):

1.0.2 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
