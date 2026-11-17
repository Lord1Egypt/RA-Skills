## Description:

Send tracked emails via Gmail and check if they were opened.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cseguinlz](https://clawhub.ai/user/cseguinlz)

### License/Terms of Use:


## Use Case:

External users and developers use DoubleTick to send Gmail messages with read tracking and later check open status, counts, device details, timing, and recent tracked-email summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to run an unpinned npm package with Gmail access.

Mitigation: Pin doubletick-cli to a reviewed exact version and review Gmail permissions before installation.

Risk: The skill enables recipient email-open tracking and metadata collection without clear consent or privacy guidance.

Mitigation: Use it only where recipients have appropriate notice or consent for open tracking and metadata collection.

## Reference(s):

- [DoubleTick website](https://doubletickr.com)
- [DoubleTick npm package](https://www.npmjs.com/package/doubletick-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Gmail read-tracking actions and status summaries through doubletick-cli; requires Node.js, Gmail, and a DoubleTick account.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
