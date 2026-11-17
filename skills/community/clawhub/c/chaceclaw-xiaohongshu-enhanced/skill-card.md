## Description:

An XHS/RED automation skill pack that guides an agent through MCP setup, login, posting, search, browsing, interaction, profile analysis, and content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ling-qian](https://clawhub.ai/user/ling-qian)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and developers use this skill to coordinate Xiaohongshu account workflows through xiaohongshu-mcp, including setup, login, content publishing, search, engagement, profile review, and content planning. The skill is intended to keep public write actions behind confirmation and platform-aware rate limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to configure full account session cookies for Xiaohongshu automation.

Mitigation: Use only accounts prepared for automation, keep cookie files out of chat and logs, store them with restricted local permissions, and refresh or replace them when login checks fail.

Risk: The setup flow references unpinned third-party package or image installation paths.

Mitigation: Prefer pinned and verified xiaohongshu-mcp package or image versions before installation, and review the resolved dependency before connecting an account.

Risk: Posting, commenting, liking, and collecting are public account actions that can affect reputation or trigger platform restrictions.

Mitigation: Require explicit user confirmation before write actions, apply the provided rate-limit guidance, and stop or reduce activity when account or platform warnings appear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ling-qian/skills/chaceclaw-xiaohongshu-enhanced)
- [xhs-compliance.md](xhs-compliance.md)
- [xhs-rate-limits.md](xhs-rate-limits.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, MCP call patterns, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured xiaohongshu-mcp service and valid account session before platform actions can run.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
