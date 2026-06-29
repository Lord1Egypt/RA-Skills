## Description: <br>
城市踏勘官 CityScout turns a city area, task goal, and time budget into an actionable field survey route, observation checklist, risk notes, photo guidance, and a short reporting summary for urban renewal, site selection, tourism route review, street vitality assessment, and related place-based work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kue0000](https://clawhub.ai/user/kue0000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, planners, consultants, researchers, and field teams use this skill to convert location-based urban tasks into practical site-visit plans. It is intended for fieldwork planning around urban renewal, commercial location scouting, cultural tourism routes, street vitality, community services, and night safety checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location and task details may be sent to Amap or another map provider when API access is used. <br>
Mitigation: Share only appropriate fieldwork details with the map provider and account for the provider's data handling terms before use. <br>
Risk: Generated routes or POI evidence may be incomplete, stale, or mock data when live API access is unavailable. <br>
Mitigation: Verify routes, stops, weather, and POI details with authoritative map data before fieldwork, submission, or business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kue0000/city-scout-amap-skill) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Example prompt](artifact/examples/example_prompt.md) <br>
- [Example output](artifact/examples/example_output.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Analysis, API Calls] <br>
**Output Format:** [Markdown with structured sections and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ordered route stops, observation checklists, risk and opportunity notes, photo guidance, a three-sentence summary, and data that must be verified.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
