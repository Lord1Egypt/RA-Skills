## Description:

Generates junior-high class meeting or English class PPT outlines and presentation content when the user asks for class meeting, homeroom, English lesson, open-class, or related PPT materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouyuzhy](https://clawhub.ai/user/zhouyuzhy)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers, education staff, and agent users use this skill to turn junior-high class meeting or English lesson requests into structured PPT outlines, teaching activities, speaker notes, and final presentation content through an AI PPT generation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated classroom material may contain inaccurate, age-inappropriate, or locally unsuitable lesson content.

Mitigation: Review generated lesson plans, activities, and speaker notes for accuracy, age appropriateness, and preferred classroom language before use.

Risk: A referenced class-topic link in the skill text appears mistyped, which may prevent an agent from finding the intended local reference.

Mitigation: Confirm local reference paths before relying on retrieved topic material; use artifact/references/class-topics.md as the available class meeting topic library.

## Reference(s):

- [BARF Prompts Framework](artifact/references/barf.md)
- [Class Meeting Topic Library](artifact/references/class-topics.md)
- [English Lesson Topic Library](artifact/references/english-topics.md)
- [ClawHub Skill Page](https://clawhub.ai/zhouyuzhy/skills/class-ppt-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style PPT outline and lesson-planning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May hand off the generated outline to ai-ppt-generator for final presentation creation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
