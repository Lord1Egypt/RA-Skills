## Description:

Helps an agent send a local worker to check, photograph, queue, or pick something up in Seoul and return location-verified photos and answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and businesses use the skill to request on-site checks or pickups by a local worker and receive photos, structured answers, and a verification result.

### Deployment Geography for Use:

Seoul, South Korea (initially Gangnam/Yeoksam; check live coverage)

## Known Risks and Mitigations:

Risk: Dispatch spends prepaid balance and sends location-specific instructions to a real worker.

Mitigation: Check live coverage and the exact quoted total, then obtain the user's explicit approval before dispatch.

Risk: An exposed API key could permit unauthorized paid missions.

Mitigation: Keep the API key private and do not include it in messages or shared output.

Risk: Source reporting shares account-linked usage information when enabled.

Mitigation: Enable source reporting only with the user's explicit consent; otherwise leave it off.

Risk: A mission cannot be cancelled after a worker accepts it.

Mitigation: Explain the cancellation limit before requesting dispatch approval.

## Reference(s):

- [Errand AI ClawHub listing](https://clawhub.ai/chloepark85/skills/errand-ai)
- [Errand setup and service](https://errand.be/clawhub)
- [Optional source-reporting privacy details](https://errand.be/privacy#clawhub-analytics)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include worker answers, photos, location evidence, and verification status; signed photo links expire after one hour.]

## Skill Version(s):

2.0.2 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
