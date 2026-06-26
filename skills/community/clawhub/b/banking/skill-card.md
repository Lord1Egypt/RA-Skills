## Description: <br>
Manage retail and business banking workflows with payment operations, account controls, reconciliation, fraud response, and compliant communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and operations teams use this skill to classify banking requests, verify payment controls, triage reconciliation and fraud incidents, and draft compliant customer-facing updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local notes in ~/banking/ may contain sensitive banking workflow context if users over-collect details. <br>
Mitigation: Keep notes minimal and operational, avoid credentials and full account numbers, and periodically remove stale incident details. <br>
Risk: Payment, fraud, or compliance guidance could be mistaken for approval to move funds or make legal determinations. <br>
Mitigation: Use the skill as support for official procedures only, confirm required controls and approvals, and escalate legal, sanctions, AML, or irreversible-funds decisions to qualified owners. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/banking) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [Skill homepage](https://clawic.com/skills/banking) <br>
- [Banking setup](setup.md) <br>
- [Payment operations guide](payment-ops.md) <br>
- [Banking incident response](incident-response.md) <br>
- [Compliance scope boundaries](compliance-scope.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with checklists, status summaries, customer message drafts, and local memory templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference or update concise local notes under ~/banking/ when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
