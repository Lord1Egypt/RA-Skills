## Description:

BaZi Insight Report - Cantian AI helps agents create paid Cantian BaZi report checkout links, check report status by profile ID, and return a download page when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianlinle](https://clawhub.ai/user/tianlinle)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to create a paid Cantian BaZi report order, receive a payment link, and later check generation status or retrieve the download page using a profile ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Report inputs and profile IDs are sent to Cantian services, and checkout creates payment links.

Mitigation: Use the skill only after the user clearly asks to buy or check a report, collect only required inputs, and make clear that payment should proceed only when the order details are correct.

Risk: The server security summary reports that status lookup can expose report status and a download-page URL from only a profile ID with unclear ownership checks.

Mitigation: Treat profile IDs like private access tokens and require explicit user consent and a profile ID supplied by the user before checking status or sharing download links.

Risk: The server security verdict is suspicious.

Mitigation: Review the skill before installation and prefer a version with stronger consent, ownership, and payment validation around status checks and downloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianlinle/skills/bazi-report)
- [Cantian AI](https://cantian.ai)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment links, profile IDs, paid/readiness status, and download-page URLs.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
