## Description:

Scans Freelancer.com for projects matching a freelancer's skills, drafts personalized bid proposals, and helps track bidding history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[27555402-spec](https://clawhub.ai/user/27555402-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers and external users use this skill to find relevant Freelancer.com projects, draft concise bid proposals, and maintain a bidding history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposal drafts may contain inaccurate claims, unsuitable commitments, or details that should not be submitted unchanged.

Mitigation: Review and edit each proposal before using it for a real bid.

Risk: Search and drafting may use freelance profile details, project criteria, or project URLs provided by the user.

Mitigation: Provide only information needed for the bid workflow and avoid secrets or unnecessary sensitive personal data.

Risk: The local bids.md log may record project, budget, status, or profile-related information.

Mitigation: Review log entries before saving them and store the workspace according to the sensitivity of the bidding history.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown project summaries, bid proposal drafts, and optional bids.md log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a local bids.md bidding history log when requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
