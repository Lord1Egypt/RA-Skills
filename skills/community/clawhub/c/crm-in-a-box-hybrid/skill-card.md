## Description: <br>
Bootstrap and manage an open, file-based CRM using the CRM-in-a-Box protocol for contacts, pipeline entries, and interactions stored as NDJSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hybrid1labs](https://clawhub.ai/user/hybrid1labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to initialize and maintain a local CRM, add contacts and leads, update pipeline stages, and record customer interactions without depending on a hosted CRM service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CRM records may contain personal, customer, deal, or interaction data stored in local files. <br>
Mitigation: Use a dedicated CRM directory, restrict file access, avoid unnecessary sensitive personal data, and keep backups or version control appropriate for the data. <br>
Risk: Bulk appends or agent-driven updates can create incorrect or duplicate CRM records. <br>
Mitigation: Require user confirmation before bulk writes and review generated NDJSON entries before relying on them operationally. <br>
Risk: The artifact advertises hash-chain or tamper-evidence behavior that security evidence says should not be relied on without verification. <br>
Mitigation: Treat the CRM files as normal local records unless a hash-chain mechanism is separately added and validated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hybrid1labs/crm-in-a-box-hybrid) <br>
- [biz-in-a-box protocol](https://biz-in-a-box.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, YAML, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local file-based CRM structures and append-only NDJSON records when used with the included CLI or documented commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
