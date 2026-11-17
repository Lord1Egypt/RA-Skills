## Description:

Search Feishu contacts by name/pinyin/department. Use when you need to find a person's open_id, email, or department info before sending messages or emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyun94](https://clawhub.ai/user/guyun94)

### License/Terms of Use:


## Use Case:

Employees, developers, and agents use this skill to locate Feishu users, departments, open IDs, and email addresses before sending messages, emails, or department-wide communications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Organization contact data may be cached locally without sufficient privacy or retention controls.

Mitigation: Install only with approved Feishu directory read access, restrict ~/.openclaw permissions, treat the cache as sensitive, and periodically delete stale cache data.

Risk: Bulk department lookups can expose many employees' contact identifiers.

Mitigation: Use department member listing only when necessary and approved, and avoid unnecessary redistribution of returned contact data.

Risk: Cached contact data can become stale.

Mitigation: Run sync before important lookups and refresh or delete stale cache data according to organizational policy.

## Reference(s):

- [Feishu Open APIs](https://open.feishu.cn/open-apis)
- [ClawHub skill release](https://clawhub.ai/guyun94/skills/feishu-contacts)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and plain-text CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local Feishu directory cache for search commands; the get command makes a live Feishu API call.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
