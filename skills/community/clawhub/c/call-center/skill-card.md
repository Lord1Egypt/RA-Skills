## Description:

Handle customer calls with scripts, issue resolution, escalation protocols, and interaction logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Customer-support and call-center agents use this skill to structure inbound support, outbound sales, complaint handling, escalations, and post-call documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer details, escalation notes, and call history may be stored in local plaintext markdown files.

Mitigation: Use the skill only with approved customer-data systems, avoid unnecessary personal or sensitive details, and define retention, deletion, and access-control rules before use.

Risk: Call handling guidance can affect customer commitments, compliance escalation, and supervisor handoff quality.

Mitigation: Review scripts and escalation thresholds against the organization's policies before deploying the skill in a live support environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/call-center)
- [Skill homepage](https://clawic.com/skills/call-center)
- [Escalation Guide](artifact/escalation.md)
- [Memory Setup](artifact/memory-template.md)
- [Call Scripts](artifact/scripts.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and call-script templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing call flows, escalation guidance, local memory-file setup steps, and documentation templates.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
