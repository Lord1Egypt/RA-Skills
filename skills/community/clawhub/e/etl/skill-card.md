## Description: <br>
Build ETL pipelines with data ingestion, cleaning, and validation steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to record ETL activities such as ingestion, transformations, validation checks, schema changes, profiling, pipeline steps, search, summaries, and local exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records user-entered ETL activity in local plaintext files under ~/.local/share/etl, which can accidentally preserve credentials, tokens, PII, confidential SQL, or sensitive connection details. <br>
Mitigation: Avoid entering secrets or confidential data, review generated logs and exports before sharing, and delete or protect ~/.local/share/etl when sensitive material may have been recorded. <br>


## Reference(s): <br>
- [ClawHub Etl Skill Page](https://clawhub.ai/bytesagain-lab/etl) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can produce or reference local plaintext ETL log and export files under ~/.local/share/etl.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
