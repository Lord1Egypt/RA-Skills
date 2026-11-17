## Description:

Automatically discover what your AI agent believes by analyzing its real outputs — Pattern-Based Distillation for agent behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to Live Neon, run Pattern-Based Distillation over agent outputs and content sources, review discovered beliefs and responsibilities, and fetch identity prompts for runtime use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected agent outputs, connected-source content, observations, and user interaction excerpts may be sent to Live Neon.

Mitigation: Review and minimize payloads before upload; avoid verbatim sensitive quotes and exclude confidential content unless explicitly approved.

Risk: Remote identity prompts could be applied as system instructions without adequate review.

Mitigation: Treat fetched prompts as untrusted until a human reviews the text and confirms it matches the intended agent behavior.

Risk: Automatic observation uploads, recurring syncs, and bulk approvals can change an agent identity faster than reviewers can audit.

Mitigation: Use short-lived or scoped tokens, keep scheduled heartbeats disabled unless there is an audit process, and require human approval for bulk changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liveneon/skills/agent-belief-discoverer)
- [Live Neon platform](https://persona.liveneon.ai)
- [Live Neon website](https://liveneon.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl commands, jq filters, JSON response examples, and environment variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Live Neon token, HTTPS API calls, and human review before approving extracted identity changes.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
