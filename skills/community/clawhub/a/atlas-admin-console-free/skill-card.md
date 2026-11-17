## Description: <br>
Atlas Admin Console Free helps agents browse MongoDB Atlas Admin API categories, inspect endpoint and schema definitions, and prepare read-only or credentialed API calls from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and MongoDB Atlas operators use this skill to find Atlas Admin API endpoints, review request and schema details, and support cluster, backup, user, alert, and monitoring lookups. Live calls require Atlas credentials and should be reviewed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentialed Atlas Admin API actions can change MongoDB Atlas resources despite read-only documentation language. <br>
Mitigation: Use least-privilege Atlas credentials and require explicit user approval before any POST, PUT, PATCH, or DELETE command. <br>
Risk: Free-edition feature claims around export and batch calls are inconsistent. <br>
Mitigation: Verify the installed artifact's available commands before relying on export, batch, or automation features. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/atlas-admin-console-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Node.js 18+ and MongoDB Atlas credential environment variables for live API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
