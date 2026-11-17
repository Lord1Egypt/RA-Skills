## Description:

Searches public Douyin videos, posts, trends, creator feeds, and comments, returning structured data for agent-written briefings and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, social-media teams, and content planners use this skill to search public Douyin posts, trends, creator posts, and comments, then summarize results for topic research, competitor reviews, and sentiment or demand analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send user-provided keywords or Douyin links to the third-party GUAIKEI API.

Mitigation: Submit only query and link data approved for third-party processing, and confirm the external-data scope before use.

Risk: GUAIKEI_API_TOKEN is required to access the data API.

Mitigation: Keep the token private; on authentication errors, stop and ask the user to check configuration instead of retrying.

Risk: The security scan had medium confidence and partial coverage; some executable files and environment permissions were not fully assessed.

Mitigation: Review the skill and its executable files and permissions before installation, accounting for the incomplete scan coverage.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-news-brief)
- [GUAIKEI service and token setup](https://www.guaikei.com)
- [Command options](references/options.md)
- [Comment demand mining guide](references/demand-mining.md)
- [Release changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown]

**Output Format:** [Structured JSON from the command-line tools; agent-written summaries, topic clusters, and analysis reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include time-limited media and share URLs; query limits depend on the API plan.]

## Skill Version(s):

1.4.2 (source: server release metadata, SKILL.md, package.json, changelog released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
