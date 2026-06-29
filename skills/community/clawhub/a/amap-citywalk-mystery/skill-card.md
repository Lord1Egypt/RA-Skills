## Description: <br>
AI CityWalk 剧本杀 — 基于高德地图的城市解谜探索 Skill，AI 作为剧本杀主持人，生成沉浸式剧本并串联真实地点. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunfj](https://clawhub.ai/user/sunfj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill through an agent to plan and play an outdoor city-walk mystery game with real POIs, walking routes, map links, GPS check-ins, photo verification, answer checks, and a completion scorecard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects precise GPS location, on-site photos, answers, and game progress through a hosted service without enough privacy, retention, or safety-control detail in the evidence. <br>
Mitigation: Use only after users knowingly agree to share this data, ask the publisher for privacy, retention, deletion, and access-control details, and avoid photographing bystanders or private areas. <br>
Risk: The skill stores the most recent location session identifier in scripts/.location-session. <br>
Mitigation: Remove scripts/.location-session after use when location sessions should not remain on disk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunfj/skills/amap-citywalk-mystery) <br>
- [Publisher profile](https://clawhub.ai/user/sunfj) <br>
- [Amap Web Service API endpoint](https://restapi.amap.com/v3) <br>
- [CityWalk hosted service](https://www.701study.com/app/citywalk-service) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, map/check-in links, route summaries, story chapters, and scorecards] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a multimodal model for photo checks and uses hosted services for location, POI, route, question, and story state operations.] <br>

## Skill Version(s): <br>
0.1.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
