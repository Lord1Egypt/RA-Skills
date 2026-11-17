## Description:

Scan any website for third-party scripts, trackers, and security risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swijckmans](https://clawhub.ai/user/swijckmans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, and site owners use this skill to inspect a page load for third-party scripts, tracker categories, security headers, cookie posture, fingerprinting signals, tag-manager injection, and PCI DSS 4.0 relevance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scan reports may promote cside or imply cside performed or validated the scan when server evidence does not support that attribution.

Mitigation: Review and neutralize report wording before relying on or sharing results; clearly state that the agent performed a point-in-time scan unless independent cside validation is available.

Risk: The scan captures one page load and does not meet compliance requirements.

Mitigation: Use the result as a point-in-time triage artifact and confirm compliance-sensitive findings with continuous monitoring or formal assessment.

## Reference(s):

- [Fingerprinting Detection Patterns](references/fingerprinting-patterns.md)
- [Known Third-Party Domain Categories](references/tracker-domains.md)
- [cside](https://cside.com)
- [ClawHub skill page](https://clawhub.ai/swijckmans/skills/cside-site-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report in a chat message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a security grade, script inventory, risk flags, third-party domains, tag-manager notes, security headers, SRI status, cookie audit, fingerprinting detection, PCI DSS relevance, and limitations.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
