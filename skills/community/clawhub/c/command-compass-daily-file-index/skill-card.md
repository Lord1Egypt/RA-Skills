## Description: <br>
Local-first resource indexing skill for Command Compass. It converts user-approved files, folders, links, skill files, downloads folders, website favorites, and prompt resources into Command Compass CardSchema v1 cards that the Windows client can import directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Command Compass users use this skill to turn explicitly selected local resources, links, favorites, and skill files into importable CardSchema v1 cards while preserving local-first privacy boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated cards may expose local paths or sensitive resource metadata if users approve private resources for indexing. <br>
Mitigation: Use the skill only with explicitly selected resources, review generated cards before importing or syncing, and do not upload local paths, file names, file contents, tokens, cookies, passwords, API keys, or usage history. <br>
Risk: Cards that point to executable-like files, shortcuts, scripts, or installers could be mistaken for safe automated actions. <br>
Mitigation: Keep shell permissions false and rely on the Command Compass client to request confirmation before opening those resources. <br>
Risk: Website-agent guidance could be applied outside the intended wboke.com development project or with mishandled credentials. <br>
Mitigation: Use the website-agent instructions only in the intended wboke.com project and handle tokens outside generated cards and public responses. <br>


## Reference(s): <br>
- [Command Compass homepage](https://www.wboke.com) <br>
- [ClawHub skill page](https://clawhub.ai/addogiavara-tech/skills/command-compass-daily-file-index) <br>
- [Command Compass skill adaptation report](artifact/COMMAND_COMPASS_SKILL_ADAPTATION_REPORT.md) <br>
- [Website agent instructions](artifact/WEBSITE_AGENT_INSTRUCTIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Configuration, Guidance] <br>
**Output Format:** [UTF-8 JSON arrays or objects containing Command Compass CardSchema v1 cards] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated cards keep permissions conservative and use instruction as the sole copy field.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
