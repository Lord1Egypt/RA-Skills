## Description: <br>
Aggregates daily work updates from connected tools when users ask for a standup, morning report, or work-status summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and developers use this skill to produce a concise daily standup summary from connected GitLab, GitHub, Jira, email, task, and calendar accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can aggregate sensitive information from connected work accounts when invoked. <br>
Mitigation: Connect only the accounts intended for standup summaries, use explicit standup or daily-report prompts, and review the generated summary before sharing. <br>
Risk: The required MorphixAI API key and linked service accounts increase the access surface for work data. <br>
Mitigation: Store MORPHIXAI_API_KEY securely, avoid linking unnecessary services, and unlink accounts that should not be included in summaries. <br>
Risk: Unavailable or unlinked services can make the daily summary incomplete. <br>
Mitigation: Treat skipped or failed sections as incomplete and verify critical work items directly in the source systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paul-leo/daily-standup) <br>
- [Morphix API keys](https://morphix.app/api-keys) <br>
- [Morphix connections](https://morphix.app/connections) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown list summary in Chinese] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output is capped by the skill instructions at 500 Chinese characters and omits sections for unconnected data sources.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
