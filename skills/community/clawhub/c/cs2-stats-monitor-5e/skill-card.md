## Description:

Query and monitor 5E CS2 player stats and match performance in real time with customizable player lists and detailed match analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ddeellttaa](https://clawhub.ai/user/ddeellttaa)

### License/Terms of Use:

MIT

## Use Case:

Developers, players, and analysts use this skill to query recent 5E CS2 match data for selected players, monitor for newly completed matches, and generate concise performance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background monitoring can keep polling 5E services without clear runtime limits.

Mitigation: Use --once for one-time lookups, run monitoring only for explicit player lists, and stop the tmux session when finished.

Risk: Installing dependencies directly into a shared Python environment can affect other projects.

Mitigation: Install aiohttp in an isolated environment and consider pinning the dependency before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ddeellttaa/skills/cs2-stats-monitor-5e)
- [5E player search API](https://arena.5eplay.com/api/search/player/1/16)
- [5E player match data API](https://gate.5eplay.com/crane/http/api/data/player_match?uuid={uuid})
- [5E match detail API](https://gate.5eplay.com/crane/http/api/data/match/{match_id})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one-time reports or continuous monitoring output; writes local monitor state when used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
