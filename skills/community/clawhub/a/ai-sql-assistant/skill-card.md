## Description: <br>
AI-powered SQL assistant. Generate SQL from natural language, explain queries, optimize performance, review security, and generate migrations for SQLite, PostgreSQL, and MySQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate SQL, explain existing queries, optimize performance, review SQL security issues, and draft migrations for SQLite, PostgreSQL, and MySQL without connecting to a database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI commands send SQL text, schema details, query literals, and migration descriptions to EvoLink's API. <br>
Mitigation: Use AI commands only when external processing by EvoLink is approved, and avoid submitting production secrets or sensitive customer data. <br>
Risk: Generated or optimized SQL may be incorrect, unsafe, or unsuitable for the target environment. <br>
Mitigation: Review generated SQL and security guidance before execution; the skill does not connect to or run commands against a database. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/evolinkai/ai-sql-assistant) <br>
- [Project homepage](https://github.com/EvoLinkAI/sql-skill-for-openclaw) <br>
- [EvoLink API documentation](https://docs.evolink.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown with SQL and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AI commands require EVOLINK_API_KEY and may call api.evolink.ai; local cheatsheet and database-list commands do not require the API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, SKILL.md frontmatter, npm package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
