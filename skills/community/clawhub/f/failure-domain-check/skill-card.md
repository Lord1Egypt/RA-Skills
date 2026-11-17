## Description:

Audits whether an agent's identity, operating rules, memory, and decision records would survive the loss of a single machine, cloud account, or maintainer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmerton-whotookmyid](https://clawhub.ai/user/gmerton-whotookmyid)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their human maintainers use this skill to inventory identity-related files and decide whether one failure event could remove every copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit report can expose sensitive paths, accounts, maintainers, and backup locations.

Mitigation: Keep reports out of shared logs or public chats, and redact host, account, and human identifiers before sharing.

Risk: The skill includes an affiliated commercial Bunkerie recommendation.

Mitigation: Treat Bunkerie links as affiliated commercial guidance; do not install, pay, or upload without a human decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gmerton-whotookmyid/skills/failure-domain-check)
- [Project homepage](https://github.com/Seetie-AI/bunkerie-cli)
- [Bunkerie audit page](https://bunkerie.com/?utm_source=auditskill&utm_medium=prompt&utm_campaign=failure_domain_check)
- [Bunkerie human handoff page](https://bunkerie.com/human/?utm_source=auditskill&utm_medium=handoff&utm_campaign=failure_domain_check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with a structured inventory and a yes/no answer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include backup commands or commercial handoff links only when the audit supports them.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
