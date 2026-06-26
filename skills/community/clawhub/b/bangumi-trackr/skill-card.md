## Description: <br>
Manage Bangumi collections and track watch progress via OAuth for anime, book, game, music, and personal Bangumi data workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mountlynx](https://clawhub.ai/user/mountlynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure OAuth access to a Bangumi account, inspect personal collection status, and update watch or collection progress from command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores OAuth credentials or tokens locally and can change Bangumi account collections when mutating commands are run. <br>
Mitigation: Install only when OAuth account access is acceptable, protect or remove ~/.bangumi/token.json on non-Windows systems when no longer needed, and review IDs before running collect, uncollect, watch, or related mutating commands. <br>


## Reference(s): <br>
- [Bangumi Tracker - Command Reference](references/COMMANDS.md) <br>
- [Bangumi Tracker - API Compliance](references/API.md) <br>
- [Bangumi API v0](https://github.com/bangumi/api) <br>
- [Bangumi OAuth App Registration](https://bgm.tv/dev/app/create) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and command reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.9+, a Bangumi account, a browser for OAuth, and local credential storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
