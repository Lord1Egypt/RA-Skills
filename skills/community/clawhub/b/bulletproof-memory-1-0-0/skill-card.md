## Description:

Never lose context again. The Write-Ahead Log (WAL) protocol with SESSION-STATE.md gives your agent bulletproof memory that survives compaction, restarts, and distractions. Part of the Hal Stack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leowing](https://clawhub.ai/user/leowing)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add a write-ahead memory protocol that records active task context, user corrections, and recovery notes in workspace files before context is lost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to automatically persist private user details and active task context to local files.

Mitigation: Require explicit user consent before enabling automatic memory writes, exclude secrets and sensitive personal data, and define what may be stored.

Risk: The skill encourages reloading stored context, which may expose stale or overly broad workspace memory.

Mitigation: Limit which memory files may be read and provide a regular review, redaction, and deletion process for stored memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leowing/skills/bulletproof-memory-1-0-0)
- [PARA Second Brain](https://clawdhub.com/halthelobster/para-second-brain)
- [Proactive Agent](https://clawdhub.com/halthelobster/proactive-agent)

## Skill Output:

**Output Type(s):** [Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline setup snippets and protocol text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory protocol instructions and example SESSION-STATE.md content for an agent workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
