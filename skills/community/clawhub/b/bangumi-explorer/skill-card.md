## Description: <br>
Query Bangumi (bgm.tv) for anime, manga, light novels, games, and music. Search subjects, view details and episode lists, browse seasonal anime charts, rating rankings, and look up voice actors / staff. No authentication required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mountlynx](https://clawhub.ai/user/mountlynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up Bangumi subjects, episode lists, seasonal anime charts, ratings, staff, voice actors, and characters through bgm.tv without authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bangumi searches are sent to bgm.tv, which can expose user query terms to an external service. <br>
Mitigation: Avoid sensitive search terms when using the skill, especially on shared or monitored systems. <br>
Risk: API responses may be cached locally in ~/.bangumi/cache/, leaving lookup history or returned content on disk. <br>
Mitigation: Clear the local Bangumi cache if local privacy matters or when using a shared machine. <br>


## Reference(s): <br>
- [Bangumi API base](https://api.bgm.tv/v0) <br>
- [Bangumi API documentation](https://github.com/bangumi/api) <br>
- [Bangumi OpenAPI v0 spec](https://github.com/bangumi/api/blob/master/open-api/v0.yaml) <br>
- [ClawHub skill page](https://clawhub.ai/mountlynx/bangumi-explorer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and plain-text Bangumi lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Script output is intended to be presented as-is; API responses may be cached locally in ~/.bangumi/cache/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
