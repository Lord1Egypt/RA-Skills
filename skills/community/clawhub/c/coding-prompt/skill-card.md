## Description:

Optimizes AI coding prompts by diagnosing missing context, constraints, acceptance criteria, and failure patterns, then rewriting prompts or giving targeted coaching during active coding sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuhanli](https://clawhub.ai/user/neuhanli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to improve prompts for coding agents before or during implementation, correction, review, and testing workflows. It is intended for explicit prompt review and for limited active-session coaching on high-priority failure signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep giving limited coaching alerts after activation during the same session.

Mitigation: Use it when prompt-coaching is desired, and treat alerts as additive guidance that should not override the user's active instruction.

Risk: The skill can update its learnings file only when the user explicitly asks to update the skill and confirms the proposed entry.

Mitigation: Review proposed learnings before confirmation and keep only reusable preferences or lessons that should persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neuhanli/skills/coding-prompt)
- [Prompt Diagnosis Checklist](references/checklist.md)
- [Core Principles](references/principles.md)
- [Communication Patterns](references/patterns.md)
- [Workflow Templates](references/templates.md)
- [Anti-Pattern Quick Reference](references/anti-patterns.md)
- [Structural Wisdom](references/structure.md)
- [Coding Prompt Learnings](references/learnings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prompt diagnosis, rewritten prompts, and concise coaching alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bilingual Chinese and English prompt text when triggered by Chinese activation phrases.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
