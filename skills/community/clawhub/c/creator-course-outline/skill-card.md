## Description: <br>
Creator Course Outline helps agents generate module structures, unit objectives, assignments, milestones, and learner friction points for creator courses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, educators, and course operators use this skill to turn course topics, audience details, goals, and duration into a review-ready curriculum outline with objectives, assignments, milestones, and confirmation gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local helper can create or overwrite files when an output path is provided. <br>
Mitigation: Choose output paths deliberately and use dry-run or stdout when reviewing behavior. <br>
Risk: Course outlines may be incomplete or misleading if source material is sparse or sensitive material is included. <br>
Mitigation: Review the generated draft, confirm missing information, and redact personal or sensitive input before processing. <br>
Risk: The artifact contains unused audit or scanning code outside the normal configured workflow. <br>
Mitigation: Review future updates carefully if that code becomes exposed or enabled. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/creator-course-outline) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Structured Specification](artifact/resources/spec.json) <br>
- [Output Template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured Markdown, with optional JSON output from the local helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable drafts and action checklists; the helper can write an output file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
