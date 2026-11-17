## Description:

CLI for AI agents to search and lookup anime info for their humans. Uses Jikan (unofficial MyAnimeList API). No auth required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffaf](https://clawhub.ai/user/jeffaf)

### License/Terms of Use:

MIT

## Use Case:

AI agents assisting users use this skill to search for anime, retrieve MyAnimeList details by ID, and browse current, upcoming, seasonal, or top-ranked anime through Jikan data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package does not include the executable script the skill tells agents to run, and its manual install path points to mutable external code.

Mitigation: Review or install only from a pinned, trusted release that includes the anime script; inspect any manually cloned script before exposing it as a persistent local command.

## Reference(s):

- [ClawHub Anime Skill](https://clawhub.ai/jeffaf/skills/anime)
- [Jikan](https://jikan.moe)
- [Jikan API Documentation](https://docs.api.jikan.moe/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text CLI output with anime IDs, titles, scores, metadata, synopsis text, and links when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, and jq. Uses the unauthenticated Jikan v4 API with documented rate limits.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
