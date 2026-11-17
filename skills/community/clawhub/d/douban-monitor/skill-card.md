## Description:

Douban Monitor helps an agent track newly qualifying high-rated Douban films and TV series, enrich results with TMDB data, and produce local reports plus a static viewing page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juryory](https://clawhub.ai/user/juryory)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media-tracking users use this skill to run a local or scheduled monitor for Douban film and TV entries that cross rating and popularity thresholds. The agent can report new qualifying titles, keep watchlist state, and generate reviewable report and web artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Douban and TMDB and writes monitoring outputs to local files.

Mitigation: Install only when this network access and local file generation are acceptable, and review generated data before sharing it.

Risk: The default configuration can automatically commit and push generated monitoring data to the configured Git remote.

Mitigation: Set auto_git_push = false or DOUBAN_MONITOR_NO_PUSH=1 before first run unless remote publication is intentional.

Risk: TMDB credentials may be exposed to an unintended endpoint if tmdb_base_url is changed.

Mitigation: Keep TMDB credentials limited and leave tmdb_base_url pointed at the official TMDB API unless the endpoint is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juryory/skills/douban-monitor)
- [Implementation Notes](references/IMPLEMENTATION_NOTES.md)
- [Example configuration](references/config.example.toml)
- [Example library data](references/library.example.json)
- [Example state data](references/state.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Configuration]

**Output Format:** [Concise agent status text, Markdown reports, JSON data files, and static HTML pages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local monitoring artifacts under data/, reports/, and detail/; when explicitly left enabled, auto_git_push can commit and push generated files to the configured Git remote.]

## Skill Version(s):

1.1.0 (source: server release evidence, changelog dated 2026-07-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
