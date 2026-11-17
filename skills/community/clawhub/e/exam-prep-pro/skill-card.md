## Description:

Exam Prep Pro helps agents create structured study plans, high-frequency topic review cards, practice questions, mistake remediation, and final sprint guidance for supported Chinese professional exams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcheisenberg](https://clawhub.ai/user/mcheisenberg)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and exam-prep agents use this skill to plan study schedules, review high-frequency topics, generate practice questions with explanations, and remediate mistakes for supported Chinese professional exams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an off-platform paid activation flow that directs users to an external payment link and asks for a payment receipt screenshot.

Mitigation: Review the payment and activation flow before installation, and prefer platform billing or another clearly governed purchase path.

Risk: The Pro unlock path requires local script execution and stores activation state in a home-directory marker file.

Mitigation: Inspect the verifier before running it, execute it only in an appropriate local environment, and avoid sharing activation codes or local marker contents.

Risk: The bundled activation materials include plaintext activation data and local activation state handling.

Mitigation: Limit access to activation files, rotate or replace bundled codes when publishing, and use scoped secure storage for activation state.

Risk: Exam plans and practice content can be incomplete or outdated if exam rules, syllabi, or weightings change.

Mitigation: Check important study plans and exam facts against official exam sources before relying on them for paid or high-stakes preparation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcheisenberg/skills/exam-prep-pro)
- [考试注册表](references/exam_registry.md)
- [公务员考试考纲与权重](references/gwy_syllabus.md)
- [公务员考试高频考点详解](references/gwy_highfreq.md)
- [法考考纲与权重](references/fk_syllabus.md)
- [法考高频考点详解](references/fk_highfreq.md)
- [注册会计师（CPA）考纲与权重](references/cpa_syllabus.md)
- [CPA高频考点详解](references/cpa_highfreq.md)
- [教师资格证考纲与权重](references/jszg_syllabus.md)
- [教师资格证高频考点详解](references/jszg_highfreq.md)
- [建造师考试考纲与权重](references/jzs_syllabus.md)
- [建造师高频考点详解](references/jzs_highfreq.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with structured study plans, review cards, practice questions, answer explanations, and occasional inline shell commands for activation checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for exam type, exam date, daily study time, current level, and weak areas before producing personalized prep guidance.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
