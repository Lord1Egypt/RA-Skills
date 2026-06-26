## Description: <br>
Apple Music DJ analyzes Apple Music listening history, Replay stats, library data, and taste patterns to generate personalized playlists, recommendations, insights, and taste summaries through MusicKit workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[and3rn3t](https://clawhub.ai/user/and3rn3t) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External Apple Music users and developers use this skill to analyze listening data, discover music, generate playlists, prepare concert or release-radar mixes, and optionally automate recurring curation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Apple Music developer and user tokens that can access personal listening data. <br>
Mitigation: Store tokens only in environment variables, treat them like passwords, and rotate or remove them when no longer needed. <br>
Risk: Playlist workflows can create or modify playlists in the user's Apple Music library. <br>
Mitigation: Use explicit user confirmation before write actions and review generated track lists before committing changes. <br>
Risk: Cron automation may run recurring Apple Music actions without direct supervision. <br>
Mitigation: Review generated schedules and crontab entries before enabling automation; avoid enabling cron until command construction has been reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/and3rn3t/apple-music-dj) <br>
- [Authentication setup](references/auth-setup.md) <br>
- [Apple Music API reference](references/api-reference.md) <br>
- [Playlist strategies](references/playlist-strategies.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Apple Music playlists, cache taste profiles locally, generate SVG or text taste cards, and configure optional cron automation.] <br>

## Skill Version(s): <br>
3.1.0 (source: frontmatter, pyproject.toml, clawhub.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
