## Description: <br>
DBdoctor database performance diagnosis platform tools for querying database instances, slow SQL, inspection reports, performance metrics, and performing SQL audit or rewrite operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbdoctor-das](https://clawhub.ai/user/dbdoctor-das) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Database administrators, developers, and operations engineers use this skill to inspect DBdoctor-managed database instances, diagnose performance issues, review slow SQL, run inspections, audit SQL, and request SQL rewrite guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate with DBdoctor administrative access and database credentials. <br>
Mitigation: Install only in a trusted, isolated environment, use HTTPS on a trusted network, and prefer least-privilege DBdoctor and database accounts. <br>
Risk: The skill may cache an API session token locally in .token_cache. <br>
Mitigation: Protect or delete .token_cache according to the deployment's credential handling requirements. <br>
Risk: The execute_sql and manage_instance tools can make database changes or register database instances. <br>
Mitigation: Require explicit human approval before running execute_sql or manage_instance, and review SQL statements and connection parameters before execution. <br>


## Reference(s): <br>
- [DBdoctor Tools on ClawHub](https://clawhub.ai/dbdoctor-das/dbdoctor-tools) <br>
- [Tool API Reference](reference/api_reference.md) <br>
- [Agent Processing Strategies and Decision Guidelines](reference/agent_guidelines.md) <br>
- [Database Performance Diagnosis Knowledge Base](reference/performance_diagnosis_guide.md) <br>
- [DBDoctor Best Practices Guide](reference/best_practices.md) <br>
- [SQL Audit Rules and Inspection Rules Description](reference/audit_and_inspection_rules.md) <br>
- [Common Issues and Solutions](reference/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and structured operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke DBdoctor API helper scripts and return database diagnostics, inspection summaries, SQL audit findings, SQL rewrite guidance, and configuration steps.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
