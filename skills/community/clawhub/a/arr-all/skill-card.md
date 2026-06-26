## Description: <br>
Unified command-line interface for Radarr, Sonarr, and Lidarr. Search, add, and manage movies (Radarr), TV shows (Sonarr), and music (Lidarr) with calendar view and health monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rappo](https://clawhub.ai/user/rappo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage configured Radarr, Sonarr, and Lidarr instances from one command-line interface, including search, add, remove, calendar, health, and status workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or remove items from configured Radarr, Sonarr, and Lidarr libraries. <br>
Mitigation: Keep API credentials private, verify service URLs point to owned instances, and require explicit user confirmation before remove commands, especially when --delete-files is used. <br>


## Reference(s): <br>
- [arr-all on ClawHub](https://clawhub.ai/rappo/arr-all) <br>
- [rappo publisher profile](https://clawhub.ai/user/rappo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Command-line text, markdown examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; optionally uses column for formatted output.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
