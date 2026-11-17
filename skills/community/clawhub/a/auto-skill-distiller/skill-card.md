## Description:

Distill completed multi-step workflows into reusable skills using quality gates for novelty, success, reuse potential, grounding, IP boundaries, trigger discipline, and pre-publish review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christianye](https://clawhub.ai/user/christianye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill after complex tasks to decide whether a successful workflow should become a reusable skill, a memory note, or a lessons-learned entry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or update persistent skills and memory notes without a clear pre-write approval step.

Mitigation: Require explicit confirmation before any SKILL.md, registry, or memory write.

Risk: Generated skill content may include private data or prompt-injection text before publication.

Mitigation: Review generated content for private data and prompt-injection text before using or publishing it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/christianye/skills/auto-skill-distiller)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with example code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose SKILL.md content, registry notes, memory entries, and pre-publish checks; users should approve writes before enabling automatic persistence.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
