## Description:

Daily Review Assistant helps an agent manually trigger daily reviews, query historical review notes, generate summary statistics, and export review content over selected time ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and knowledge-work users use this Chinese-language skill to manually run or inspect daily reflection workflows, including immediate reviews, history queries, statistics, and exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported review history may include conversation history, personal reflections, plans, and other sensitive notes.

Mitigation: Review exports before sharing them and handle daily review records as private data.

Risk: The skill may read or export daily review files under memory/evolution/daily-review/.

Mitigation: Install only when that file access is acceptable for the agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pagoda111king/skills/cloud-shrimp-daily-review)
- [Publisher profile](https://clawhub.ai/user/pagoda111king)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown or plain text review summaries, statistics, and exported review records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read from or export files under memory/evolution/daily-review/.]

## Skill Version(s):

0.1.0 (source: server release metadata, package.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
