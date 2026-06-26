## Description: <br>
AI Company KB (EN) helps agents manage shared operations records, strategy documents, audit logs, cross-agent knowledge sharing, state sync, and task handoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents in an AI-company workspace use this skill to read and write shared state, audit logs, strategy records, and handoff documents across operational domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad read and write access to operational records can expose or alter sensitive financial, legal, HR, security, or audit data. <br>
Mitigation: Install only in workspaces where this access is intended, restrict the skill to narrow folders and resources, and avoid secrets or regulated records unless explicitly approved. <br>
Risk: Cloud sync, deletion, or record writes could change shared operational state without sufficient review. <br>
Mitigation: Require explicit confirmation before writes, cloud sync, deletion, or access to financial, legal, HR, security, or audit records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnsmithfan/ai-company-kb) <br>
- [Skill homepage](https://clawhub.com/skills/ai-company-kb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and structured records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update shared-state, audit-log, strategy, and handoff records when an agent is granted file access.] <br>

## Skill Version(s): <br>
1.0.1-en2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
