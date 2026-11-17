## Description:

DeepTutor 轻量辅导台 is a lightweight personalized tutoring workflow that maintains inspectable learner memory, tracks mastery with BKT-lite, calibrates practice difficulty, supports multi-perspective discussion, and grounds explanations in provided sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenxianxuexifa](https://clawhub.ai/user/shenxianxuexifa)

### License/Terms of Use:

MIT-0

## Use Case:

External educators, learners, and tutoring agents use this skill for long-running one-to-one or small-group tutoring where learner weaknesses should be remembered, practice should be calibrated to mastery, and explanations should cite the learner's selected source material. It is especially oriented toward chemistry and other school subjects, while routing pure summaries, one-off answers, schedule planning, and flashcard-only work to more specific skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learner profiles can expose sensitive learning records if used without learner agreement or stored in shared workspaces.

Mitigation: Use only with learners who agree to persistent profiling, avoid real names for student_id, keep tutor_memory out of shared or public workspaces, and provide clear inspect, delete, and export instructions.

Risk: Using raw student_id values as file paths can allow unsafe filenames or path traversal.

Mitigation: Validate student_id before file operations and reject path separators, '..', absolute paths, and other unsafe filename characters.

## Reference(s):

- [ClawHub skill page: DeepTutor 轻量辅导台](https://clawhub.ai/shenxianxuexifa/skills/deeptutor-lite)
- [ClawHub publisher profile: shenxianxuexifa](https://clawhub.ai/user/shenxianxuexifa)
- [HKUDS/DeepTutor project site](https://deeptutor.info)
- [HKUDS/DeepTutor arXiv:2604.26962](https://arxiv.org/abs/2604.26962)
- [THU-MAIC/OpenMAIC DOI 10.1007/s11390-025-6000-0](https://doi.org/10.1007/s11390-025-6000-0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tutoring responses with optional plain-text tables, JSON-like learner memory fields, and code or HTML snippets for visual explanations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update tutor_memory/<student_id>.md, session notes, review checklists, Anki handoff guidance, or optional visualization files when the host agent supports those actions.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
