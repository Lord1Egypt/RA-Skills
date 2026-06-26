## Description: <br>
Interact with Akaunting open-source accounting software via REST API. Use for creating invoices, tracking income/expenses, managing accounts, and bookkeeping automation. Triggers on accounting, bookkeeping, invoicing, expenses, income tracking, or Akaunting mentions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liekzejaws](https://clawhub.ai/user/liekzejaws) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to an Akaunting instance for bookkeeping tasks such as listing accounts, categories, transactions, and items, and creating income, expense, and item records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change financial records and handles accounting credentials. <br>
Mitigation: Use it only with an Akaunting instance the agent is authorized to access, use a least-privileged account, protect the config file, and require explicit confirmation before creating or deleting records. <br>
Risk: The provided setup exposes Akaunting on port 8080 and includes default credentials. <br>
Mitigation: Change default passwords, restrict access to port 8080, and use HTTPS for any non-local access. <br>
Risk: Accounting data may be affected by agent actions or setup changes. <br>
Mitigation: Back up accounting data before installation, configuration changes, or record-modifying workflows. <br>


## Reference(s): <br>
- [Akaunting API Reference](references/api.md) <br>
- [Akaunting skill page](https://clawhub.ai/liekzejaws/akaunting) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with CLI commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Akaunting REST API endpoints and may create or modify accounting records when directed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
