## Description:

Generate structured daily standup reports by analyzing git commits, pull request activity, issue trackers, and project context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and team leads use this skill to prepare daily standup or async status updates from recent repository, pull request, issue, branch, and work-in-progress activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read recent repository, pull request, issue-tracker, branch, and uncommitted work activity that can contain private project or team information.

Mitigation: Run it only in intended repositories and issue trackers, avoid broad team mode unless authorized, and review generated standup content before sharing.

Risk: The generated standup may summarize development activity inaccurately or include context that is not appropriate for the target audience.

Mitigation: Treat the report as a draft and verify the yesterday, today, and blockers sections before posting or presenting it.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown standup report by default, with optional verbose, Slack-style, or JSON formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include yesterday, today, and blockers sections, with optional activity metrics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
