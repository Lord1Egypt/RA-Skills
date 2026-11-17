## Description:

A Chinese-language course-development assistant that turns project reviews, expert interviews, workflows, policies, product knowledge, legacy courseware, training notes, or course topics into enterprise training course materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cylunjoe](https://clawhub.ai/user/cylunjoe)

### License/Terms of Use:

MIT-0

## Use Case:

Training designers, internal enablement teams, and course developers use this skill to evaluate source material, extract reusable methods, design course structure, and generate teaching assets such as outlines, cases, exercises, question banks, PPT page drafts, and instructor manuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local course documents that the user explicitly points it at, including PDF and DOCX files.

Mitigation: Review source documents before processing them and only provide files that are intended for course-development use.

Risk: PDF and DOCX parsing depends on optional Python packages installed in the execution environment.

Mitigation: Use a virtual environment and prefer hash-verified dependency installation where stricter supply-chain controls are required.

Risk: Generated training materials may include inferred, simulated, or externally expanded content.

Mitigation: Review output labels and confirm facts, cases, legal requirements, standards, and current data before teaching or publishing the course.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cylunjoe/skills/experience-extraction-course-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/cylunjoe)
- [Course Development Framework](artifact/references/course-development-framework.md)
- [Course Format Specification](artifact/references/course-format-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown with tables, structured course-development sections, optional bash commands, and optional local file-reading output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can ask up to three high-impact clarification questions, conditionally use STAR and PRM analysis, and generate full course deliverables only when explicitly requested.]

## Skill Version(s):

1.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
