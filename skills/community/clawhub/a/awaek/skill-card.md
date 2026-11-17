## Description:

Personal source engine for saved X bookmarks: ask, draft, decide, and plan from the user's own saves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1lystore](https://clawhub.ai/user/1lystore)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Awaek to sync saved X bookmarks into a local SQLite library, then ask questions, find saved posts, draft content, compare ideas, and plan from focused saved-post evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Awaek requires local access to an authenticated xurl setup and stores saved X bookmarks in a local SQLite database.

Mitigation: Use it only on trusted devices, keep X credentials out of chat, protect the local database path, and review local data-retention expectations before syncing.

Risk: The documented xurl prerequisite includes a curl-to-bash installer flow.

Mitigation: Prefer a pinned or package-managed installation method, or independently verify the installer before running it.

Risk: Saved social posts may contain inaccurate content or prompt-like text that should not be treated as trusted instructions.

Mitigation: Ground responses in focused retrieved evidence, cite saved posts when useful, and clearly state when the saved evidence is weak or missing.

## Reference(s):

- [Awaek ClawHub page](https://clawhub.ai/1lystore/skills/awaek)
- [Awaek project homepage](https://github.com/1lystore/awaek)
- [OpenClaw xurl skill](https://github.com/openclaw/openclaw/blob/main/skills/xurl/SKILL.md)
- [OpenClaw xAI provider docs](https://docs.openclaw.ai/providers/xai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text with inline shell commands and JSON retrieval plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should be grounded in retrieved saved-bookmark evidence and should state when evidence is weak or missing.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
