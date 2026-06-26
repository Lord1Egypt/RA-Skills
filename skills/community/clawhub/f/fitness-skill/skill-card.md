## Description: <br>
Fitness & Workout Manager helps OpenClaw users create workout plans, log live or post-workout exercise entries, view progress summaries, export reports, and optionally sync plans or logs to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PH13917403910](https://clawhub.ai/user/PH13917403910) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to manage personal fitness plans, record workout sessions, review training summaries, and export reports. Users who trust their Feishu workspace can also sync plans and recent logs to a Feishu document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores workout plans, notes, feelings, and history in local OpenClaw workspace files. <br>
Mitigation: Use it only in trusted workspaces and treat generated exports and local data files as personal fitness data. <br>
Risk: When Feishu sync is configured, personal fitness data can be copied to a Feishu document. <br>
Mitigation: Enable sync only for a trusted Feishu bot and document, and review document sharing permissions before syncing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PH13917403910/fitness-skill) <br>
- [Fitness data schemas](references/schemas.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON-backed plan, log, active-session, and export files; Feishu sync is optional when configured.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata, SKILL.md frontmatter, manifest.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
