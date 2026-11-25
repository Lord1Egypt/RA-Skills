## Description:

Searches Douyin for current videos and image posts, trending topics, creator posts, work details, and comments, returning structured data for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content teams, marketers, analysts, and customer support teams use this skill to find current public Douyin content, inspect creator and post activity, and summarize trends or comment themes. It can support topic research, competitor monitoring, and sentiment or demand analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword-based account discovery may extend beyond a request to find Douyin content.

Mitigation: Use creator search only when the user explicitly asks to find accounts, and keep the search scope tied to that request.

Risk: Search terms and supplied links or IDs are sent to the external Guaikei service; returned data may also be affected by task-reuse windows.

Mitigation: Tell the user what query or identifier will be sent, submit only the public content they requested, and check result timestamps or rerun when freshness matters.

Risk: The benign scanner verdict has medium confidence and coverage is incomplete.

Mitigation: Treat the verdict as limited assurance, review the release before installation, and keep the API token confined to the intended runtime.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/douyin-realtime-searchs)
- [Guaikei service](https://www.guaikei.com)
- [Output contract](references/contract.md)
- [Command options](references/options.md)
- [Errors and limits](references/errors.md)
- [Comment demand analysis](references/demand-mining.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance, Shell commands]

**Output Format:** [Structured JSON results with concise text or Markdown analysis and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can contain public post, creator, and comment data for user-requested searches.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
