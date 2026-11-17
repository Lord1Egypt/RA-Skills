## Description:

AI CityWalk 剧本杀 — 基于高德地图的城市解谜探索 Skill，AI 作为剧本杀主持人，生成沉浸式剧本并串联真实地点.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunfj](https://clawhub.ai/user/sunfj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create and play location-based CityWalk mystery routes in a chosen city, with AI-generated story chapters, real POIs, walking routes, map links, GPS check-ins, photo validation, answers, scoring, and completion summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles precise user location and photo data through online services.

Mitigation: Use only after explicit user consent, provide a clear privacy notice, and avoid deployment contexts where location or image sharing is not acceptable.

Risk: Local session data is shared through a broad session file behavior that may be unsuitable for shared or multi-user agent environments.

Mitigation: Prefer per-user session storage with restrictive file permissions, or isolate the agent runtime per user before enabling the skill.

Risk: The story-create flow can read and upload a local JSON file path supplied to the script.

Mitigation: Do not pass arbitrary local JSON files; validate story payload schemas and restrict allowed input locations before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunfj/skills/amap-citywalk-mystery)
- [README](README.md)
- [Workflow diagram](assets/workflow.svg)
- [Architecture diagram](assets/architecture.svg)
- [Theme overview](assets/themes.svg)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown conversation output with JSON service responses, map links, route summaries, story chapters, check-in prompts, and completion scorecards.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user consent for location sharing and photo submission; generated routes and tasks depend on external map, weather, location, and story services.]

## Skill Version(s):

0.1.10 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
