## Description: <br>
Track Claude.ai token usage and session costs by scraping the Claude.ai usage dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals or teams who track Claude.ai usage use this skill to log dashboard snapshots, check current limits and spend, and project near-term usage exhaustion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill works with Claude.ai usage, spend, and balance details that may be sensitive. <br>
Mitigation: Share only the values needed for the usage question, avoid including credentials or full billing records, and keep the local snapshot state in an appropriate user-controlled location. <br>
Risk: Usage projections can be stale or low confidence when snapshot history is sparse. <br>
Mitigation: Confirm current Claude.ai dashboard values before billing or capacity decisions and clearly caveat projections when there are fewer than several representative snapshots. <br>
Risk: The workflow depends on local Python commands and disclosed command use. <br>
Mitigation: Review commands before running them, confirm the target workspace and state file, and install only when the publisher and workflow are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/claude-usage-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/nissan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and concise status or projection summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference usage percentages, reset timers, spend, balance, and confidence caveats when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
