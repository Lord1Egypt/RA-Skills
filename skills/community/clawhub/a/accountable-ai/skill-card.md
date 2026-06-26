## Description: <br>
Implements governance for AI teams by defining roles, decision authority, procedures, and delegation protocols for accountable, traceable agent work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kgapol](https://clawhub.ai/user/kgapol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, administrators, and teams running AI agents use this skill to establish governance documents, operational checklists, delegation workflows, and audit trails for multi-agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The governance documents may give agents broad authority around deletion, proactive contact, repository pushes, deployments, credentials, or shared configuration. <br>
Mitigation: Review and customize the documents before installation, and require explicit approval before external messages, repository pushes, deployments, or changes to shared configuration. <br>
Risk: Credential handling guidance may encourage documenting access details in workspace files. <br>
Mitigation: Replace credential documentation with references to an approved secrets manager and avoid storing secrets in governance, memory, or procedure files. <br>
Risk: The startup guidance includes deleting bootstrap material after first use, which can remove setup context or audit evidence. <br>
Mitigation: Remove automatic bootstrap deletion or replace it with an archival process that preserves initialization history. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kgapol/accountable-ai) <br>
- [README.md](artifact/README.md) <br>
- [GOVERNANCE.md](artifact/GOVERNANCE.md) <br>
- [PROCEDURES.md](artifact/PROCEDURES.md) <br>
- [DELEGATION.md](artifact/DELEGATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documents with installation shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs governance reference files into a local agent workspace for customization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
