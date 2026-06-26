## Description: <br>
Audit Trail records agent actions in timestamped, hash-chained JSONL logs for auditing, investigation, and accountability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arhadnane](https://clawhub.ai/user/arhadnane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and governance reviewers use this skill to create local audit logs, verify log-chain integrity, query agent activity, and generate investigation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit logs are mutable and should not be treated as compliance-grade immutable records. <br>
Mitigation: Use this skill as a best-effort local audit trail and pair it with external integrity protection, restricted file permissions, and independent log retention controls. <br>
Risk: Agent activity logs may retain secrets, private messages, memory contents, or configuration values. <br>
Mitigation: Review and test redaction behavior before deployment, avoid logging sensitive fields where possible, and add stronger redaction rules for the target environment. <br>
Risk: Retention and purge behavior may preserve sensitive local audit data longer than intended. <br>
Mitigation: Define an approved retention policy before enabling the skill and periodically review stored files under .security/audit-trail. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/arhadnane/audit-trail) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSONL audit logs, JSON verification and report objects, and Markdown usage examples with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local audit artifacts under .security/audit-trail and redacts configured secret patterns before logging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
