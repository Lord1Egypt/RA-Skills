## Description: <br>
Persist and retrieve structured data using the Lance columnar format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vitorhugoze](https://clawhub.ai/user/vitorhugoze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Data Vault to persist structured records across sessions, query stored data, track context, and maintain small local knowledge bases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides agent-accessible local persistent storage and broad destructive operations. <br>
Mitigation: Avoid storing secrets, personal data, credentials, or regulated information, and back up important datasets before update, delete, or drop operations. <br>
Risk: Security evidence reports that the write path can store datasets outside the documented current-directory scope. <br>
Mitigation: Use explicit simple dataset names and review or fix path validation and backup safeguards before relying on the skill for important data. <br>
Risk: Lance locks field types after the first stored record. <br>
Mitigation: Plan dataset schemas before the first append and keep subsequent values consistent with the initially inferred field types. <br>


## Reference(s): <br>
- [Data Vault on ClawHub](https://clawhub.ai/vitorhugoze/data-vault) <br>
- [Lance columnar format](https://github.com/lance-format/lance) <br>
- [Lance documentation](https://lance.org) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands] <br>
**Output Format:** [JSON command responses and local Lance dataset files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can create, read, update, delete, back up, count, and list local datasets.] <br>

## Skill Version(s): <br>
1.0.18 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
