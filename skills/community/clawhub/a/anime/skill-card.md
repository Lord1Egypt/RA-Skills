## Description: <br>
CLI for AI agents to search and lookup anime info for their humans. Uses Jikan (unofficial MyAnimeList API). No auth required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffaf](https://clawhub.ai/user/jeffaf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and AI agents use this skill to search anime titles, retrieve MyAnimeList details by MAL ID, and browse current, upcoming, or top-ranked anime through the Jikan API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Anime search queries are sent to the Jikan API. <br>
Mitigation: Avoid including private or sensitive information in anime search queries. <br>
Risk: Installation or use may rely on an external anime CLI script. <br>
Mitigation: Confirm any external CLI script comes from the intended repository before installing or executing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeffaf/anime) <br>
- [Jikan](https://jikan.moe) <br>
- [Jikan v4 API Documentation](https://docs.api.jikan.moe/) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs anime search results, rankings, seasonal lists, details, synopsis text, and trailer URLs when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
