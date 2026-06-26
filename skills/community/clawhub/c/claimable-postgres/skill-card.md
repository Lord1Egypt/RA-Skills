## Description: <br>
Provision instant temporary Postgres databases via Claimable Postgres by Neon (neon.new) with no login, signup, or credit card. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrelandgraf](https://clawhub.ai/user/andrelandgraf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to provision short-lived Neon Postgres databases for local development, demos, prototypes, and tests when no existing DATABASE_URL is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create temporary Neon databases and place generated database credentials in project environment files. <br>
Mitigation: Use it for development, demos, and tests; keep .env files out of source control and avoid sensitive or production data unless the database is properly claimed and managed. <br>
Risk: CLI and Vite plugin paths rely on external packages executed in the target project. <br>
Mitigation: Review package use before choosing those paths, and prefer the REST API path when the agent needs predictable behavior with no added runtime dependency. <br>
Risk: Seed SQL may modify or remove database contents. <br>
Mitigation: Review destructive SQL such as DROP, TRUNCATE, or mass DELETE before running seed scripts. <br>


## Reference(s): <br>
- [Claimable Postgres API](https://neon.new/api/v1/database) <br>
- [Claimable Postgres Vite Plugin Docs](https://neon.com/docs/reference/claimable-postgres#vite-plugin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include REST API JSON parsing guidance and .env key names for generated database URLs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
