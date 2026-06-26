## Description: <br>
Automate VC investment partner workflows by triaging emails, integrating with Affinity CRM, generating memos, managing calendars, and providing daily briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lindsay-pettingill](https://clawhub.ai/user/lindsay-pettingill) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Venture capital investment partners, solo GPs, and emerging fund managers use this skill to triage founder email, prepare draft responses, manage Affinity CRM deal records, generate investment memos, coordinate calendar workflows, and review daily briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require broad Gmail, Google Calendar, and Affinity CRM authority. <br>
Mitigation: Review requested access before installation and start in draft-only and review-only mode until the workflows are scoped and tested. <br>
Risk: Automation boundaries for archive actions and CRM writes may be too broad for automatic approval. <br>
Mitigation: Disable auto-archive and automatic Affinity writes initially, and require explicit action-specific confirmation for external changes. <br>
Risk: Affinity API keys and other credentials could be exposed if stored in shell startup files or committed configuration. <br>
Mitigation: Store credentials in a password manager or secret manager and keep API keys out of git-tracked files and shell startup files. <br>
Risk: Scheduled or heartbeat runs could perform workflow actions without enough supervision. <br>
Mitigation: Avoid unattended scheduled runs until permissions, labels, CRM mappings, and review checkpoints are narrowed and verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lindsay-pettingill/clawdbot-for-vcs) <br>
- [gog CLI](https://github.com/martynsmith/gog) <br>
- [Affinity CRM](https://www.affinity.co/) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact bootstrap guide](artifact/BOOTSTRAP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown workflow guidance with command examples, draft email text, CRM update instructions, calendar actions, daily briefings, and investment memo templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gmail, Google Calendar, and Affinity access; user approval is expected before sending email or making external CRM and calendar changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
