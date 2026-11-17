## Description:

blooming-elf（绽放精灵）—— 智能浇花浇水提醒与植物绿植花卉养护助手

This skill is ready for commercial/non-commercial use.

## Publisher:

[shirley1011](https://clawhub.ai/user/shirley1011)

### License/Terms of Use:

MIT-0

## Use Case:

External plant owners use this skill to set up plant profiles, receive watering and care reminders, log plant-care activity, and get concise troubleshooting guidance for houseplants, cut flowers, and multi-plant collections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores plant-care state, home-environment details, reminder settings, document IDs, and file paths in shared agent memory.

Mitigation: Use it only where this storage is acceptable, avoid entering unnecessary sensitive home details, and review stored configuration before sharing or reusing the agent environment.

Risk: Broad plant-care triggers could activate persistent data handling unintentionally.

Mitigation: Deploy with narrow, explicit plant-care invocation patterns and review trigger behavior before enabling it for shared or production agent sessions.

Risk: Reminder automations and weather-aware checks may run recurring plant-care workflows.

Mitigation: Require clear user confirmation before enabling automations or weather lookups, and keep recurring reminders scoped to the user's configured plant-care task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shirley1011/skills/blooming-elf-new)
- [ClawHub publisher profile](https://clawhub.ai/user/shirley1011)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown with concise plant-care guidance, tables, reminders, and document-update summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or append plant profile and care-log documents when the user has configured storage and confirmed the action.]

## Skill Version(s):

5.3.1 (source: server release evidence; artifact frontmatter reports 3.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
