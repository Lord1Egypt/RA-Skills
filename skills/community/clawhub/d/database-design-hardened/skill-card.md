## Description: <br>
Database design helper for table design, normalization, indexing strategy, migration scripts, test data, and ER diagram descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft database schemas, normalization guidance, indexes, migration SQL, seed data, and ER diagram descriptions for database design workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL, migrations, or index-drop recommendations may be unsuitable for a production database if applied without review. <br>
Mitigation: Review generated SQL carefully and test migrations, index changes, and schemas in a non-production environment before applying them to real data. <br>
Risk: A local command history may record command names and first arguments, which can expose secrets or sensitive schema details if passed on the command line. <br>
Mitigation: Avoid passing secrets or sensitive schema details as command arguments, and remove ~/.local/share/database-design/history.log when needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/database-design-hardened) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown and plain text with SQL and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate SQL schema, migration, index, seed-data, and ER diagram text for review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
