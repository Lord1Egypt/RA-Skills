## Description:

Chinese-language Dota 2 coaching skill that helps agents provide hero win-rate context, item builds, matchup notes, skill data, talent trees, and gameplay guidance from bundled game data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangjian1412](https://clawhub.ai/user/yangjian1412)

### License/Terms of Use:

MIT-0

## Use Case:

External users and Dota 2 players use this skill through an agent to get Chinese-language build recommendations, lane and teamfight advice, rank-specific win-rate context, and optional hero ability or talent details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional update scripts fetch public game data and rewrite local JSON databases.

Mitigation: Run update scripts only when intentionally refreshing data, from the skill directory, and not as root.

Risk: Merge scripts consume dotabase JSON files from /tmp, which can affect generated local databases.

Mitigation: Use merge scripts only after confirming the /tmp dotabase inputs are trusted and expected.

Risk: Game recommendations may become stale as Dota 2 heroes, items, and balance patches change.

Mitigation: Refresh the bundled databases before relying on the skill for current patch-specific coaching.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangjian1412/skills/dota2-coach-publish)
- [ClawHub publisher profile](https://clawhub.ai/user/yangjian1412)
- [OpenDota API](https://api.opendota.com/api)
- [dotabase game data](https://github.com/mdiller/dotabase)
- [Valve VPK file format](https://developer.valvesoftware.com/wiki/VPK_File_Format)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown-style Chinese-language coaching response with tables and optional bash command snippets for manual data refresh.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal use reads bundled local JSON data; update scripts are optional and manually invoked.]

## Skill Version(s):

1.1.9 (source: release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
