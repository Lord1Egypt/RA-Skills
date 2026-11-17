## Description:

Triage incoming insurance claims by checking policy-trigger coverage, banding severity and complexity, screening fraud indicators, estimating first-pass reserves, and recommending routing with an SLA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Claims handlers, adjusters, and claims operations teams use this skill to turn FNOL or new-claim details into a structured triage note for coverage review, severity banding, fraud-indicator screening, reserve planning, and routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle sensitive claim and policy information.

Mitigation: Use it only in an approved claims workflow with appropriate privacy, access-control, and data-handling practices.

Risk: Reserve, SIU-routing, and coverage outputs could be mistaken for final decisions.

Mitigation: Treat outputs as support for qualified claims professionals and follow applicable claims-handling policy and regulation before making coverage, fraud, reserve, or payment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/claims-triage)
- [Claims Triage homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/claims-triage.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown triage note with coverage view, severity band, indicator screen, reserve range, routing recommendation, SLA, and information gaps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Labels assumptions from thin FNOL inputs and frames coverage, reserve, and SIU referral outputs as analytical support rather than final determinations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
