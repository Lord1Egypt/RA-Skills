## Description: <br>
Discover China like a local with deep city-region coverage, practical route planning, food context, and execution-ready travel logistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to plan China trips, choose bases and routes, adapt plans by season and travel style, and handle practical logistics such as transport, payments, connectivity, documents, and pacing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trip preferences are stored locally in ~/china/memory.md and could include sensitive travel details if the user adds them. <br>
Mitigation: Avoid storing passport numbers, full booking confirmations, ticket numbers, account links, or other sensitive travel documents there; review or delete the file when saved context is no longer needed. <br>
Risk: Entry, permit, weather, transport, and health conditions can change after travel guidance is generated. <br>
Mitigation: Confirm current requirements and conditions before booking non-refundable travel or entering permit-sensitive, high-altitude, remote, or weather-exposed areas. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/china) <br>
- [Skill homepage](https://clawic.com/skills/china) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory template](artifact/memory-template.md) <br>
- [Entry and documents planning](artifact/entry-and-documents.md) <br>
- [Transport guide](artifact/transport.md) <br>
- [Emergencies and safety](artifact/emergencies.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown travel guidance with occasional shell commands and local memory updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local trip context under ~/china/memory.md when the user uses the skill's memory workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
