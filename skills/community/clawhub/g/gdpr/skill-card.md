## Description: <br>
Audit GDPR compliance, generate privacy policies, and document data flows. Use when auditing practices, drafting policies, or checking consent flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Privacy, security, and compliance teams use this skill to record GDPR-related audit, policy, consent, retention, and data-access events in a local command-line log and export those records for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Entries are saved in plaintext local logs and exports, so secrets, raw personal data, or full identifiers could be exposed on the user's machine. <br>
Mitigation: Enter only redacted or non-sensitive summaries; avoid passwords, API keys, raw personal data, and full identifiers. <br>
Risk: Local GDPR log and export files may persist longer than intended under ~/.local/share/gdpr. <br>
Mitigation: Protect or delete the local data directory according to the user's retention policy and access-control requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/gdpr) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text terminal output with local log files and JSON, CSV, or TXT exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores activity logs and exports locally under ~/.local/share/gdpr.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
