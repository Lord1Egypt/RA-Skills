## Description:

Dota2 Coach provides Chinese-language Dota 2 item-build and playstyle guidance using local hero, ability, talent, and item-popularity data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangjian1412](https://clawhub.ai/user/yangjian1412)

### License/Terms of Use:

MIT-0

## Use Case:

Dota 2 players and agent users use this skill to ask for Chinese-language hero win-rate context, item builds, laning advice, matchup considerations, and playstyle tips. Maintainers can manually refresh the bundled local data from public game-data sources when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual update scripts may contact public game-data APIs and overwrite local JSON databases.

Mitigation: Run update scripts intentionally, review the resulting data changes, and keep the default local-database behavior for normal guidance requests.

Risk: A few older utilities assume a specific OpenClaw filesystem path.

Mitigation: Check paths before running legacy utilities and prefer current scripts that operate relative to the skill directory.

Risk: Gameplay guidance can become stale when Dota 2 patches change heroes, abilities, or items.

Mitigation: Refresh and review the bundled data after game patches before relying on item-build or matchup recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangjian1412/skills/dota2-coach)
- [OpenDota API](https://api.opendota.com/api)
- [Valve VPK file format](https://developer.valvesoftware.com/wiki/VPK_File_Format)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style Chinese gameplay guidance with tables and concise bullet points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bundled local JSON data by default; update scripts may be run manually to refresh game data.]

## Skill Version(s):

1.1.10 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
