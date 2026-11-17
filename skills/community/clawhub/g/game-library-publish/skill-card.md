## Description:

Queries Steam and Epic Games libraries for game lists, search results, statistics, duplicate detection, recommendations, and Chinese game-name display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlalamoon](https://clawhub.ai/user/vlalamoon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to inspect personal Steam and Epic Games libraries, find owned games, identify unplayed or duplicate titles, and refresh Chinese display-name mappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted search text can execute code.

Mitigation: Escape or parameterize search input before passing it to embedded Python, and reject unexpected shell metacharacters.

Risk: Account-linked Steam and Epic library metadata is cached insecurely.

Mitigation: Store cache files in a user-owned location with restrictive permissions and provide a clear purge path.

Risk: Steam CLI forwarding may allow operations beyond read-only library queries.

Mitigation: Restrict forwarded Steam CLI arguments to an allowlist of read-only library and metadata commands.

Risk: Chinese-name lookups contact Steam and Xiaoheihe services with game identifiers.

Mitigation: Make network lookups explicit and allow users to skip or disable Chinese-name refresh commands.

## Reference(s):

- [Skill page](https://clawhub.ai/vlalamoon/skills/game-library-publish)
- [Legendary CLI](https://github.com/derrod/legendary)
- [Steam app details API](https://store.steampowered.com/api/appdetails)
- [Xiaoheihe game detail endpoint](https://api.xiaoheihe.cn/game/share_game_detail)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI text output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Steam CLI, Legendary CLI, and STEAM_API_KEY; uses local cache files for library data and Chinese-name mappings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
