## Description:

Barog helps users view booking guidance, open BeautsGO pages, submit appointment requests, consult support, and check prices for Barog Clinic's Gangnam location in Seoul.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beautsgo](https://clawhub.ai/user/beautsgo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get Barog Clinic Gangnam booking guidance, submit appointment details through BeautsGO, open consultation and price pages, and retrieve project pricing when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit appointment and contact details, including a phone number if provided, to external booking services without the promised explicit confirmation step.

Mitigation: Require a clear confirmation step that displays the destination service and submitted fields before calling the booking API.

Risk: The skill includes a shell-based browser-opening helper.

Mitigation: Remove shell-based URL opening or replace it with a safer platform API while retaining strict HTTPS and host allowlisting.

Risk: API credentials are distributed with the package.

Mitigation: Move credentials out of the distributed skill package and load them from a managed secret store or deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beautsgo/skills/barog-clinic-booking)
- [BeautsGO Barog Clinic Gangnam booking page](https://i.beautsgo.com/cn/hospital/barogclinic-gangnam/skill)
- [BeautsGO Barog Clinic Gangnam profile](https://i.beautsgo.com/cn/hospital/barogclinic-gangnam?from=skill)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, guidance]

**Output Format:** [String containing Markdown-style booking guidance, status messages, links, and price or submission results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open allowed BeautsGO URLs in a local browser and may call external booking or price APIs based on user intent.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
