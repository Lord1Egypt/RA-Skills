## Description: <br>
Discover Australia like a local with deep city-region coverage, practical route planning, food context, and execution-ready travel logistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to plan Australia travel with city and regional guidance, route pacing, seasonality, safety, cost, food, accommodation, and transport considerations. It helps agents produce practical itineraries, tradeoff guidance, checklists, and locally stored trip context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist trip preferences and booking context in ~/australia/memory.md. <br>
Mitigation: Do not store passport numbers, payment details, sensitive booking codes, or other sensitive personal information; edit or delete the memory file when saved context is no longer wanted. <br>
Risk: Travel requirements, biosecurity rules, weather, marine conditions, park closures, and emergency conditions can change after guidance is generated. <br>
Mitigation: Verify current official requirements and local safety advisories before booking, driving, hiking, visiting parks, or entering marine and remote areas. <br>


## Reference(s): <br>
- [Australia Skill Page](https://clawhub.ai/ivangdavila/australia) <br>
- [Australia Skill Homepage](https://clawic.com/skills/australia) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Setup Guide](artifact/setup.md) <br>
- [Australia Trip Memory Template](artifact/memory-template.md) <br>
- [Entry and Biosecurity Planning](artifact/entry-and-biosecurity.md) <br>
- [Emergencies and Safety](artifact/emergencies.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown travel guidance with occasional shell commands for local memory setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local trip context in ~/australia/memory.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
