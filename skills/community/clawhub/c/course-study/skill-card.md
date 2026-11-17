## Description:

Creates Chinese lecture-by-lecture study companions from course PDFs, records sourced concepts in a course memory bank, and supports follow-up questions and final review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT

## Use Case:

Students use this skill to turn course slides into page-linked explanations and exam-focused study notes, maintain a course memory bank, answer questions about recorded concepts, and compile end-of-term reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A course folder containing 管理/catalog.py can cause the agent to execute untrusted local Python code after writing notes.

Mitigation: Use only trusted course folders and scripts, or remove or disable the catalog.py step before using shared or downloaded materials.

## Reference(s):

- [course-study release](https://clawhub.ai/vincentjiang06/skills/course-study)
- [course-study documentation](README.en.md)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Chinese Markdown study companions, memory-bank entries, and review notes; conversational text for follow-up questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Page-linked explanations with exam-evidence labels; optional PDF export on request.]

## Skill Version(s):

4.2.1 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
