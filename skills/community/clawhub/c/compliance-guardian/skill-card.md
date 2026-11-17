## Description:

Compliance Guardian helps real estate professionals screen transactions for FinCEN real estate reporting requirements, collect report data, and track filing deadlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonbarnato](https://clawhub.ai/user/jonbarnato)

### License/Terms of Use:

MIT-0

## Use Case:

Real estate agents, brokers, transaction coordinators, and closing teams use this skill to identify potentially reportable residential property transfers, prepare FinCEN pre-fill data, and monitor filing deadlines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive identity and tax data, including SSNs, TINs, dates of birth, addresses, and transaction details.

Mitigation: Use only on trusted devices and origins, avoid entering SSNs, TINs, or dates of birth unless necessary, clear browser storage after use, and treat copied exports as sensitive documents.

Risk: Browser-side storage and clipboard export can expose client data to local browser state or other local applications.

Mitigation: Warn users before export, redact fields when possible, and avoid retaining completed filings in localStorage longer than needed.

Risk: The security review flags unsafe browser-side rendering patterns for tracker entries.

Mitigation: Render tracker entries with textContent or equivalent safe DOM APIs, add deletion controls, and review changes before using with real client data.

## Reference(s):

- [Compliance Guardian on ClawHub](https://clawhub.ai/jonbarnato/skills/compliance-guardian)
- [FinCEN BSA E-File Portal](https://bsaefiling.fincen.treas.gov/)
- [First American FinCEN Resources](https://www.firstam.com/fincen/)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Browser-rendered guidance with plain-text report pre-fill output and deadline status data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores filing tracker data in browser localStorage and copies report pre-fill output to the clipboard.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
