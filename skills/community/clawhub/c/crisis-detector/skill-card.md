## Description:

Crisis Detector helps agents identify self-harm, suicide ideation, and mental-health crisis signals in user communication, estimate severity, provide crisis resources, and support escalation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi)

### License/Terms of Use:


## Use Case:

Developers and safety teams at platforms with user communication can use this skill to analyze text for crisis signals, triage risk, connect users with support resources, and coordinate human follow-up. It is most relevant for social, community, wellness, education, support, and chat applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad mental-health monitoring and retained tracking can expose sensitive user data without clear consent or lawful basis.

Mitigation: Use explicit user notice or consent/lawful-basis handling, data minimization, redaction, retention limits, deletion workflows, and least-privilege access.

Risk: Automated crisis severity scoring and escalation can create harmful false positives, missed crises, or inappropriate emergency actions.

Mitigation: Require human review for escalation decisions, train safety-team reviewers, document clear escalation procedures, and keep emergency-services decisions under qualified human control.

Risk: Crisis logs, alerts, and safety dashboards can expose highly sensitive mental-health status to unauthorized users.

Mitigation: Implement role-based access controls, audit logging, server-side identity binding, and confidential logging before production use.

Risk: Unverified package provenance increases supply-chain and maintenance risk.

Mitigation: Require an exact reviewed package version or source provenance before installation and run the skill with least privilege.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raghulpasupathi/skills/crisis-detector)
- [ClawHub publisher profile](https://clawhub.ai/user/raghulpasupathi)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, JavaScript, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include crisis triage categories, resource lookup examples, integration snippets, event-handling examples, and operational guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
