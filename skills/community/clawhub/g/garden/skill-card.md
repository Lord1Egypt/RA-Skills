## Description: <br>
Track your entire garden with structured memory for plants, zones, tasks, harvests, and climate-aware planning that compounds over seasons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to maintain a local garden notebook for plant records, garden zones, activity logs, harvest tracking, climate-aware planning, and problem diagnosis across seasons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains persistent local garden notes and may save garden information from broad conversational triggers. <br>
Mitigation: Use it only when a local garden notebook is desired, ask the agent to preview entries before saving, and periodically review ~/garden for records that should not be retained. <br>
Risk: The skill can optionally write an integration note to workspace memory. <br>
Mitigation: Only allow workspace memory updates after explicit user consent, and review the proposed memory entry before it is saved. <br>


## Reference(s): <br>
- [Garden ClawHub skill page](https://clawhub.ai/ivangdavila/garden) <br>
- [Garden homepage](https://clawic.com/skills/garden) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory template](artifact/memory-template.md) <br>
- [Plant and activity tracking](artifact/tracking.md) <br>
- [Climate configuration](artifact/climate-setup.md) <br>
- [Problem diagnosis](artifact/diagnostics.md) <br>
- [Rotation and seasonal planning](artifact/planning.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance and local Markdown garden records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local garden notes under ~/garden/ when the user wants persistent tracking.] <br>

## Skill Version(s): <br>
1.1.6 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
