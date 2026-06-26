## Description: <br>
Searches, recommends, and launches games on the Tianyi Cloud Game platform from natural-language game requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pokemummaster](https://clawhub.ai/user/pokemummaster) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users ask an agent to find a specific game or recommend games by genre or style on Tianyi Cloud Game, then open a selected play.cn game page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Game searches and opened pages are handled through play.cn services. <br>
Mitigation: Use the skill only for game queries appropriate to share with Tianyi Cloud Game, and review the opened game page before continuing. <br>
Risk: Recent game queries and results may be retained in a local cache. <br>
Mitigation: Avoid private searches, or clear or disable the local cache when recent game activity should not be retained on disk. <br>


## Reference(s): <br>
- [Tianyi Cloud Game](https://h5.play.cn/) <br>
- [Cloud Game on ClawHub](https://clawhub.ai/pokemummaster/cloud-game) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with user-facing status messages, game cards, recommendation lists, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open validated play.cn game pages and may cache recent game query results locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
