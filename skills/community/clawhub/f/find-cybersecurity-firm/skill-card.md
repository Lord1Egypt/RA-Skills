## Description:

Helps users find, shortlist, vet, or enrich US cybersecurity firms for B2B procurement needs such as pen-testing, red team work, security audits, vCISO, SOC 2 readiness, incident response, managed SOC, IAM, cloud security, and AppSec.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, procurement teams, and consultants use this skill to search ServiceGraph's US pro services dataset for cybersecurity firms, compare brief firm profiles, and decide which firms to unlock for contact or enrichment details. It is intended for B2B firm discovery, not consumer security help, hiring, product comparisons, or do-it-yourself remediation guidance.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Fallback REST authentication guidance sources .env.local as shell code, which can execute local commands if that file contains more than simple assignments.

Mitigation: Use a pre-exported SERVICEGRAPH_API_KEY or a strict dotenv parser instead of sourcing .env.local.

Risk: Unlocking detailed firm records consumes credits and may expose contact, social, address, and platform details for selected firms.

Mitigation: Show the credit cost and selected apex domains before requesting paid unlocks, and proceed only after user approval.

## Reference(s):

- [Find Cybersecurity Firm on ClawHub](https://clawhub.ai/nostrband/skills/find-cybersecurity-firm)
- [Publisher profile: nostrband](https://clawhub.ai/user/nostrband)
- [ServiceGraph API](https://api.servicegraph.co)
- [ServiceGraph API keys](https://servicegraph.co/profile/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with ServiceGraph API filters, curl examples, firm shortlists, and unlock guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include paid unlock recommendations after showing credit cost and selected firms.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
