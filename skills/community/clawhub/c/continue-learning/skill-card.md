## Description:

Instinct-based learning system for OpenClaw that analyzes sessions, detects patterns, creates atomic learnings with confidence scoring, and suggests optimizations for self-evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adelpro](https://clawhub.ai/user/adelpro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to analyze OpenClaw session history, identify recurring behavior and error patterns, and generate reviewed learning artifacts or optimization suggestions for self-improving agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads recent OpenClaw session logs and may process private interaction history.

Mitigation: Run analysis with an explicit --agent scope when possible, and use --all only when broad review is needed.

Risk: Session-derived snippets may retain sensitive details despite redaction.

Mitigation: Review stored learning contents periodically and run the prune command if sensitive data may have appeared in tool errors or session output.

Risk: The skill persists derived instincts, patterns, and optimization suggestions locally.

Mitigation: Use the documented retention limits and prune command to remove stored learning data before sharing or retiring a workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adelpro/skills/continue-learning)

## Skill Output:

**Output Type(s):** [text, JSON files, shell commands, guidance]

**Output Format:** [Console text plus local JSON and JSONL learning files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; analysis requires an explicit --agent scope or explicit --all selection.]

## Skill Version(s):

1.3.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
