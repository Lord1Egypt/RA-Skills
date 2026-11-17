## Description:

Generates personalized, concise cold emails pitching Gracie AI Receptionist by scraping business websites for relevant details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayjjimenez](https://clawhub.ai/user/jayjjimenez)

### License/Terms of Use:


## Use Case:

Sales operators and agent users can use this skill to research public business websites and draft short, personalized cold outreach emails for Gracie AI Receptionist campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The website-scraping workflow can be used with internal or unsafe URLs.

Mitigation: Use only trusted public business URLs or scrubbed lead lists, and do not point the skill at internal hosts or private network addresses.

Risk: Generated outreach emails may contain inaccurate or unsuitable claims.

Mitigation: Manually review generated emails before sending them.

Risk: Saving output writes business or contact details and generated outreach text to local disk.

Mitigation: Use --save only in an appropriate local workspace and protect or delete saved outreach files according to the campaign's data-handling needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayjjimenez/skills/cold-email-generator)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Plain text email output with optional saved .txt files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated emails are intended to be manually reviewed before sending.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
