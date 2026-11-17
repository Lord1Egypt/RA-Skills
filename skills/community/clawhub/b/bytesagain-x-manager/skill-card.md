## Description:

Manage X (Twitter) account: auto-post AI-generated tweets, monitor brand mentions, auto-like relevant posts, and send Telegram approval requests for replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to draft, publish, monitor, and engage with X content for the BytesAgain account through X, xAI, and Telegram workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish posts, replies, and likes from the configured X account.

Mitigation: Use a dedicated low-privilege X account or tightly scoped credentials, and add explicit confirmations or dry-run defaults before posting, liking, or replying.

Risk: Reply approval safeguards may be weak or inconsistently enforced.

Mitigation: Fix the reply approval enforcement before deployment and require operator confirmation for every public reply.

Risk: Some local state is stored in shared temporary paths.

Mitigation: Move state to a private per-user application directory with restrictive permissions before running on shared systems.

Risk: Monitored content and generated drafts may be sent to xAI and Telegram services.

Mitigation: Install only when this data sharing is acceptable for the target account, and avoid processing confidential or regulated content through this workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-x-manager)
- [Command Boundary](references/command-boundary.md)
- [API Notes](references/api-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated text for X posts, reports, and approval messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces text-only X posts and replies; when executed with configured credentials, it may call X, xAI, and Telegram APIs and write local state files for drafts, likes, mentions, and pending replies.]

## Skill Version(s):

1.6.0 (source: ClawHub release evidence; artifact frontmatter says 1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
