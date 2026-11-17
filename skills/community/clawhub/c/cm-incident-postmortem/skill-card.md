## Description:

Generate structured, blame-free incident postmortem reports from logs, timeline data, and incident metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and incident response teams use this skill to draft post-incident reviews, reconstruct timelines from logs or JSON event data, check for blameful language, and produce action-oriented postmortem reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can carry untrusted incident or log content into a rendered document.

Mitigation: Prefer Markdown or JSON for untrusted inputs, and only open or host HTML generated from trusted or sanitized content.

Risk: Incident reports and logs may contain sensitive operational details.

Mitigation: Provide only intended incident files and review generated reports before sharing them outside the response team.

## Reference(s):

- [Postmortem Templates & Guidelines](artifact/references/templates.md)
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/cm-incident-postmortem)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, guidance]

**Output Format:** [Markdown, HTML, JSON, or plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write reports to a requested output path; exits nonzero for blame findings, critical severity, or parsed error/fatal log events.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
