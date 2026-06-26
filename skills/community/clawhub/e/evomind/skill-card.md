## Description: <br>
EvoMind provides a five-layer local SQLite memory engine for agents, including persistent facts, reusable skills, session cache, curation, and full-text recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thebuddha5566](https://clawhub.ai/user/thebuddha5566) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use EvoMind to add persistent local memory, reusable skill storage, session cache, curation, and recall to Python-based agents without external services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent memories may persist sensitive prompts, personal data, or secrets in a local SQLite database. <br>
Mitigation: Do not store passwords, API keys, private prompts, or personal data unless local retention is intended; choose the database path deliberately and review backups. <br>
Risk: Deletion and curation commands can remove or alter stored memories and reusable skills. <br>
Mitigation: Review deletion calls before execution, use the built-in confirmations where available, and keep backups when the memory database is important. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local SQLite database at the configured db_path.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
