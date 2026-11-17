## Description:

Concord negotiates, redacts, and scores risks for sensitive data shared between agents to support privacy-aware transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrea-cola](https://clawhub.ai/user/andrea-cola)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use Concord before forwarding user text to another agent or external service when that text may contain personal, financial, medical, credential, or other sensitive data. It returns a negotiated transfer result that can include redaction decisions, risk scores, a redacted outbound payload, and audit information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Potentially sensitive unredacted user text may be sent to the Concord service without clear user consent.

Mitigation: Use Concord only when the user or deployment policy permits this transfer, and verify the service operator, retention policy, authorization controls, and user-consent requirements before processing sensitive data.

Risk: Credentials, secrets, protected health information, payment data, national identifiers, or children's data could be included in submitted payloads.

Mitigation: Avoid sending these categories unless the service's controls and legal requirements have been verified for the specific deployment.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/andrea-cola/agent-to-agent-privacy/tree/dev/concord)
- [ClawHub skill page](https://clawhub.ai/andrea-cola/skills/concord)
- [Concord service base URL](https://concord-xybl.onrender.com)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON responses with concise text or Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted outbound payloads, category decisions, risk scores, re-identification checks, and signed attestations.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
