## Description:

China Express Query helps agents query Chinese courier tracking information for major carriers such as SF Express, YTO, ZTO, STO, Yunda, EMS, JD Logistics, Debon, Best Express, and J&T Express.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyqdq888](https://clawhub.ai/user/hyqdq888)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check shipment status and tracking history for Chinese courier packages from the command line. It can auto-detect supported courier companies or accept an explicit carrier code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider query failures can be shown as ordinary tracking activity, creating misleading shipment status.

Mitigation: Treat tracking results as unverified until the skill clearly reports provider failures and does not substitute simulated tracking events.

Risk: Tracking numbers are sent to third-party lookup services.

Mitigation: Avoid using the skill for sensitive shipment identifiers unless sharing those numbers with the listed providers is acceptable.

Risk: Saved or displayed output may include untrusted provider content.

Mitigation: Review output before reuse and ensure terminal or downstream rendering paths sanitize provider-returned text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyqdq888/skills/china-express-query)
- [Kuaidi100 lookup service](https://www.kuaidi100.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Plain text courier tracking summary; optionally written to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and sends tracking numbers to third-party courier lookup services.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
