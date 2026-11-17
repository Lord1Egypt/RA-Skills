## Description:

Fetches Bilibili popular-video rankings, summarizes basic trend metrics, and can export the results as JSON or CSV.

This skill is for research and development only.

## Publisher:

[mkt-agents](https://clawhub.ai/user/mkt-agents)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content analysts can use this skill to fetch current Bilibili trending-video data, inspect ranking metrics, generate a simple text summary, and save local JSON or CSV exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Bilibili and can write local export files.

Mitigation: Run it only when that network access is acceptable, choose explicit output paths, and review generated files before reuse.

Risk: CSV exports may be unsafe to open directly in spreadsheet applications.

Mitigation: Inspect CSV output as text first or sanitize fields before opening it in a spreadsheet.

Risk: The release advertises AI summaries, scheduling, and push delivery beyond the reviewed script behavior.

Mitigation: Treat those capabilities as unavailable unless a separate implementation is provided and reviewed.

Risk: The package metadata includes an unnecessary npm python dependency.

Mitigation: Prefer a pinned ClawHub installer version and review or remove that dependency before npm-based installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkt-agents/skills/bilibili-hot-daily)
- [Bilibili popular API endpoint](https://api.bilibili.com/x/web-interface/popular)
- [Bilibili website](https://www.bilibili.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON or CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; fetches public Bilibili data over HTTPS and writes export files only when an output path is supplied.]

## Skill Version(s):

2.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
