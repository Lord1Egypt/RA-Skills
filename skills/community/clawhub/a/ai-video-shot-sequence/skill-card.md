## Description:

Guides agents to design coherent AI video shot sequences that turn a script scene or single storyboard frame into a paced narrative sequence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beermanzz](https://clawhub.ai/user/beermanzz)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video prompt writers, and agent users use this skill to plan cinematic shot sequences from scene descriptions, including shot order, rhythm, movement, sound cues, and continuity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The framework has a minor element-count inconsistency that may confuse checklist use.

Mitigation: Review generated shot plans against the sequence checklist and reconcile element counts before production use.

Risk: The skill provides Chinese-language guidance only, which may be misunderstood in non-Chinese workflows.

Mitigation: Use a qualified bilingual reviewer or translation step before applying outputs in non-Chinese production settings.

Risk: AI video generation may struggle with cross-shot continuity, micro-expressions, motion stability, and synchronized audio.

Mitigation: Validate character assets, lighting direction, motion feasibility, and audio notes during creative review before rendering or publishing.

## Reference(s):

- [sequence-design.md](references/sequence-design.md)
- [sequence-templates.md](references/sequence-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance with shot lists, sequence templates, rhythm notes, and quality checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language documentation-only guidance; no executable behavior, account access, persistent state, or file modification is identified in server security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
