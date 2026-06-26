## Description: <br>
滴答清单任务管理工具 helps agents manage Dida365/TickTick tasks and projects through Python CLI commands for creating, viewing, completing, updating, moving, searching, and deleting items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woodcoal](https://clawhub.ai/user/woodcoal) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and users with Dida365/TickTick accounts use this skill to manage task and project workflows from the command line, including task creation, search, updates, completion, movement, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify task and project data in a connected Dida365/TickTick account. <br>
Mitigation: Install it only for accounts where this access is intended, and review account-changing commands before execution. <br>
Risk: Local credential and cache files may contain sensitive account data. <br>
Mitigation: Keep .env, .dida-token.json, and .dida-cache.json private and avoid committing or casually syncing them. <br>
Risk: Delete operations can remove tasks or projects when supplied with the wrong ID. <br>
Mitigation: Verify task and project IDs and require explicit user approval before running delete commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/woodcoal/dida365-skill) <br>
- [Dida365 developer platform](https://developer.dida365.com/manage) <br>
- [Dida365 OpenAPI endpoint](https://api.dida365.com/open/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OAuth credentials and a local cache; destructive delete commands require explicit approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
