## Description:

订阅摘要(免费版) helps an agent use the feed CLI to fetch RSS items, scan unread entries, filter likely high-value content, and produce lightweight reading summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a lightweight RSS reading workflow: fetch feeds, inspect unread entries, filter high-value items, summarize selected content, and optionally mark entries as read.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an external feed CLI that reads from and writes to the user's local feed database.

Mitigation: Install the feed CLI only from a trusted source and ask the agent to keep actions read-only unless you explicitly want database changes.

Risk: Commands such as adding subscriptions or marking entries as read can change local feed state.

Mitigation: Require explicit confirmation before running state-changing commands such as feed add or feed update entries --read.

## Reference(s):

- [Detailed feed digest examples](references/detail.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/feed-digest-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with shell command snippets, Python examples, and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include feed CLI commands and summarized RSS entry content.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
