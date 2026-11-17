## Description:

Detects and mitigates hallucinations in agent outputs by self-checking facts, verifying claims, and correcting unsupported or contradictory information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tooled-app](https://clawhub.ai/user/tooled-app)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add self-checks, confidence calibration, verification prompts, and correction logging to LLM-based agents. It is intended to reduce unsupported factual claims, fabricated tool results, and misleading reasoning before responses or agent actions are finalized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Correction logs may persist sensitive conversation-derived content.

Mitigation: Keep logs in a skill-specific location, redact sensitive content, and set retention limits.

Risk: Suggested edits to AGENTS.md, SKILL.md, or TOOLS.md may affect broad agent behavior.

Mitigation: Require administrator opt-in and manually review instruction-file changes before enabling them.

Risk: Reliability guidance may be adopted without sufficient release review.

Mitigation: Review and scan the skill before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tooled-app/skills/anti-hallucination-skill)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with checklists and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose correction logs and edits to agent instruction files when enabled.]

## Skill Version(s):

1.1.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
