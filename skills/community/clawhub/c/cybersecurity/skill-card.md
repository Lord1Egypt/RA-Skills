## Description:

Runs defensive security: alert triage, compromise investigation, attack paths, vulnerability prioritization, detection, and risk reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Security practitioners, developers, and operations teams use this skill for authorized defensive work: triaging alerts, investigating possible compromise, prioritizing vulnerabilities, hardening identity and infrastructure, producing detections, and communicating security risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can maintain sensitive local cybersecurity records, including findings, incidents, inventories, vendors, and generated artifacts.

Mitigation: Install only when this local knowledge base is intended; restrict file permissions, consider encryption or approved secure storage, review sync and backup behavior, and periodically remove stale records.

Risk: The skill may propose actions for live security systems where disruptive or attacker-visible changes could affect evidence, availability, or response outcomes.

Mitigation: Keep live-system work inside written authorization and require explicit confirmation for destructive, noisy, irreversible, or attacker-visible operations.

Risk: Security records can accidentally capture secrets or unnecessary personal data if outputs are saved without review.

Mitigation: Store secret pointers instead of values, keep evidence files and personal records in the user's case store, and limit local notes to identifiers, hashes, counts, categories, and locations.

## Reference(s):

- [ClawHub Cybersecurity skill page](https://clawhub.ai/ivangdavila/skills/cybersecurity)
- [Clawic Cybersecurity skill page](https://clawic.com/skills/cybersecurity)
- [Skill definition](artifact/SKILL.md)
- [Authorization guidance](artifact/authorization.md)
- [Working file templates](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with tables, checklists, code snippets, shell commands, configuration guidance, and risk reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local cybersecurity notes, inventories, findings, incidents, detections, vendors, and generated artifacts under configured local Clawic data paths.]

## Skill Version(s):

1.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
