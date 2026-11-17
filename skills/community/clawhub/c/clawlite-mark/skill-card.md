## Description:

ClawLite Mark automates Facebook posting, comment reading, context-aware reply drafting or posting, and follow-up thread engagement for community operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

External community operators and developers can use this skill to manage Facebook engagement by posting content, reading comments, drafting or posting replies, and tracking follow-up threads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post public Facebook replies from a persistent browser session and may generate inappropriate or brand-sensitive responses.

Mitigation: Prefer draft or per-reply approval mode, use a dedicated Facebook profile, and require human review for sensitive, controversial, or major-announcement replies.

Risk: The artifact references a private cross-workspace persona file for writing style.

Mitigation: Remove or replace the cross-workspace persona reference with a packaged style guide before allowing public auto-replies.

Risk: The security verdict is suspicious because the skill combines public posting automation with private workspace context.

Mitigation: Review before installing, verify required scripts and browser profile state, and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/clawlite-mark)
- [Publisher profile](https://clawhub.ai/user/x-rayluan)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON receipt examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Facebook action receipts, comment snapshots, reply status records, and error logs when the referenced automation scripts are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
