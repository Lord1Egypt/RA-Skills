## Description:

Manage software development sprints and stories in Bolt, including story creation and updates, Kanban status transitions, blocker and dependency tracking, sprint digests, AI activity logging, and file attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ndhill84](https://clawhub.ai/user/ndhill84)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to let an agent inspect and update Bolt projects, sprints, stories, blockers, dependencies, notes, files, and sprint summaries through the Bolt REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad live write and delete access to Bolt projects, sprints, stories, files, labels, notes, and agent-session events.

Mitigation: Require explicit confirmation before deletes, sprint close actions, file deletion, batch updates, and other destructive or high-impact changes; use dry-run options where the API supports them.

Risk: API tokens may be sent to a user-configured Bolt URL.

Mitigation: Use trusted Bolt server URLs, prefer HTTPS for non-local servers, keep BOLT_API_TOKEN narrowly scoped, and avoid exposing tokens in logs or shell history.

Risk: The release guidance mentions an unpinned npx install path.

Mitigation: Install only from trusted sources and verify the package or source before using unpinned installation commands.

## Reference(s):

- [Bolt API Reference](artifact/references/api-reference.md)
- [Bolt Workflow Patterns](artifact/references/workflows.md)
- [Bolt Sprint ClawHub Listing](https://clawhub.ai/ndhill84/skills/bolt-skill)
- [Publisher Profile](https://clawhub.ai/user/ndhill84)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BOLT_BASE_URL and may use BOLT_API_TOKEN when the Bolt server requires authentication.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
