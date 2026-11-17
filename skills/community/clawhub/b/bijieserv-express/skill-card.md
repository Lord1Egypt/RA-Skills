## Description:

Fast package tracking and logistics timeline lookup for 2000+ couriers with BijieServ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhao19871026](https://clawhub.ai/user/huhao19871026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query BijieServ for package status, courier identity, recent logistics events, delivery timelines, and ETA when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package tracking numbers and optional phone or address hints are sent to BijieServ during queries.

Mitigation: Install only where this data sharing is acceptable, provide only required tracking details, and review output redaction before privacy-sensitive use.

Risk: The security guidance notes dependency and privacy hygiene issues.

Mitigation: Review and pin dependency versions, remove or move the unused clawhub dependency, and improve redaction before privacy-sensitive deployment.

## Reference(s):

- [Courier company code table](references/company-codes.md)
- [BijieServ Express Query API](https://www.bijieserv.com/api/method/express_app.open.v1.query.exec)
- [BijieServ](https://www.bijieserv.com/)
- [ClawHub skill page](https://clawhub.ai/huhao19871026/skills/bijieserv-express)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown package-tracking summary with status, latest event, recent timeline, and ETA when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Masks phone numbers in returned tracking text and limits displayed tracking events to recent entries.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact package metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
