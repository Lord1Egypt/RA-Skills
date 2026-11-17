## Description:

DBdoctor database performance diagnosis platform tools for querying database instances, slow SQL, inspection reports, performance metrics, and SQL audit or rewrite operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbdoctor-das](https://clawhub.ai/user/dbdoctor-das)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to inspect DBdoctor-managed database instances, diagnose performance issues, review slow SQL, run SQL audits, and request SQL rewrite guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute unrestricted SQL against a target database.

Mitigation: Require authorized operators to review each SQL statement before execution and avoid production write access unless explicitly approved.

Risk: The skill can register database instances and accepts connection parameters and database credentials.

Mitigation: Use least-privileged DBDoctor and database accounts, verify connection parameters before registration, and avoid passing real database passwords through shared shells.

Risk: The security evidence flags unsafe transport and token storage practices.

Mitigation: Prefer HTTPS with certificate validation and protect or relocate the token cache in trusted DBDoctor environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dbdoctor-das/skills/dbdoctor-tools)
- [Tool API Reference](reference/api_reference.md)
- [Agent Processing Strategies and Decision Guidelines](reference/agent_guidelines.md)
- [DBDoctor Best Practices Guide](reference/best_practices.md)
- [Database Performance Diagnosis Knowledge Base](reference/performance_diagnosis_guide.md)
- [SQL Audit Rules and Inspection Rules Description](reference/audit_and_inspection_rules.md)
- [Common Issues and Solutions](reference/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DBdoctor API query results, SQL audit findings, performance diagnosis summaries, and operator review guidance.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
