## Description: <br>
Handle customer calls with scripts, issue resolution, escalation protocols, and interaction logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Customer support, sales, and operations teams use this skill to structure phone or voice interactions, document caller issues, resolve or escalate cases, and track call-center follow-up work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Caller, escalation, and follow-up details may include sensitive personal, payment, legal, health, credential, or compliance information if stored directly in local files. <br>
Mitigation: Use approved CRM or ticketing systems, redact sensitive fields before local notes, and define retention, deletion, and access-control rules before using the skill in a real customer-support environment. <br>
Risk: Local call-center memory files can retain raw customer interaction history beyond operational need. <br>
Mitigation: Limit local memory to the minimum necessary details, regularly review stored entries, and remove records according to the organization's retention policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/call-center) <br>
- [Skill homepage](https://clawic.com/skills/call-center) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with call scripts, checklists, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can guide creation of local memory, escalation, metrics, and script files under ~/call-center/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
