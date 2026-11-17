## Description:

Creates and maintains Bazi-based AI personas for charting, ongoing persona updates, dynamic time-flow analysis, and lunar-calendar queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojxiao2021](https://clawhub.ai/user/xiaojxiao2021)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create, query, update, and converse with file-backed Bazi personas, including dynamic Bazi flow and almanac lookups. It provides interpretive guidance and should not replace professional medical, legal, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad file-backed persona management can affect local persona data, including deletion.

Mitigation: Use a trusted, contained persona directory and review delete actions before execution.

Risk: Weak path controls make arbitrary or unverified base_dir values risky.

Mitigation: Avoid arbitrary base_dir values and use only verified persona storage paths.

Risk: Imported private or third-party chat logs may be stored and reused as persistent persona memory.

Mitigation: Import chat logs only when the user is comfortable with persistent storage and reuse of that content.

Risk: The development command uses unpinned npx tooling.

Mitigation: Avoid the npx development command unless the tooling has been pinned and verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaojxiao2021/skills/bazi-persona)
- [ClawHub Package Homepage](https://clawhub.ai/xiaojxiao2021/bazi-persona)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses, with JSON data for persona records and Bazi/calendar tool results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [File-backed persona data may be read, updated, imported, or deleted through configured persona directories.]

## Skill Version(s):

0.3.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
