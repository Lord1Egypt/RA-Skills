## Description:

Create short URLs and submit feature requests using 1p.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuanpmt](https://clawhub.ai/user/tuanpmt)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to shorten links, manage organization-scoped short links, and submit or vote on 1p.io feature requests through documented API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send full destination URLs and related metadata to the third-party 1p.io service.

Mitigation: Use it only for links the user is comfortable sharing with 1p.io, and avoid private, tokenized, internal, password-reset, presigned, or otherwise sensitive URLs.

Risk: The skill includes organization link deletion and management actions.

Mitigation: Require an explicit user instruction and confirmation before deleting links or making destructive link-management changes.

Risk: Feature status changes can affect organization-scoped feature tracking.

Mitigation: Require an explicit user instruction, confirm the intended feature and status, and ensure the agent has the required edit permission before updating status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuanpmt/skills/1p-shortlink)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Markdown text with short URL strings and summarized JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated 1p.io short URLs, link metadata, feature request details, and status updates.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
