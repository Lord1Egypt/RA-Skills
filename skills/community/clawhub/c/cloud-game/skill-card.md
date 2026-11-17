## Description:

Cloud Game helps users search, compare, and launch games on Tianyi Cloud Game from natural-language game names or genre requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pokemummaster](https://clawhub.ai/user/pokemummaster)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to find exact games or get genre-based recommendations on Tianyi Cloud Game, then launch the selected play.cn game page in a browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Game search terms are sent to play.cn.

Mitigation: Use the skill only for non-sensitive game discovery and launch requests; avoid account, payment, and troubleshooting details.

Risk: The skill writes a local cache of game results.

Mitigation: Treat cached content as short-lived non-sensitive game metadata and avoid entering sensitive information into game search prompts.

Risk: The skill opens play.cn game pages in the browser.

Mitigation: Open only sanitized h5.play.cn or play.cn game URLs and ask the user to choose when a match is ambiguous.

## Reference(s):

- [Tianyi Cloud Game](https://h5.play.cn/)
- [ClawHub skill page](https://clawhub.ai/pokemummaster/skills/cloud-game)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown game cards and short text prompts, with browser-launch commands when a game URL is selected]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selected games are opened on play.cn after URL filtering.]

## Skill Version(s):

1.0.0 (source: frontmatter, _meta.json, README.md, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
