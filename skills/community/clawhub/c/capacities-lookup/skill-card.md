## Description: <br>
Search Capacities for likely object matches and return direct capacities:// links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GrantGochnauer](https://clawhub.ai/user/GrantGochnauer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and other Capacities users use this skill to find notes, meetings, projects, people, references, pages, or other Capacities objects by title or search term and return direct links to likely matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses CAPACITIES_API_TOKEN to search a user's Capacities workspace. <br>
Mitigation: Install and enable it only in workspaces where agent access to Capacities lookup is intended, and prefer explicit lookup requests. <br>
Risk: Lookup terms and result metadata may remain in the local data/capacities cache. <br>
Mitigation: Treat the workspace cache as sensitive and clear it when lookup history or metadata should not persist. <br>
Risk: A configurable API base URL could send requests to an unintended endpoint. <br>
Mitigation: Use the default Capacities endpoint or another trusted CAPACITIES_API_BASE_URL. <br>
Risk: Sourcing ~/.zshrc before running commands can execute local shell configuration. <br>
Mitigation: Source shell startup files only when they are trusted, or export the required token directly for the command. <br>


## Reference(s): <br>
- [OpenClaw-Capacities homepage](https://github.com/GrantGochnauer/OpenClaw-Capacities) <br>
- [Capacities Lookup on ClawHub](https://clawhub.ai/GrantGochnauer/capacities-lookup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with direct capacities:// links and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Lookup results may include titles, object types, match quality, matched terms, and fallback suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
