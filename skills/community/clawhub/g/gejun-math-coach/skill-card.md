## Description:

Gejun Math Coach is a Chinese high-school math tutoring agent that guides students through problem analysis, worked solutions, multiple methods, variants, error diagnosis, Socratic questioning, and a Three-One reflection protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abill6688](https://clawhub.ai/user/abill6688)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and educators use this skill for Chinese high-school math coaching, including Gaokao-style problem solving, concept decomposition, alternative solution comparison, variant generation, and error diagnosis. The agent emphasizes guided reasoning and post-solution reflection rather than only returning final answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional voice workflow writes conversation-derived audio to a shared predictable temporary path.

Mitigation: Treat voice playback as opt-in, use a private unique temporary file, and clean up generated audio after playback.

Risk: Broad trigger keywords may activate the skill when a user did not intend to use the math coach.

Mitigation: Narrow trigger keywords or invoke the skill explicitly in environments where broad activation is undesirable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abill6688/skills/gejun-math-coach)
- [Workflow Templates](references/workflow-templates.md)
- [Examples](references/examples.md)
- [Three-One Reflection Protocol](references/reflection-protocol.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown tutoring dialogue with math notation, structured feedback, and optional shell commands for voice playback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language responses; optional voice integration; no fixed token cap specified]

## Skill Version(s):

5.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
