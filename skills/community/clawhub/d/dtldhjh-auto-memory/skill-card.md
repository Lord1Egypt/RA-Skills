## Description:

Auto Memory gives OpenClaw agents persistent memory by extracting recent session content, summarizing it, deduplicating entries, and updating daily memory files and indexes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtldhjh](https://clawhub.ai/user/dtldhjh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain persistent OpenClaw memory from recent sessions, including daily notes, longer-term summaries, learnings, and searchable indexes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain and index private conversation content long term.

Mitigation: Use it only in workspaces approved for persistent memory, avoid secrets or confidential content, and review stored memory files regularly.

Risk: The skill can share selected learning and error content across agents.

Mitigation: Require user or administrator approval before enabling shared writes and limit the skill to trusted agents.

Risk: The skill can send recent memory text to a configured model provider.

Mitigation: Configure only approved providers and redact secrets before persistence or network use.

Risk: Security evidence reports an agent-id code-execution flaw.

Mitigation: Validate agent identifiers and review the scripts before installation or scheduled execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dtldhjh/skills/dtldhjh-auto-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown memory files and shell-script console output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily memory, learning, error, shared-learning, index-state, and long-term MEMORY.md files in OpenClaw workspaces.]

## Skill Version(s):

3.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
