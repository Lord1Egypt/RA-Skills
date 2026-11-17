## Description:

Publish a YouTube Short from a real rented iPhone through the 0bull MCP server, with the required title, then follow it to a final status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0bull](https://clawhub.ai/user/0bull)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and channel managers use this skill to submit a YouTube Short to a connected account as a draft or published post and check its final status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posting to the wrong account or publishing an unapproved video or title.

Mitigation: Confirm the account, video, title, and draft-versus-publish choice with the user before submission.

Risk: A retry could publish the same Short twice.

Mitigation: Check the submission's final status and do not automatically retry a failed submission.

Risk: The connected 0bull service is outside this skill artifact.

Mitigation: Review the remote service separately before connecting it to a YouTube account.

## Reference(s):

- [0bull MCP documentation](https://docs.0bull.net/mcp/overview)
- [0bull-youtube-post release](https://clawhub.ai/0bull/skills/0bull-youtube-post)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports submission progress and final status; does not claim a Short is live before it is published.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
