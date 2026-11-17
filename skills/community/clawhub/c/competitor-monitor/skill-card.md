## Description:

Monitors competitor or other target web pages over time, compares each crawl with a saved snapshot, and reports changes in prices, copy, listings, or page structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

External users, operators, and developers can use this skill to monitor approved public pages for business-relevant changes such as price moves, new listings, content updates, and compliance changes. It is suited to recurring monitoring workflows where the agent should create or update snapshots and produce concise change reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs from the runner, which may expose internal services or cloud metadata endpoints if unrestricted.

Mitigation: Run it only in restricted environments and limit monitoring targets to approved public sites.

Risk: The main snapshot workflow may bypass the promised robots.txt check.

Mitigation: Review target authorization before use and prefer workflows that enforce robots.txt, site terms, and rate limits.

Risk: Snapshot and learned pattern files can retain local business data.

Mitigation: Use dedicated output and state directories, review retained files, and clean them up according to data handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/competitor-monitor)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON snapshot files, and plain-text change reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local snapshot, diff, and learned pattern files when invoked by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
