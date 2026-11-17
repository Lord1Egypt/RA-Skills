## Description:

Beautsgo Booking helps an AI assistant match users with Korean dermatology, plastic surgery, and aesthetic clinics, then provide booking guidance, price lookup, live consultation links, or appointment submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beautsgo](https://clawhub.ai/user/beautsgo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an AI assistant to find Korean beauty and medical aesthetic clinics, compare booking or price options, and submit appointment requests when they provide the required details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send appointment details, including contact information, to BeautsGO-related services.

Mitigation: Require explicit user confirmation immediately before submission and disclose the clinic, date, party size, and contact information that will be sent.

Risk: The security evidence flags browser URL opening as not safely controlled.

Mitigation: Review and constrain browser-opening behavior before approval, and only allow expected BeautsGO destinations.

Risk: The security evidence recommends removing or redacting logs that may contain personal information.

Mitigation: Redact contact details and appointment payloads from logs before deployment.

Risk: Unpinned install commands can resolve to newer dependency versions.

Mitigation: Use pinned install instructions or lockfile-based installation for reviewed releases.

## Reference(s):

- [Beautsgo Booking ClawHub page](https://clawhub.ai/beautsgo/skills/beautsgo-booking)
- [BeautsGO publisher profile](https://clawhub.ai/user/beautsgo)
- [BeautsGO clinic pages](https://beautsgo.github.io/beautsgo-booking/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown booking guidance with optional browser-opening commands and appointment submission summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request clinic, party size, preferred date or time, and contact information before appointment submission.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
