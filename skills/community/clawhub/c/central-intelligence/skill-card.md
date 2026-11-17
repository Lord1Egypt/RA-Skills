## Description:

Persistent memory across sessions for remembering facts, recalling them later with semantic search, sharing knowledge between agents, and forgetting outdated memories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alekseimarchenko](https://clawhub.ai/user/alekseimarchenko)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and AI-agent users use this skill to persist selected preferences, project decisions, and other useful context across sessions, then recall or delete those memories when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist user and project context to a third-party remote memory service.

Mitigation: Require manual review before storing or sharing memories, and avoid storing confidential project, business, personal, or credential material.

Risk: Shared memories can expose information beyond the current agent scope.

Mitigation: Keep memories at agent scope by default and share to user or org scope only when the content is non-sensitive and intentionally reusable.

Risk: Recalled memories may be stale or no longer accurate.

Mitigation: Verify recalled information before using it for critical decisions or user-facing actions.

## Reference(s):

- [Central Intelligence homepage](https://centralintelligence.online)
- [Central Intelligence repository](https://github.com/AlekseiMarchenko/central-intelligence)
- [ClawHub skill listing](https://clawhub.ai/alekseimarchenko/skills/central-intelligence)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Configuration, Guidance]

**Output Format:** [Markdown instructions with curl command examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CI_API_KEY and uses a remote memory service for remember, recall, context, forget, and share commands.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
