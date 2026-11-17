## Description:

Generates personalized freelance proposal drafts and follow-up messages for Upwork or Fiverr-style gigs matching a freelancer's niche.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skunnyo](https://clawhub.ai/user/skunnyo)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers and independent service providers use this skill to draft daily client outreach proposals, timelines, portfolio pitches, and follow-up messages for gig opportunities in their niche.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated proposal text can include inaccurate, overstated, or placeholder claims before it is sent to a client.

Mitigation: Review and personalize every generated proposal, including portfolio links, claimed experience, pricing, schedule, and follow-up timing.

Risk: Running the bundled script writes a local proposals.md file and may overwrite an existing file with that name.

Mitigation: Run it in a directory where replacing proposals.md is acceptable, or move any existing file before execution.

## Reference(s):

- [Upwork Gig Parsing Patterns](references/upwork-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown proposal drafts and optional CSV-ready proposal content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes proposal drafts to a local proposals.md file when the bundled script is run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
