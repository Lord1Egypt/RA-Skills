## Description:

Fetches live ClawHub publisher metrics for a specified handle, including aggregate author stats and per-skill downloads, installs, stars, comments, and coverage notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and marketplace analysts use this skill to fetch current ClawHub publisher performance metrics and produce a concise author and per-skill report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to public ClawHub-related sites, which can fail, rate-limit, or disclose the queried publisher handle to those sites.

Mitigation: Install only when those public requests are acceptable, and keep --limit and --workers values reasonable.

Risk: Markdown reports may contain live public data that is partial, stale, or unavailable for some skill-page fields.

Mitigation: Prefer JSON output for automated reuse and keep source limitation notes visible in user-facing summaries.

## Reference(s):

- [ClawHub Publisher Stats listing](https://clawhub.ai/harrylabsj/skills/clawhub-publisher-stats)
- [Source descriptions](references/sources.md)
- [Top ClawHub Skills](https://topclawhubskills.com/)
- [ClawHub publisher profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown report or JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live public data; optional per-skill page fetching adds install and comment counts when available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
